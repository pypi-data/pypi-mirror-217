"""
A class to run a pipeline.
"""
from functools import reduce
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from hyfi.__global__.config import __global_config__
from hyfi.composer import Composer
from hyfi.pipeline.configs import BaseRunConfig, PipeConfig, Pipes, RunningConfig
from hyfi.project import ProjectConfig
from hyfi.task import TaskConfig
from hyfi.utils.contexts import change_directory
from hyfi.utils.logging import LOGGING
from hyfi.workflow import WorkflowConfig

logger = LOGGING.getLogger(__name__)


class PipelineConfig(BaseRunConfig):
    """Pipeline Configuration"""

    steps: Optional[List[Union[str, Dict]]] = []
    initial_object: Optional[Any] = None
    use_task_as_initial_object: bool = False

    @validator("steps", pre=True)
    def steps_to_list(cls, v):
        """
        Convert a list of steps to a list

        Args:
            cls: class to use for conversion
            v: list of steps to convert

        Returns:
            list of steps converted to
        """
        return [v] if isinstance(v, str) else Composer.to_dict(v)

    def update_configs(
        self,
        rc: Union[Dict, RunningConfig],
    ):
        """
        Update running config with values from another config

        Args:
            rc: RunningConfig to update from
        """
        # If rc is a dict or dict it will be converted to RunningConfig.
        if isinstance(rc, dict):
            rc = RunningConfig(**rc)
        self.name = rc.name or self.name
        self.desc = rc.desc or self.desc

    def get_pipes(self, task: Optional[TaskConfig] = None) -> Pipes:
        """
        Get all pipes that this task is aware of

        Args:
            task: The task to use for the pipe

        Returns:
            A list of : class : `PipeConfig` objects
        """
        pipes: Pipes = []
        # Add pipes to the pipeline.
        for rc in PIPELINEs.get_RCs(self.steps):
            # Add a pipe to the pipeline.
            if rc.uses in self.__dict__ and isinstance(self.__dict__[rc.uses], dict):
                config = self.__dict__[rc.uses]
                pipe = PipeConfig(**Composer.update(config, rc.dict()))
                # Set the task to be used for the pipe.
                if task is not None:
                    pipe.task = task
                pipes.append(pipe)
        return pipes


Pipelines = List[PipelineConfig]


class PIPELINEs:
    """
    A class to run a pipeline.
    """

    @staticmethod
    def run_pipeline(
        config: Union[Dict, PipelineConfig],
        initial_object: Optional[Any] = None,
        task: Optional[TaskConfig] = None,
    ) -> Any:
        """
        Run a pipeline given a config

        Args:
            config: PipelineConfig to run the pipeline
            initial_obj: Object to use as initial value
            task: TaskConfig to use as task

        Returns:
            The result of the pipeline
        """
        # If config is not a PipelineConfig object it will be converted to a PipelineConfig object.
        if not isinstance(config, PipelineConfig):
            config = PipelineConfig(**Composer.to_dict(config))
        pipes = config.get_pipes(task)
        if initial_object is None and config.initial_object is not None:
            initial_object = config.initial_object
        # Return initial object for the initial object
        if not pipes:
            logger.warning("No pipes specified")
            return initial_object

        logger.info("Applying %s pipes", len(pipes))
        # Run the task in the current directory.
        if task is not None:
            with change_directory(task.root_dir):
                return reduce(PIPELINEs.run_pipe, pipes, initial_object)
        return reduce(PIPELINEs.run_pipe, pipes, initial_object)

    @staticmethod
    def run_pipe(
        obj: Any,
        config: Union[Dict, PipeConfig],
    ) -> Any:
        """
        Run a pipe on an object

        Args:
            obj: The object to pipe on
            config: The configuration for the pipe

        Returns:
            The result of the pipe
        """
        # Create a PipeConfig object if not already a PipeConfig.
        if not isinstance(config, PipeConfig):
            config = PipeConfig(**Composer.to_dict(config))
        pipe_fn = config.get_pipe_func()
        # Return the object that is being used to execute the pipe function.
        if pipe_fn is None:
            logger.warning("No pipe function specified")
            return obj
        # Run a pipe with the pipe_fn
        if config.verbose:
            logger.info("Running a pipe with %s", pipe_fn)
        # Apply pipe function to each object.
        if isinstance(obj, dict):
            objs = {}
            # Apply pipe to each object.
            for no, name in enumerate(obj):
                obj_ = obj[name]

                # Apply pipe to an object.
                if config.verbose:
                    logger.info(
                        "Applying pipe to an object [%s], %d/%d",
                        name,
                        no + 1,
                        len(obj),
                    )

                objs[name] = pipe_fn(obj_, config)
            return objs

        return pipe_fn(obj, config)

    @staticmethod
    def get_RCs(steps: list) -> List[RunningConfig]:
        """
        Parses and returns list of running configs

        Args:
            steps: list of config to parse

        Returns:
            list of : class : `RunningConfig` objects
        """
        RCs: List[RunningConfig] = []
        # Return the list of running RCs
        if not steps:
            logger.warning("No running configs provided")
            return RCs
        # Add running config to the list of running configs.
        for rc in steps:
            # Append a running config to the RCs list.
            if isinstance(rc, str):
                RCs.append(RunningConfig(uses=rc))
            elif isinstance(rc, dict):
                RCs.append(RunningConfig(**rc))
            else:
                raise ValueError(f"Invalid running config: {rc}")
        return RCs

    @staticmethod
    def get_pipelines(task: TaskConfig) -> Pipelines:
        """
        Get the list of pipelines for a task

        Args:
            task: The task to get the pipelines for

        Returns:
            A list of PipelineConfig objects
        """
        task.pipelines = task.pipelines or []
        pipelines: Pipelines = [
            PipelineConfig(**task.__dict__[name])
            for name in task.pipelines
            if name in task.__dict__ and isinstance(task.__dict__[name], dict)
        ]
        return pipelines

    @staticmethod
    def run_task(task: TaskConfig, project: Optional[ProjectConfig] = None):
        """
        Run pipelines specified in the task

        Args:
            task: TaskConfig to run pipelines for
            project: ProjectConfig to run pipelines
        """
        # Set project to the project.
        if project:
            task.project = project
        # Run all pipelines in the pipeline.
        for pipeline in PIPELINEs.get_pipelines(task):
            if task.verbose:
                logger.info("Running pipeline: %s", pipeline.dict())
            initial_object = task if pipeline.use_task_as_initial_object else None
            PIPELINEs.run_pipeline(pipeline, initial_object, task)

    @staticmethod
    def run_workflow(workflow: WorkflowConfig):
        """
        Run the tasks specified in the workflow

        Args:
            workflow: WorkflowConfig object to run
        """
        # Run all tasks in the workflow.
        for task in workflow.get_tasks():
            # Run the task if verbose is true.
            if workflow.verbose:
                logger.info("Running task: %s", task.task_name)
            PIPELINEs.run_task(task, project=workflow.project)
