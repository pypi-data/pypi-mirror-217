from __future__ import annotations
import copy

from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import subprocess
from textwrap import indent
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray
from hpcflow.sdk import app
from hpcflow.sdk.core.errors import JobscriptSubmissionFailure

from hpcflow.sdk.core.json_like import ChildObjectSpec, JSONLike
from hpcflow.sdk.submission.schedulers import Scheduler
from hpcflow.sdk.submission.schedulers.direct import DirectPosix, DirectWindows
from hpcflow.sdk.submission.schedulers.sge import SGEPosix
from hpcflow.sdk.submission.schedulers.slurm import SlurmPosix
from hpcflow.sdk.submission.shells import DEFAULT_SHELL_NAMES, get_shell


# lookup by (scheduler, `os.name`):
scheduler_cls_lookup = {
    (None, "posix"): DirectPosix,
    (None, "nt"): DirectWindows,
    ("sge", "posix"): SGEPosix,
    ("slurm", "posix"): SlurmPosix,
}


def generate_EAR_resource_map(
    task: app.WorkflowTask,
    loop_idx: Dict,
) -> Tuple[List[app.ElementResources], List[int], NDArray, NDArray]:
    """Generate an integer array whose rows represent actions and columns represent task
    elements and whose values index unique resources."""
    # TODO: assume single iteration for now; later we will loop over Loop tasks for each
    # included task and call this func with specific loop indices
    none_val = -1
    resources = []
    resource_hashes = []

    arr_shape = (task.num_actions, task.num_elements)
    resource_map = np.empty(arr_shape, dtype=int)
    EAR_ID_map = np.empty(arr_shape, dtype=int)
    # EAR_idx_map = np.empty(
    #     shape=arr_shape,
    #     dtype=[("EAR_idx", np.int32), ("run_idx", np.int32), ("iteration_idx", np.int32)],
    # )
    resource_map[:] = none_val
    EAR_ID_map[:] = none_val
    # EAR_idx_map[:] = (none_val, none_val, none_val)  # TODO: add iteration_idx as well

    for element in task.elements[:]:
        for iter_i in element.iterations:
            if iter_i.loop_idx != loop_idx:
                continue
            if iter_i.EARs_initialised:  # not strictly needed (actions will be empty)
                for act_idx, action in iter_i.actions.items():
                    for run in action.runs:
                        if run.submission_status.name == "PENDING":
                            # TODO: consider `time_limit`s
                            res_hash = run.resources.get_jobscript_hash()
                            if res_hash not in resource_hashes:
                                resource_hashes.append(res_hash)
                                resources.append(run.resources)
                            resource_map[act_idx][element.index] = resource_hashes.index(
                                res_hash
                            )
                            EAR_ID_map[act_idx, element.index] = run.id_
                            # EAR_idx_map[act_idx, element.index] = (
                            #     run.index,
                            #     run.run_idx,
                            #     iter_i.index,
                            # )

    return (
        resources,
        resource_hashes,
        resource_map,
        EAR_ID_map,
    )


