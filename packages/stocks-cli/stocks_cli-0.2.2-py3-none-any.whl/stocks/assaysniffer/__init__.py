from abc import ABC, abstractmethod
from typing import List, Any, Optional
from pathlib import Path
import logging

from stocks.models import InstrumentRun
from cli.utils import Technology

logger = logging.getLogger(__name__)

def check_valid_directory(path: Path) -> bool:
    if not path or not path.exists() or not path.is_dir():
        return False
    return True


class AssaySniffer(ABC):
    """
    An AssaySniffer is responsible to parse run folders and extract Assay and Dataset description corresponding
    to one or many InstrumentRun.
    """

    @classmethod
    @abstractmethod
    def get_supported_technology(cls) -> Technology:
        """
        :return: the technology this sniffer supports
        """
        pass

    @classmethod
    @abstractmethod
    def get_supported_platforms(cls) -> List[str]:
        """
        :return: platforms: the list of Platform this sniffer supports or None if the sniffer is
        not platform specific. Please use all UPPERCASE eg NANOPORE, ILLUMINA ...
        """
        pass

    @classmethod
    @abstractmethod
    def is_multi_run_sniffer(cls) -> bool:
        """
        Tells if the sniffer can sniff more than one run.
        :return: true if more than one instrument run can be sniffed by this sniffer
        """
        pass

    @classmethod
    @abstractmethod
    def get_sniffer_description(cls) -> str:
        """
        Describes how this assay sniffer works i.e. what (meta)data is extracted
        :return: a string explaining what the plugin expects to find / is looking for
        """
        pass

    def is_sniffer_valid_for(self, technology: Technology, platform: str | None = None,
                             enforce_platform_match: bool = False) -> bool:
        """
        checks if this sniffer can be used for a given Technology and, optionally, a specific platform.
        The platform filtering only happens if a valid platform name is given.
        When a platform is given, a sniffer of requested technology that does not restrict on specific platform is
        considered valid unless enforce_platform_match is True
        considered valid
        :param technology: the techonology for which you need a sniffer
        :param platform: an optional platform
        :param enforce_platform_match: if true, sniffer that do not explicitly list the requested platform are
        not considered valid
        """
        res: bool = technology == self.get_supported_technology()
        if res and platform:
            if self.get_supported_platforms():
                # if the sniffer defines platforms, we anyway do the filtering
                res = platform.upper() in self.get_supported_platforms()
            elif enforce_platform_match:
                res = False
        return res

    @abstractmethod
    def sniff_instrument_run_assays(self, dir_path: Path, group: str, username: Optional[str] = None) \
            -> List[InstrumentRun]:
        """
        Main method to parse the content of a directory in a list of assay objects.

        :param dir_path: the path to the directory to sniff
        :param group: the unix group_name considered to be the owner of the dir_path content
        :param username: an optional username to use as data owner
        :return the list of discovered Assay
        :except : AssayStructureError if the dir_path structure does not match sniffer's expectations
        """
        pass


class JSONAssaySniffer(AssaySniffer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def get_json_schema(self, technology: Technology, platform: str) -> Any:
        """
        Returns the JSON schema this sniffer uses for the technology and platform.
        """
        pass
