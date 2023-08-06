from pathlib import Path
import sys
import os
from typing import List

import typer
import getpass
import configparser

# user calling cmd line
CURRENT_USERNAME = getpass.getuser()

# global name and version for the STOCKS CLI app
__app_name__ = "stocks"
__version__ = "1.0.0"


#######################################
# Common option values
########################################


##############################################
# Configuration global ie users defaults
#############################################
FILE_DIR = Path(__file__).parent

_GLOBAL_CONFIG_FILE_NAME = os.path.join(FILE_DIR, 'stockscli.ini')

# options found in the global config file
_CONFIG_SECTION_STOCKS = 'stocks'
_CONFIG_OPTION_STOCKS_API_URL = 'api_url'
_CONFIG_OPTION_STOCKS_SNIFFER_PLUGIN_DIRS = 'sniffer_plugin_dirs'

_CONFIG_SECTION_MAIL = 'mail'
_CONFIG_OPTION_MAIL_HOST = 'host'
_CONFIG_OPTION_MAIL_SMTP = 'smtp'

_CONFIG_SECTION_ADMIN = 'admin'
_CONFIG_OPTION_ADMIN_NAME = 'name'
_CONFIG_OPTION_ADMIN_EMAIL = 'mail'

_CONFIG_SECTION_MAGETAB = 'magetab'
_CONFIG_OPTION_MAGETAB_LASTNAME = 'submitter_lastname'
_CONFIG_OPTION_MAGETAB_MIDDLENAME = 'submitter_middlename'
_CONFIG_OPTION_MAGETAB_FIRSTNAME = 'submitter_firstname'
_CONFIG_OPTION_MAGETAB_EMAIL = 'submitter_email'
_CONFIG_OPTION_MAGETAB_AFFILIATION = 'default_affiliation'

_CONFIG_SECTION_INSTITUTION = 'institution'
_CONFIG_OPTION_DEFAULT_INSTITUTION = 'default_institution'

config_parser = configparser.ConfigParser()
here: Path = Path(__file__).parent.resolve()
_conf_file_path: Path = Path(here.parent, _GLOBAL_CONFIG_FILE_NAME)

if not _conf_file_path.exists():
    typer.echo(f"Could not find the global config file ({_GLOBAL_CONFIG_FILE_NAME}): {str(_conf_file_path)}")
    sys.exit(1)

# read up default config
config_parser.read(_conf_file_path)

############################################
# User specific setup
# where to save configs by default ; this is :
#   - /Users/<user>/Library/Application\ Support/watchdog/ on mac
#   - /home/user/.config/watchdog/ on ubuntu ...
###########################################
_DEFAULT_CONFIG_DIR_PATH = Path(typer.get_app_dir(app_name=__app_name__, force_posix=True))
# default name of the config file
_DEFAULT_CONFIG_FILE_PATH: Path = _DEFAULT_CONFIG_DIR_PATH / "stocksapi.yml"


def get_sniffer_plugin_dir_list() -> List[Path]:
    """
    read the list of registered sniffer plugin dirs from the config file
    :return: a list of Path or an empty list
    """
    path_list: List[Path] = []
    value: str = config_parser.get(_CONFIG_SECTION_STOCKS, _CONFIG_OPTION_STOCKS_SNIFFER_PLUGIN_DIRS)
    if not value:
        return path_list

    for p in value.split(sep=","):
        plugin_dir_path: Path = Path(p)
        if plugin_dir_path.exists() and plugin_dir_path.is_dir():
            path_list.append(plugin_dir_path)

    return path_list


def get_default_config_file_path() -> Path:
    """
    Show current configuration information
    """
    return _DEFAULT_CONFIG_FILE_PATH


def get_default_stocks_api_url() -> str:
    """
    :return: the default STOCKS API URL
    """
    return config_parser.get(_CONFIG_SECTION_STOCKS, _CONFIG_OPTION_STOCKS_API_URL)

def get_default_mail_host() -> str:
    return config_parser.get(_CONFIG_SECTION_MAIL, _CONFIG_OPTION_MAIL_HOST)

def get_default_mail_smtp() -> str:
    return config_parser.get(_CONFIG_SECTION_MAIL, _CONFIG_OPTION_MAIL_SMTP)

def get_default_admin_name() -> str:
    return config_parser.get(_CONFIG_SECTION_ADMIN, _CONFIG_OPTION_ADMIN_NAME)

def get_default_admin_email() -> str:
    return config_parser.get(_CONFIG_SECTION_ADMIN, _CONFIG_OPTION_ADMIN_EMAIL)

def get_default_submitter_lastname() -> str:
    return config_parser.get(_CONFIG_SECTION_MAGETAB, _CONFIG_OPTION_MAGETAB_LASTNAME)

def get_default_submitter_middlename() -> str:
    return config_parser.get(_CONFIG_SECTION_MAGETAB, _CONFIG_OPTION_MAGETAB_MIDDLENAME)

def get_default_submitter_firstname() -> str:
    return config_parser.get(_CONFIG_SECTION_MAGETAB, _CONFIG_OPTION_MAGETAB_FIRSTNAME)

def get_default_submitter_email() -> str:
    return config_parser.get(_CONFIG_SECTION_MAGETAB, _CONFIG_OPTION_MAGETAB_EMAIL)

def get_default_affiliation() -> str:
    return config_parser.get(_CONFIG_SECTION_INSTITUTION, _CONFIG_OPTION_DEFAULT_INSTITUTION)
