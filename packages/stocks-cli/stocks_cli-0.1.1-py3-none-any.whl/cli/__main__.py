import logging
from enum import Enum
from typing import Optional
import typer
from cli import config, export, fetch, register, __app_name__, __version__

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# The main app
app = typer.Typer()
# app the different module, each one file in the cli package
app.add_typer(config.app, name="config")
app.add_typer(export.app, name="export")
app.add_typer(fetch.app, name="fetch")
app.add_typer(register.app, name="register")


# a method to print version and exit directly
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


# define the eager option --version, on the global app
@app.callback()
def add_version_callback(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return

@app.callback()
def add_verbose_callback(
        log_level: LogLevel = typer.Option(
            "WARNING",
            "--log-level",
            case_sensitive=False,
            help="Sets the verbose level")
) -> None:
    logging.basicConfig(
        level=str(log_level.value),
        #format='%(levelname)-8s  %(name)-23s  %(message)s'
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def main():
    app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
