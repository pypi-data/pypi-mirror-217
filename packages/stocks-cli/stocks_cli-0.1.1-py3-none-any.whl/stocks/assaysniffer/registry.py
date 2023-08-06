# -*- coding: utf-8 -*-
import logging
import os
import sys
from importlib import import_module
from pathlib import Path
from typing import Type, Iterable, List, Set, Optional

from stocks.assaysniffer import AssaySniffer

logger = logging.getLogger("AssaySnifferRegistry")


class AssaySnifferRegistry:
    """A registry for `Assay Sniffer` classes."""

    def __init__(self):
        self._sniffers = {}

    def install(self, sniffer_cls: Type[AssaySniffer]):
        """
        Install a sniffer class in the registry dict. The class.__name__ is used as a key for easy lookup.
        Can be used as a decorator or called directly:

            registry = AssaySnifferRegistry()
            @registry.install
            class IlluminaSniffer(AssaySniffer):
                ...

            registry.install(IlluminaSniffer)
        """
        logger.debug(sniffer_cls.__name__)
        self._sniffers[sniffer_cls.__name__] = sniffer_cls
        return sniffer_cls

    def get_sniffers(self) -> List[Type[AssaySniffer]]:
        """
        Get the list of registered AssaySniffer classes
        :return: the list of registered AssaySniffer classes
        """
        return list(self._sniffers.values())

    def get_sniffer(self, name) -> Optional[Type[AssaySniffer]]:
        """
        Look up registered AssaySniffer classes by name
        :param name: the look up name i.e. class.__name__
        :return: the registered AssaySniffer class
        """
        if name in self._sniffers:
            return self._sniffers[name]
        return None

    def get_sniffer_instance(self, name) -> Optional[AssaySniffer]:
        """
        Get an instance of a registered AssaySniffer class by class name
        :param name: the look up name i.e. class.__name__
        :return: an instance of the registered AssaySniffer class or None
        """
        if name in self._sniffers:
            return self._sniffers[name]()
        return None

    def get_registered_sniffer_names(self) -> Set[str]:
        """
        Get the set of registered AssaySniffer class names
        :return:
        """
        return set(self._sniffers.keys())

    @staticmethod
    def load_custom_plugins(plugin_dirs: Iterable) -> None:
        """
        Loads each dir_path as a module.
        :param plugin_dirs:
        :return:
        """
        logger.debug(f"Got plugin directories: {plugin_dirs}")
        for plugin_dir in plugin_dirs:
            plugin = os.path.basename(plugin_dir)
            try:
                logger.debug(f"Trying to load plugin: {plugin}")
                import_module(plugin)
            except ModuleNotFoundError:
                # The only way to avoid this bad behavior (modifying sys.path) would be to install the plugins using
                # setuptools/pip. One cannot import modules from parent directories.
                logger.debug(f"Adding '{plugin_dir}' to PYTHONPATH and trying to load plugin: {plugin}")
                sys.path.append(plugin_dir)
                sys.path.append(os.path.dirname(plugin_dir))
                import_module(plugin)

    @classmethod
    def load_custom_plugins_from_plugin_base_dir(cls, base_dir: Path) -> None:
        """
        Finds direct subdirs that contains __init__.py and loads them
        """
        discovered_modules: List[str] = []
        for path in base_dir.iterdir():
            if path.is_dir() and Path(path, "__init__.py").exists():
                discovered_modules.append(str(path))

        if len(discovered_modules) > 0:
            cls.load_custom_plugins(discovered_modules)


registry = AssaySnifferRegistry()
