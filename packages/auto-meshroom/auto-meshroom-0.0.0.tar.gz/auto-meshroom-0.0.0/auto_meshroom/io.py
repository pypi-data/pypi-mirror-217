# io.py

from typing import Optional, List
import zipfile
import requests
import shutil
import os
from pathlib import Path
import subprocess
import warnings

from spinneroo import Spinner

from auto_meshroom.exceptions import (
    AliceVisionFailError, DirectoryNotEmptyWarning
)
from auto_meshroom.base import (
    source, scripts, MESHROOM_SOURCE, MESHROOM_URL,
    MESHROOM_NAME
)

__all__ = [
    "execute",
    "check_content",
    "remove_content",
    "build_directory",
    "build_scripts"
]

def execute(command: str, process: Optional[str] = None) -> str:
    """
    Runs string commands in the command line.

    :param command: The string command to run in the command line
    :param process: The name of the process.

    :return: str: The returned string from the process
    """

    try:
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT
        )

    except subprocess.CalledProcessError:
        raise AliceVisionFailError(
            command=command, process=process
        )
    # end try
# end execute

def check_content(path: str) -> List[str]:
    """
    Removes all files and directories inside the path.

    :param path: The path to remove its content.
    """

    if os.path.isdir(path) and len(paths := os.listdir(path)) > 0:
        return paths
    # end if

    return []
# end _remove_content

def remove_content(path: str) -> None:
    """
    Removes all files and directories inside the path.

    :param path: The path to remove its content.
    """

    if os.path.isfile(path):
        os.remove(path)

    elif os.path.isdir(path):
        for sub_path in os.listdir(path):
            remove_content(os.path.join(path, sub_path))

            try:
                shutil.rmtree(os.path.join(path, sub_path))

            except FileNotFoundError:
                continue
            # end try
        # end for
    # end if
# end remove_content

def build_directory(path: str, override: Optional[bool] = False) -> None:
    """
    Creates the directory by its name.

    :param path: The directory to create.
    :param override: The value to remove the content of the directory.
    """

    try:
        if path is not None:
            os.makedirs(path, exist_ok=True)
        # end if

    except FileExistsError:
        if override:
            remove_content(path)

        elif paths := check_content(path):
            warnings.warn(
                DirectoryNotEmptyWarning(path=path, paths=paths)
            )
        # end if
    # end try
# end build_directory

def build_scripts(
        path: Optional[str] = None, progress: Optional[bool] = None
) -> str:
    """
    Builds the source directory.

    :param path: The directory in with the source will be saved.
    :param progress: The value to silence the destination
    """

    path = path or source()

    scripts_location = str(Path(path) / Path(MESHROOM_NAME))
    scripts_path = str(Path(path) / Path(MESHROOM_SOURCE))

    if os.path.exists(scripts_path):
        return scripts()

    else:
        with Spinner(
            title="Building Source",
            message=f"Downloading source data from {MESHROOM_URL}",
            silence=not progress, counter=True,
            complete="Downloading complete"
        ):
            response = requests.get(MESHROOM_URL, allow_redirects=True)
        # end Spinner

        os.makedirs(path, exist_ok=True)

        with Spinner(
            title="Building Source",
            message=f"Writing source data to: {scripts_path}",
            silence=not progress, counter=True,
            complete="Downloading complete"
        ):
            with open(scripts_path, 'wb') as zip_file:
                zip_file.write(response.content)
            # end open
        # end Spinner

        if progress:
            print("Downloading Complete.")
        # end if
    # end if

    with Spinner(
        title="Building Source",
        message=f"Extracting Binaries to: {scripts_location}",
        silence=not progress, counter=True,
        complete="Downloading complete"
    ):
        with zipfile.ZipFile(scripts_path, 'r') as zip_file:
            zip_file.extractall(f"{path}\\")
        # end open
    # end Spinner

    if progress:
        print("Extraction Complete.")
    # end if

    return scripts()
# end build_scripts