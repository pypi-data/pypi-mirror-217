# -*- coding: utf-8 -*-
"""
The 'config' module of the CLI
"""

import getpass
import logging
import os
import stat
from pathlib import PosixPath, Path
from typing import Any, Dict

import typer
import yaml

from cli import __app_name__, get_default_config_file_path, get_default_stocks_api_url
from stocks.models import User
from stocksapi.client import StocksClient
from stocksapi.manager import StocksManager
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)

# name of this module (as appearing on the command line) is the last part of the __name__ e.g. cli.config -> config
_MODULE_NAME = __name__.rsplit(".", 1)[-1]
# list of command names offered in this module
_CMD_SHOW = "show"
_CMD_SETUP = "setup"
_CMD_CLEAN = "clean"
_CMD_SWITCH = "switch"
_CMD_REFRESH = "refresh"

# create the CLI app
app = typer.Typer()


@app.command(_CMD_CLEAN)
def clean(
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    wipe the config file
    """
    conf_file: PosixPath = PosixPath(conf_file_path)
    conf_file.unlink(missing_ok=True)


@app.command(_CMD_SHOW)
def show(
        verbose: bool = typer.Option(
            True,
            "--verbose/--brief",
            help="Show extensive information about your account"
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Show current configuration information
    """
    conf_file: PosixPath = PosixPath(conf_file_path)
    _config = get_config(conf_file)
    _username: str = _config[_config["default"]]["username"]

    print(f"Configurations defined in  {str(conf_file)}")
    print(f"Available configurations : {os.linesep}")
    print(yaml.dump(_config))

    print(f"Currently using: {_config['default']} with {_username}")

    try:
        if verbose:
            client: StocksClient = StocksClient(_config)
            stocks_manager: StocksManager = StocksManager(client)
            # list groups & dropboxes
            me: User = stocks_manager.fetch_user(_username)
            if me.groups:
                print(f"You belong to the following groups:")
                for g in me.groups.values():
                    print(f"- {g.name} [Primary Group: {g.is_primary_group}]")
            else:
                print("!!! Warning: No dropboxes are currently defined for this account. "
                      "Please contact your admin to set this up.")

            # list dropboxes
            dropboxes: dict[str, str] = stocks_manager.list_dropboxes()
            if dropboxes:
                print(f"Available dropboxes for {_username}:")
                for k, v in dropboxes.items():
                    print(f"- Group: {k} -> Dropbox: {v}")
            else:
                print("!!! Warning: No dropboxes are currently defined for this account."
                      " Please contact your admin to set this up.")
    except ConnectionError:
        logger.warning("The server seems down and more info cannot be fetched")


@app.command(_CMD_SWITCH)
def switch(
        stocks_url: str = typer.Option(
            ...,
            "--stocks-api-url",
            prompt="STOCKS API URL?",
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Switch the server to connect
    """
    conf_file: PosixPath = PosixPath(conf_file_path)
    current_config = get_config(conf_file)
    stocks_url = stocks_url.strip()
    if stocks_url in current_config:
        current_config["default"] = stocks_url
        update_config(current_config, conf_file)
    else:
        raise typer.BadParameter(
            message=f"'{stocks_url}' does not match any of the registered URLs in your config.",
            param_hint="--stocks-api-url"
        )


@app.command(_CMD_REFRESH, help="Refresh the login token of the default connection")
def refresh(
        stocks_pwd: str = typer.Option(
            ...,
            "--stocks_pwd",
            prompt="STOCKS username pwd to use?",
            hide_input=True,
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    When token has expired, refresh the login
    """
    conf_file: PosixPath = PosixPath(conf_file_path)
    config: Dict = get_config(conf_file)
    stocks_url = config["default"]
    # connect stocks api to get a token
    client: StocksClient = StocksClient(config)
    client.authenticate(stocks_pwd)
    # save the token in config
    logger.debug("Got token: %s", client.token)
    config[stocks_url]["token"] = client.token
    update_config(config, conf_file)


@app.command(_CMD_SETUP)
def setup(
        stocks_url: str = typer.Option(
            get_default_stocks_api_url(),
            "--stocks-api-url",
            prompt="STOCKS API URL?",
        ),
        stocks_user: str = typer.Option(
            str(getpass.getuser()),
            "--stocks-user",
            prompt="STOCKS username to use?",
        ),
        stocks_pwd: str = typer.Option(
            ...,
            "--stocks-pwd",
            prompt="STOCKS username pwd to use?",
            hide_input=True,
        ),
        unix_group: str = typer.Option(
            ...,
            "--group-name",
            prompt="What is your unix primary group_name?"
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Set up a configuration file containing important STOCKS connection parameters and
    other information. A first authentication is done and your personal token stored.
    """
    stocks_url = stocks_url.strip()
    if not stocks_url.startswith("http"):
        raise typer.BadParameter(
            message=f"'{stocks_url}' is not a valid URL; URL must start with http or https e.g. http://{stocks_url}",
            param_hint="--stocks-api-url"
        )

    conf_file: PosixPath = PosixPath(conf_file_path)
    config: Dict = setup_config(conf_file, stocks_url, stocks_user, unix_group)
    # connect stocks api to get a token
    client: StocksClient = StocksClient(config)
    client.authenticate(stocks_pwd)
    # save the token in config
    logger.debug("Got token: %s", client.token)
    config[stocks_url]["token"] = client.token
    update_config(config, conf_file)


def get_config(config_path: Path) -> Any:
    """
    :type config_path: Union[str, Path]
    :param config_path: location of config yaml file
    :return:
    """
    if not config_path.exists():
        mess: str = f"'{config_path}' does not exist, please run '{__app_name__} {_MODULE_NAME} {_CMD_SETUP}' first"
        # logger.critical(mess)
        typer.echo(mess, err=True)
        raise typer.Exit(1)

    with open(str(config_path)) as c:
        return yaml.safe_load(c)


def setup_config(config_path: PosixPath, url: str, username: str, unix_group: str) -> Any:
    """
    Set up the config based on the parameters given and the possibly already
    existing config file.
    :param config_path:
    :param url:
    :param username:
    :param unix_group: the user's unix group ie not the STOCKS' group name
    :return:
    """
    if config_path.exists():
        config = get_config(config_path)
    else:
        # use a default setup
        config = {
            "default": url,
            url: {
                "username": username,
                "unix_group": unix_group
            }
        }

    # update
    config["default"] = url
    if url not in config:
        config[url] = {
            "username": username,
        }

    if username and username != config[url]["username"]:
        config[url]["username"] = username
        config[url].pop("token", None)

    if unix_group:
        config[url]["unix_group"] = unix_group

    update_config(config, config_path)
    return config


def update_config(config_content, config_path: PosixPath):
    """
    Update (or create if missing) a config file with current configuration
    :param config_content:
    :param config_path:
    :return:
    """
    logger.info(config_content)
    # check all parent dirs exist, make sure only owner can read this
    config_path.parent.mkdir(parents=True, exist_ok=True, mode=stat.S_IRWXU)
    # write
    with open(config_path, "w") as c:
        yaml.dump(config_content, c)
        c.close()
    #  make sure only owner can read this config file as it contains a login token
    os.chmod(config_path, mode=stat.S_IRWXU)
