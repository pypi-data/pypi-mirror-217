# base.py

import os
from pathlib import Path

__all__ = [
    "MESHROOM_VERSION",
    "MESHROOM_NAME",
    "MESHROOM_SOURCE",
    "MESHROOM_URL",
    "root",
    "source",
    "assets",
    "scripts",
    "dependencies"
]

MESHROOM_VERSION = "2018.1.0"
MESHROOM_NAME = f"Meshroom-{MESHROOM_VERSION}"
MESHROOM_SOURCE = f"{MESHROOM_NAME}-win64.zip"
MESHROOM_URL = (
    f"https://github.com/alicevision/meshroom/releases/"
    f"download/v{MESHROOM_VERSION}/{MESHROOM_SOURCE}"
)

def root() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    try:
        if os.getcwd() in os.environ['VIRTUAL_ENV']:
            path = Path(__file__).parent

        else:
            raise KeyError
        # end if

    except KeyError:
        if os.getcwd() not in (
            path := str(Path(__file__).parent)
        ):
            path = os.getcwd()
        # end if
    # end try

    return str(path)
# end root

def source() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(root()) / Path("source"))
# end source

def dependencies() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(source()) / Path("dependencies"))
# end dependencies

def scripts() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(source()) / Path(f"{MESHROOM_NAME}\\aliceVision\\bin"))
# end scripts

def assets() -> str:
    """
    Returns the root of the source program.

    :return: The path to the source.
    """

    return str(Path(source()) / Path("assets"))
# end assets