def group_resource_map_into_jobscripts(
    resource_map: Union[List, NDArray],
    none_val: Any = -1,
):
    resource_map = np.asanyarray(resource_map)
    resource_idx = np.unique(resource_map)
    jobscripts = []
    allocated = np.zeros_like(resource_map)
    js_map = np.ones_like(resource_map, dtype=float) * np.nan
    nones_bool = resource_map == none_val
    stop = False
    for act_idx in range(resource_map.shape[0]):
        for res_i in resource_idx:
            if res_i == none_val:
                continue

            if res_i not in resource_map[act_idx]:
                continue

            resource_map[nones_bool] = res_i
            diff = np.cumsum(np.abs(np.diff(resource_map[act_idx:], axis=0)), axis=0)

            elem_bool = np.logical_and(
                resource_map[act_idx] == res_i, allocated[act_idx] == False
            )
            elem_idx = np.where(elem_bool)[0]
            act_elem_bool = np.logical_and(elem_bool, nones_bool[act_idx] == False)
            act_elem_idx = np.where(act_elem_bool)

            # add elements from downstream actions:
            ds_bool = np.logical_and(
                diff[:, elem_idx] == 0,
                nones_bool[act_idx + 1 :, elem_idx] == False,
            )
            ds_act_idx, ds_elem_idx = np.where(ds_bool)
            ds_act_idx += act_idx + 1
            ds_elem_idx = elem_idx[ds_elem_idx]

            EARs_by_elem = {k.item(): [act_idx] for k in act_elem_idx[0]}
            for ds_a, ds_e in zip(ds_act_idx, ds_elem_idx):
                ds_e_item = ds_e.item()
                if ds_e_item not in EARs_by_elem:
                    EARs_by_elem[ds_e_item] = []
                EARs_by_elem[ds_e_item].append(ds_a.item())

            EARs = np.vstack([np.ones_like(act_elem_idx) * act_idx, act_elem_idx])
            EARs = np.hstack([EARs, np.array([ds_act_idx, ds_elem_idx])])

            if not EARs.size:
                continue

            js = {
                "resources": res_i,
                "elements": dict(sorted(EARs_by_elem.items(), key=lambda x: x[0])),
            }
            allocated[EARs[0], EARs[1]] = True
            js_map[EARs[0], EARs[1]] = len(jobscripts)
            jobscripts.append(js)

            if np.all(allocated[~nones_bool]):
                stop = True
                break

        if stop:
            break

    resource_map[nones_bool] = none_val

    return jobscripts, js_map


def resolve_jobscript_dependencies(jobscripts, element_deps):
    # first pass is to find the mappings between jobscript elements:
    jobscript_deps = {}
    for js_idx, elem_deps in element_deps.items():
        # keys of new dict are other jobscript indices on which this jobscript (js_idx)
        # depends:
        jobscript_deps[js_idx] = {}

        for js_elem_idx_i, EAR_deps_i in elem_deps.items():
            # locate which jobscript elements this jobscript element depends on:
            for EAR_dep_j in EAR_deps_i:
                for js_k_idx, js_k in jobscripts.items():
                    if js_k_idx == js_idx:
                        break

                    if EAR_dep_j in js_k["EAR_ID"]:
                        if js_k_idx not in jobscript_deps[js_idx]:
                            jobscript_deps[js_idx][js_k_idx] = {"js_element_mapping": {}}

                        if (
                            js_elem_idx_i
                            not in jobscript_deps[js_idx][js_k_idx]["js_element_mapping"]
                        ):
                            jobscript_deps[js_idx][js_k_idx]["js_element_mapping"][
                                js_elem_idx_i
                            ] = []

                        # retrieve column index, which is the JS-element index:
                        js_elem_idx_k = np.where(
                            np.any(js_k["EAR_ID"] == EAR_dep_j, axis=0)
                        )[0][0].item()

                        # add js dependency element-mapping:
                        if (
                            js_elem_idx_k
                            not in jobscript_deps[js_idx][js_k_idx]["js_element_mapping"][
                                js_elem_idx_i
                            ]
                        ):
                            jobscript_deps[js_idx][js_k_idx]["js_element_mapping"][
                                js_elem_idx_i
                            ].append(js_elem_idx_k)

    # next we can determine if two jobscripts have a one-to-one element mapping, which
    # means they can be submitted with a "job array" dependency relationship:
    for js_i_idx, deps_i in jobscript_deps.items():
        for js_k_idx, deps_j in deps_i.items():
            # is this an array dependency?

            js_i_num_js_elements = jobscripts[js_i_idx]["EAR_ID"].shape[1]
            js_k_num_js_elements = jobscripts[js_k_idx]["EAR_ID"].shape[1]

            is_all_i_elems = list(
                sorted(set(deps_j["js_element_mapping"].keys()))
            ) == list(range(js_i_num_js_elements))

            is_all_k_single = set(
                len(i) for i in deps_j["js_element_mapping"].values()
            ) == {1}

            is_all_k_elems = list(
                sorted(i[0] for i in deps_j["js_element_mapping"].values())
            ) == list(range(js_k_num_js_elements))

            is_arr = is_all_i_elems and is_all_k_single and is_all_k_elems
            jobscript_deps[js_i_idx][js_k_idx]["is_array"] = is_arr

    return jobscript_deps


