from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from hyfi.batch import BatchConfig
from hyfi.composer.extended import XC
from hyfi.task import TaskConfig
from hyfi.utils.logging import LOGGING

logger = LOGGING.getLogger(__name__)


class BatchTaskConfig(TaskConfig):
    _config_name_: str = "__batch__"
    _config_group_: str = "task"

    batch_name: str = "demo"
    batch: BatchConfig = None  # type: ignore

    class Config:
        property_set_methods = {
            "task_name": "set_task_name",
            "task_root": "set_task_root",
            "batch_name": "set_batch_name",
            "batch_num": "set_batch_num",
        }

    def set_batch_name(self, val):
        self.initialize_configs(batch_name=val)

    def set_batch_num(self, val):
        self.batch.batch_num = val

    def initialize_configs(self, **config_kwargs):
        super().initialize_configs(**config_kwargs)
        subconfigs = {
            "batch": BatchConfig,
        }
        self.initialize_subconfigs(subconfigs, **config_kwargs)
        logger.info(
            "Initalized batch: %s(%s) in %s",
            self.batch_name,
            self.batch_num,
            self.batch_dir,
        )

    @property
    def batch_num(self):
        return self.batch.batch_num

    @property
    def seed(self):
        return self.batch.seed

    @property
    def batch_dir(self):
        return self.batch.batch_dir

    @property
    def device(self):
        return self.batch.device

    @property
    def num_devices(self):
        return self.batch.num_devices

    def save_config(
        self,
        filepath: Optional[Union[str, Path]] = None,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
        save_as_json_as_well: bool = True,
    ) -> str:
        """
        Save the batch configuration to file.

        Args:
            filepath (Optional[Union[str, Path]]): The filepath to save the configuration to. Defaults to None.
            exclude (Optional[Union[str, List[str], Set[str], None]]): Keys to exclude from the saved configuration.
                Defaults to None.
            exclude_none (bool): Whether to exclude keys with None values from the saved configuration. Defaults to True.
            only_include (Optional[Union[str, List[str], Set[str], None]]): Keys to include in the saved configuration.
                Defaults to None.
            save_as_json_as_well (bool): Whether to save the configuration as a json file as well. Defaults to True.

        Returns:
            str: The filename of the saved configuration.
        """
        if not filepath:
            filepath = self.batch.config_filepath

        if save_as_json_as_well:
            self.save_config_as_json(
                exclude=exclude,
                exclude_none=exclude_none,
                only_include=only_include,
            )
        return super().save_config(
            filepath=filepath,
            exclude=exclude,
            exclude_none=exclude_none,
            only_include=only_include,
        )

    def save_config_as_json(
        self,
        filepath: Optional[Union[str, Path]] = None,
        exclude: Optional[Union[str, List[str], Set[str], None]] = None,
        exclude_none: bool = True,
        only_include: Optional[Union[str, List[str], Set[str], None]] = None,
    ) -> str:
        if not filepath:
            filepath = self.batch.config_jsonpath
        return super().save_config_as_json(
            filepath=filepath,
            exclude=exclude,
            exclude_none=exclude_none,
            only_include=only_include,
        )

    def load_config(
        self,
        batch_name: Optional[str] = None,
        batch_num: Optional[int] = None,
        filepath: Optional[Union[str, Path]] = None,
        **config_kwargs,
    ) -> Dict:
        """Load the config from the batch config file"""
        if not batch_name:
            batch_name = self.batch_name
        if batch_num is None:
            batch_num = -1
        if not filepath and batch_num >= 0:
            batch = BatchConfig(
                batch_root=self.batch.batch_root,
                batch_name=batch_name,
                batch_num=batch_num,
            )
            filepath = batch.config_filepath
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if self.verbose:
            logger.info(
                "> Loading config for batch_name: %s batch_num: %s",
                batch_name,
                batch_num,
            )
        cfg = self.export_config()
        if filepath:
            if filepath.is_file():
                logger.info("Loading config from %s", filepath)
                batch_cfg = XC.load(filepath)
                logger.info("Merging config with the loaded config")
                cfg = XC.merge(cfg, batch_cfg)
            else:
                logger.info("No config file found at %s", filepath)
        if self.verbose:
            logger.info("Updating config with config_kwargs: %s", config_kwargs)
        cfg = XC.update(XC.to_dict(cfg), config_kwargs)

        self.initialize_configs(**cfg)

        return self.__dict__

    def print_config(
        self,
        batch_name: Optional[str] = None,
        batch_num: Optional[int] = None,
    ):
        self.load_config(batch_name, batch_num)
        XC.print(self.dict())