def merge_jobscripts_across_tasks(jobscripts: Dict) -> Dict:
    """Try to merge jobscripts between tasks.

    This is possible if two jobscripts share the same resources and have an array
    dependency (i.e. one-to-one element dependency mapping).

    """

    for js_idx, js in jobscripts.items():
        # for now only attempt to merge a jobscript with a single dependency:
        if len(js["dependencies"]) == 1:
            js_j_idx = next(iter(js["dependencies"]))
            dep_info = js["dependencies"][js_j_idx]
            js_j = jobscripts[js_j_idx]  # the jobscript we are merging `js` into

            # can only merge if resources are the same and is array dependency:
            if js["resource_hash"] == js_j["resource_hash"] and dep_info["is_array"]:
                num_loop_idx = len(
                    js_j["task_loop_idx"]
                )  # TODO: should this be: `js_j["task_loop_idx"][0]`?

                # append task_insert_IDs
                js_j["task_insert_IDs"].append(js["task_insert_IDs"][0])
                js_j["task_loop_idx"].append(js["task_loop_idx"][0])

                add_acts = []
                for t_act in js["task_actions"]:
                    t_act = copy.copy(t_act)
                    t_act[2] += num_loop_idx
                    add_acts.append(t_act)

                js_j["task_actions"].extend(add_acts)
                js_j["task_elements"].update(js["task_elements"])

                # update EARs dict
                # js_j["EARs"].update(js["EARs"])

                # append to elements and elements_idx list
                js_j["EAR_ID"] = np.vstack((js_j["EAR_ID"], js["EAR_ID"]))

                # mark this js as defunct
                js["is_merged"] = True

                # update dependencies of any downstream jobscripts that refer to this js
                for ds_js_idx, ds_js in jobscripts.items():
                    if ds_js_idx <= js_idx:
                        continue
                    for dep_k_js_idx in list(ds_js["dependencies"].keys()):
                        if dep_k_js_idx == js_idx:
                            jobscripts[ds_js_idx]["dependencies"][js_j_idx] = ds_js[
                                "dependencies"
                            ].pop(dep_k_js_idx)

    # remove is_merged jobscripts:
    jobscripts = {k: v for k, v in jobscripts.items() if "is_merged" not in v}

    return jobscripts


def jobscripts_to_list(jobscripts: Dict[int, Dict]) -> List[Dict]:
    """Convert the jobscripts dict to a list, normalising jobscript indices so they refer
    to list indices; also remove `resource_hash`."""
    lst = []
    for js_idx, js in jobscripts.items():
        new_idx = len(lst)
        if js_idx != new_idx:
            # need to reindex jobscripts that depend on this one
            for js_j_idx, js_j in jobscripts.items():
                if js_j_idx <= js_idx:
                    continue
                if js_idx in js_j["dependencies"]:
                    jobscripts[js_j_idx]["dependencies"][new_idx] = jobscripts[js_j_idx][
                        "dependencies"
                    ].pop(js_idx)
        del jobscripts[js_idx]["resource_hash"]
        lst.append(js)

    return lst


class Jobscript(JSONLike):
    _app_attr = "app"
    _EAR_files_delimiter = ":"
    _workflow_app_alias = "wkflow_app"

    _child_objects = (
        ChildObjectSpec(
            name="resources",
            class_name="ElementResources",
        ),
    )

    def __init__(
        self,
        task_insert_IDs: List[int],
        task_actions: List[Tuple],
        task_elements: Dict[int, List[int]],
        EAR_ID: NDArray,
        resources: app.ElementResources,
        task_loop_idx: List[Dict],
        dependencies: Dict[int:Dict],
        submit_time: Optional[datetime] = None,
        scheduler_job_ID: Optional[str] = None,
        process_ID: Optional[int] = None,
        version_info: Optional[Tuple[str]] = None,
        os_name: Optional[str] = None,
        shell_name: Optional[str] = None,
        scheduler_name: Optional[str] = None,
    ):
        self._task_insert_IDs = task_insert_IDs
        self._task_loop_idx = task_loop_idx
        self._task_actions = task_actions
        self._task_elements = task_elements
        self._EAR_ID = EAR_ID
        self._resources = resources
        self._dependencies = dependencies

        # assigned on parent `Submission.submit` (or retrieved form persistent store):
        self._submit_time = submit_time

        self._scheduler_job_ID = scheduler_job_ID
        self._process_ID = process_ID
        self._version_info = version_info

        # assigned as submit-time:
        self._os_name = os_name
        self._shell_name = shell_name
        self._scheduler_name = scheduler_name

        self._submission = None  # assigned by parent Submission
        self._index = None  # assigned by parent Submission
        self._scheduler_obj = None  # assigned on first access to `scheduler` property
        self._shell_obj = None  # assigned on first access to `shell` property
        self._submit_time_obj = None  # assigned on first access to `submit_time` property

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"index={self.index!r}, "
            f"task_insert_IDs={self.task_insert_IDs!r}, "
            f"resources={self.resources!r}, "
            f"dependencies={self.dependencies!r}"
            f")"
        )

    def to_dict(self):
        dct = super().to_dict()
        del dct["_index"]
        del dct["_scheduler_obj"]
        del dct["_shell_obj"]
        del dct["_submit_time_obj"]
        dct = {k.lstrip("_"): v for k, v in dct.items()}
        dct["EAR_ID"] = dct["EAR_ID"].tolist()
        return dct

    @classmethod
    def from_json_like(cls, json_like, shared_data=None):
        json_like["EAR_ID"] = np.array(json_like["EAR_ID"])
        return super().from_json_like(json_like, shared_data)

    @property
    def workflow_app_alias(self):
        return self._workflow_app_alias

    def get_commands_file_name(self, js_action_idx, shell=None):
        shell = shell or self.shell
        return f"js_{self.index}_act_{js_action_idx}{shell.JS_EXT}"

    @property
    def task_insert_IDs(self):
        return self._task_insert_IDs

    @property
    def task_actions(self):
        return self._task_actions

    @property
    def task_elements(self):
        return self._task_elements

    @property
    def EAR_ID(self):
        return self._EAR_ID

    @property
    def resources(self):
        return self._resources

    @property
    def task_loop_idx(self):
        return self._task_loop_idx

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def submit_time(self):
        if self._submit_time_obj is None and self._submit_time:
            self._submit_time_obj = (
                datetime.strptime(self._submit_time, self.workflow.ts_fmt)
                .replace(tzinfo=timezone.utc)
                .astimezone()
            )
        return self._submit_time_obj

    @property
    def scheduler_job_ID(self):
        return self._scheduler_job_ID

    @property
    def process_ID(self):
        return self._process_ID

    @property
    def version_info(self):
        return self._version_info

    @property
    def index(self):
        return self._index

    @property
    def submission(self):
        return self._submission

    @property
    def workflow(self):
        return self.submission.workflow

    @property
    def num_actions(self):
        return self.EAR_ID.shape[0]

    @property
    def num_elements(self):
        return self.EAR_ID.shape[1]

    @property
    def is_array(self):
        if not self.scheduler_name:
            return False

        support_EAR_para = self.workflow._store._features.EAR_parallelism
        if self.resources.use_job_array is None:
            if self.num_elements > 1 and support_EAR_para:
                return True
            else:
                return False
        else:
            if self.resources.use_job_array and not support_EAR_para:
                raise ValueError(
                    f"Store type {self.workflow._store!r} does not support element "
                    f"parallelism, so jobs cannot be submitted as scheduler arrays."
                )
            return self.resources.use_job_array

    @property
    def os_name(self) -> Union[str, None]:
        return self._os_name or self.resources.os_name

    @property
    def shell_name(self) -> Union[str, None]:
        return self._shell_name or self.resources.shell

    @property
    def scheduler_name(self) -> Union[str, None]:
        return self._scheduler_name or self.resources.scheduler

    def _get_submission_os_args(self):
        return {"linux_release_file": self.app.config.linux_release_file}

    def _get_submission_shell_args(self):
        return self.resources.shell_args

    def _get_submission_scheduler_args(self):
        return self.resources.scheduler_args

    def _get_shell(self, os_name, shell_name, os_args=None, shell_args=None):
        """Get an arbitrary shell, not necessarily associated with submission."""
        os_args = os_args or {}
        shell_args = shell_args or {}
        return get_shell(
            shell_name=shell_name,
            os_name=os_name,
            os_args=os_args,
            **shell_args,
        )

    def _get_scheduler(self, scheduler_name, os_name, scheduler_args=None):
        """Get an arbitrary scheduler, not necessarily associated with submission."""
        scheduler_args = scheduler_args or {}
        key = (scheduler_name.lower() if scheduler_name else None, os_name.lower())
        try:
            scheduler_cls = scheduler_cls_lookup[key]
        except KeyError:
            raise ValueError(
                f"Unsupported combination of scheduler and operation system: {key!r}"
            )
        return scheduler_cls(**scheduler_args)

    @property
    def shell(self):
        """Retrieve the shell object for submission."""
        if self._shell_obj is None:
            self._shell_obj = self._get_shell(
                os_name=self.os_name,
                shell_name=self.shell_name,
                os_args=self._get_submission_os_args(),
                shell_args=self._get_submission_shell_args(),
            )
        return self._shell_obj

    @property
    def scheduler(self):
        """Retrieve the scheduler object for submission."""
        if self._scheduler_obj is None:
            self._scheduler_obj = self._get_scheduler(
                scheduler_name=self.scheduler_name,
                os_name=self.os_name,
                scheduler_args=self._get_submission_scheduler_args(),
            )
        return self._scheduler_obj

    @property
    def EAR_ID_file_name(self):
        return f"js_{self.index}_EAR_IDs.txt"

    @property
    def element_run_dir_file_name(self):
        return f"js_{self.index}_run_dirs.txt"

    @property
    def direct_stdout_file_name(self):
        """For direct execution stdout."""
        return f"js_{self.index}_stdout.log"

    @property
    def direct_stderr_file_name(self):
        """For direct execution stderr."""
        return f"js_{self.index}_stderr.log"

    @property
    def jobscript_name(self):
        return f"js_{self.index}{self.shell.JS_EXT}"

    @property
    def EAR_ID_file_path(self):
        return self.submission.path / self.EAR_ID_file_name

    @property
    def element_run_dir_file_path(self):
        return self.submission.path / self.element_run_dir_file_name

    @property
    def jobscript_path(self):
        return self.submission.path / self.jobscript_name

    @property
    def direct_stdout_path(self):
        return self.submission.path / self.direct_stdout_file_name

    @property
    def direct_stderr_path(self):
        return self.submission.path / self.direct_stderr_file_name

    def _set_submit_time(self, submit_time: datetime) -> None:
        submit_time = submit_time.strftime(self.workflow.ts_fmt)
        self._submit_time = submit_time
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            submit_time=submit_time,
        )

    def _set_scheduler_job_ID(self, job_ID: str) -> None:
        """For scheduled submission only."""
        self._scheduler_job_ID = job_ID
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            scheduler_job_ID=job_ID,
        )

    def _set_process_ID(self, process_ID: str) -> None:
        """For direct submission only."""
        self._process_ID = process_ID
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            process_ID=process_ID,
        )

    def _set_version_info(self, version_info: Dict) -> None:
        self._version_info = version_info
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            version_info=version_info,
        )

    def _set_os_name(self) -> None:
        """Set the OS name for this jobscript. This is invoked at submit-time."""
        self._os_name = self.resources.os_name or os.name
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            os_name=self._os_name,
        )

    def _set_shell_name(self) -> None:
        """Set the shell name for this jobscript. This is invoked at submit-time."""
        self._shell_name = self.resources.shell or DEFAULT_SHELL_NAMES[self.os_name]
        self.workflow._store.set_jobscript_metadata(
            sub_idx=self.submission.index,
            js_idx=self.index,
            shell_name=self._shell_name,
        )

    def _set_scheduler_name(self) -> None:
        """Set the scheduler name for this jobscript. This is invoked at submit-time."""
        self._scheduler_name = self.resources.scheduler or None
        if self._scheduler_name:
            self.workflow._store.set_jobscript_metadata(
                sub_idx=self.submission.index,
                js_idx=self.index,
                scheduler_name=self._scheduler_name,
            )

    def get_task_loop_idx_array(self):
        loop_idx = np.empty_like(self.EAR_ID)
        loop_idx[:] = np.array([i[2] for i in self.task_actions]).reshape(
            (len(self.task_actions), 1)
        )
        return loop_idx

    def write_EAR_ID_file(self):
        """Write a text file with `num_elements` lines and `num_actions` delimited tokens
        per line, representing whether a given EAR must be executed."""

        with self.EAR_ID_file_path.open(mode="wt", newline="\n") as fp:
            # can't specify "open" newline if we pass the file name only, so pass handle:
            np.savetxt(
                fname=fp,
                X=(self.EAR_ID).T,
                fmt="%.0f",
                delimiter=self._EAR_files_delimiter,
            )

    def write_element_run_dir_file(self, run_dirs: List[List[Path]]):
        """Write a text file with `num_elements` lines and `num_actions` delimited tokens
        per line, representing the working directory for each EAR.

        We assume a given task element's actions all run in the same directory, but in
        general a jobscript "element" may cross task boundaries, so we need to provide
        the directory for each jobscript-element/jobscript-action combination.

        """
        run_dirs = self.shell.prepare_element_run_dirs(run_dirs)
        with self.element_run_dir_file_path.open(mode="wt", newline="\n") as fp:
            # can't specify "open" newline if we pass the file name only, so pass handle:
            np.savetxt(
                fname=fp,
                X=np.array(run_dirs),
                fmt="%s",
                delimiter=self._EAR_files_delimiter,
            )

    def compose_jobscript(
        self,
        os_name: str = None,
        shell_name: str = None,
        os_args: Optional[Dict] = None,
        shell_args: Optional[Dict] = None,
        scheduler_name: Optional[str] = None,
        scheduler_args: Optional[Dict] = None,
    ) -> str:
        """Prepare the jobscript file string."""

        os_name = os_name or self.os_name
        shell_name = shell_name or self.shell_name
        scheduler_name = scheduler_name or self.scheduler_name

        if not os_name:
            raise RuntimeError(
                f"Jobscript {self.index} `os_name` is not yet set. Pass the `os_name` as "
                f"a method argument to compose the jobscript for a given `os_name`."
            )
        if not shell_name:
            raise RuntimeError(
                f"Jobscript {self.index} `shell_name` is not yet set. Pass the "
                f"`shell_name` as a method argument to compose the jobscript for a given "
                f"`shell_name`."
            )

        shell = self._get_shell(
            os_name=os_name,
            shell_name=shell_name,
            os_args=os_args or self._get_submission_os_args(),
            shell_args=shell_args or self._get_submission_shell_args(),
        )
        scheduler = self._get_scheduler(
            scheduler_name=scheduler_name,
            os_name=os_name,
            scheduler_args=scheduler_args or self._get_submission_scheduler_args(),
        )

        env_setup = self.app.config._file.invoc_data["invocation"]["environment_setup"]
        if env_setup:
            env_setup = indent(env_setup.strip(), shell.JS_ENV_SETUP_INDENT)
            env_setup += "\n\n" + shell.JS_ENV_SETUP_INDENT
        else:
            env_setup = shell.JS_ENV_SETUP_INDENT

        app_invoc = list(self.app.run_time_info.invocation_command)
        header_args = shell.process_JS_header_args(
            {
                "workflow_app_alias": self.workflow_app_alias,
                "env_setup": env_setup,
                "app_invoc": app_invoc,
                "app_package_name": self.app.package_name,
                "config_dir": str(self.app.config.config_directory),
                "config_invoc_key": self.app.config.config_invocation_key,
                "workflow_path": self.workflow.path,
                "sub_idx": self.submission.index,
                "js_idx": self.index,
                "EAR_file_name": self.EAR_ID_file_name,
                "element_run_dirs_file_path": self.element_run_dir_file_name,
            }
        )

        shebang = shell.JS_SHEBANG.format(
            shebang_executable=" ".join(shell.shebang_executable),
            shebang_args=scheduler.shebang_args,
        )
        header = shell.JS_HEADER.format(**header_args)

        if isinstance(scheduler, Scheduler):
            header = shell.JS_SCHEDULER_HEADER.format(
                shebang=shebang,
                scheduler_options=scheduler.format_options(
                    resources=self.resources,
                    num_elements=self.num_elements,
                    is_array=self.is_array,
                    sub_idx=self.submission.index,
                ),
                header=header,
            )
        else:
            # the NullScheduler (direct submission)
            header = shell.JS_DIRECT_HEADER.format(
                shebang=shebang,
                header=header,
            )

        main = shell.JS_MAIN.format(
            num_actions=self.num_actions,
            EAR_files_delimiter=self._EAR_files_delimiter,
            workflow_app_alias=self.workflow_app_alias,
            commands_file_name=self.get_commands_file_name(r"${JS_act_idx}", shell=shell),
            app_package_name=self.app.package_name,
        )

        out = header

        if self.is_array:
            out += shell.JS_ELEMENT_ARRAY.format(
                scheduler_command=scheduler.js_cmd,
                scheduler_array_switch=scheduler.array_switch,
                scheduler_array_item_var=scheduler.array_item_var,
                num_elements=self.num_elements,
                main=main,
            )

        else:
            out += shell.JS_ELEMENT_LOOP.format(
                num_elements=self.num_elements,
                main=indent(main, shell.JS_INDENT),
            )

        return out

    def write_jobscript(
        self,
        os_name: str = None,
        shell_name: str = None,
        os_args: Optional[Dict] = None,
        shell_args: Optional[Dict] = None,
        scheduler_name: Optional[str] = None,
        scheduler_args: Optional[Dict] = None,
    ):
        js_str = self.compose_jobscript(
            os_name=os_name,
            shell_name=shell_name,
            os_args=os_args,
            shell_args=shell_args,
            scheduler_name=scheduler_name,
            scheduler_args=scheduler_args,
        )
        with self.jobscript_path.open("wt", newline="\n") as fp:
            fp.write(js_str)
        return self.jobscript_path

    def _get_EARs_arr(self):
        EARs_flat = self.workflow.get_EARs_from_IDs(self.EAR_ID.flatten())
        EARs_arr = np.array(EARs_flat).reshape(self.EAR_ID.shape)
        return EARs_arr

    def make_artifact_dirs(self):
        EARs_arr = self._get_EARs_arr()
        task_loop_idx_arr = self.get_task_loop_idx_array()

        run_dirs = []
        for js_elem_idx in range(self.num_elements):
            run_dirs_i = []
            for js_act_idx in range(self.num_actions):
                EAR_i = EARs_arr[js_act_idx, js_elem_idx]
                t_iID = EAR_i.task.insert_ID
                l_idx = task_loop_idx_arr[js_act_idx, js_elem_idx].item()
                r_idx = EAR_i.index

                loop_idx_i = self.task_loop_idx[l_idx]
                task_dir = self.workflow.tasks.get(insert_ID=t_iID).get_dir_name(
                    loop_idx_i
                )
                elem_dir = EAR_i.element.dir_name
                run_dir = f"r_{r_idx}"

                EAR_dir = Path(self.workflow.execution_path, task_dir, elem_dir, run_dir)
                EAR_dir.mkdir(exist_ok=True, parents=True)

                # copy (TODO: optionally symlink) any input files:
                for name, path in EAR_i.get("input_files", {}).items():
                    if path:
                        shutil.copy(path, EAR_dir)

                run_dirs_i.append(EAR_dir.relative_to(self.workflow.path))

            run_dirs.append(run_dirs_i)

        return run_dirs

    def submit(
        self,
        scheduler_refs: Dict[int, (str, bool)],
        print_stdout: Optional[bool] = False,
    ) -> str:
        run_dirs = self.make_artifact_dirs()
        self.write_EAR_ID_file()
        self.write_element_run_dir_file(run_dirs)
        js_path = self.write_jobscript()
        js_path = self.shell.prepare_JS_path(js_path)

        deps = []
        for js_idx, deps_i in self.dependencies.items():
            dep_job_ID, dep_js_is_arr = scheduler_refs[js_idx]
            # only submit an array dependency if both this jobscript and the dependency
            # are array jobs:
            dep_is_arr = deps_i["is_array"] and self.is_array and dep_js_is_arr
            deps.append((dep_job_ID, dep_is_arr))

        if not self.submission.JS_parallelism and self.index > 0:
            # add fake dependencies to all previously submitted jobscripts to avoid
            # simultaneous execution:
            for job_ID, (sched_ref, _) in scheduler_refs.items():
                deps.append((sched_ref, False))

        job_ID = None
        process_ID = None

        is_scheduler = isinstance(self.scheduler, Scheduler)

        err_args = {
            "js_idx": self.index,
            "js_path": js_path,
            "subprocess_exc": None,
            "job_ID_parse_exc": None,
        }
        try:
            submit_cmd = self.scheduler.get_submit_command(self.shell, js_path, deps)
            self.app.submission_logger.info(
                f"submitting jobscript {self.index!r} with command: {submit_cmd!r}"
            )
            if is_scheduler:
                # scheduled submission, wait for submission so we can parse the job ID:
                proc = subprocess.run(
                    args=submit_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=str(self.workflow.path),
                )
                stdout = proc.stdout.decode().strip()
                stderr = proc.stderr.decode().strip()
                err_args["stdout"] = stdout
                err_args["stderr"] = stderr
                if print_stdout and stdout:
                    print(stdout)

            else:
                # direct submission; submit jobscript asynchronously:
                with self.direct_stdout_path.open("wt") as fp_stdout:
                    with self.direct_stderr_path.open("wt") as fp_stderr:
                        proc = subprocess.Popen(
                            args=submit_cmd,
                            stdout=fp_stdout,
                            stderr=fp_stderr,
                            cwd=str(self.workflow.path),
                        )
                        process_ID = proc.pid

        except Exception as subprocess_exc:
            err_args["message"] = f"Failed to execute submit command."
            err_args["submit_cmd"] = submit_cmd
            err_args["stdout"] = None
            err_args["stderr"] = None
            err_args["subprocess_exc"] = subprocess_exc
            raise JobscriptSubmissionFailure(**err_args)

        if is_scheduler:
            # scheduled submission
            if stderr:
                err_args["message"] = "Non-empty stderr from submit command."
                err_args["submit_cmd"] = submit_cmd
                raise JobscriptSubmissionFailure(**err_args)

            try:
                job_ID = self.scheduler.parse_submission_output(stdout)

            except Exception as job_ID_parse_exc:
                # TODO: maybe handle this differently. If there is no stderr, then the job
                # probably did submit fine, but the issue is just with parsing the job ID
                # (e.g. if the scheduler version was updated and it now outputs
                # differently).
                err_args["message"] = "Failed to parse job ID from stdout."
                err_args["submit_cmd"] = submit_cmd
                err_args["job_ID_parse_exc"] = job_ID_parse_exc
                raise JobscriptSubmissionFailure(**err_args)

            self._set_scheduler_job_ID(job_ID)
            ref = job_ID

        else:
            # direct submission
            self._set_process_ID(process_ID)
            ref = process_ID

        self._set_submit_time(datetime.utcnow())

        return ref
