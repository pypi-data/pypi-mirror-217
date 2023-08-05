# modeling.py

import warnings
from pathlib import Path
import shutil
from typing import (
    List, Callable, Optional, Type, Union, Generator
)
import tqdm
import os
import tempfile
from datetime import datetime
from colorama import Fore

from represent import BaseModel

from auto_meshroom.io import (
    execute, build_directory,
    build_scripts, remove_content
)
from auto_meshroom.base import scripts, MESHROOM_SOURCE, MESHROOM_NAME
from auto_meshroom.mesh import Mesh
from auto_meshroom.commands import CommandsGenerator

__all__ = [
    "Modeler",
    "render"
]

def process_name(method: Callable) -> str:
    """
    Returns the name of the method as a process title.

    :param method: The method to get its name.

    :return: The title of the process of the method.
    """

    return method.__name__.replace("_", " ").replace("  ", "").title()
# end process_name

class Modeler(BaseModel):
    """
    An object to create CAD model using images of the object.

    An instance of this class can be used to run an operation of
    creating a 3D model of an object, using a set of images of
    the object, taken by a camera.

    This class uses the Meshroom technology of AliveVision, automatically.
    Can be used as a module, object, function or in the command line.

    The constractor parameters:

    - destination:
        The destination directory in which to save the result files.

    - source:
        The path to the directory of the source images of an object to 3D model,
        taken by a digital camera.

    - override:
        The value to override existing files and directories, if their names
        are given for destination, source and output.

    - group_size:
        The amount of images to include in each image group,
        for the modeling process.

    - color:
        The value to add a colored texture to the 3D model.

    - model:
        The mesh object or class for the results object.

    - path:
        The path to the source scripts of meshroom.

    - progress:
        The value to show the output of the process.

    - output:
        The path to a directory in which the building process
        will be taking place, as saved files and directories.

    >>> from auto_meshroom import Modeler
    >>>
    >>> modeler = Modeler(
    >>>     source="datasets/lion",
    >>>     destination='results/lion',
    >>>     color=True,
    >>>     progress=True
    >>> )
    >>>
    >>> mesh = modeler.render()
    """

    COLOR = False

    MESH_NAME = CommandsGenerator.MESH_NAME
    GROUP_SIZE = CommandsGenerator.GROUP_SIZE

    def __init__(
            self,
            destination: Optional[str] = None,
            source: Optional[str] = None,
            override: Optional[bool] = False,
            group_size: Optional[int] = None,
            color: Optional[bool] = None,
            model: Optional[Union[Mesh, Type[Mesh]]] = None,
            path: Optional[str] = None,
            progress: Optional[bool] = True,
            output: Optional[str] = None,
            name: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes for the process.

        :param destination: The destination directory to save the process in.
        :param source: The directory of the input images of the object.
        :param group_size: The number of images to include in a group.
        :param color: The value to add the texture to the model.
        :param path: The source directory path.
        :param model: The results object to obtain the process data.
        :param override: The value to remove existing content from the directories.
        :param progress: The value to silence the destination
        :param output: The output directory.
        :param name: The name of the mesh file.
        """

        self._commands: List[Callable[[], None]] = []
        self._commands_names: List[str] = []

        self._path = None
        self._model = None

        self.models: List[Mesh] = []

        self.command_generator: Optional[CommandsGenerator] = None

        self.images_count: Optional[int] = None
        self.group_size: Optional[int] = None

        self.override: Optional[bool] = None
        self.progress: Optional[bool] = None
        self.color: Optional[bool] = None

        self.output: Optional[str] = None
        self.destination: Optional[str] = None
        self.source: Optional[str] = None
        self.name: Optional[str] = None

        self.initialize(
            destination=destination, source=source,
            path=path, group_size=group_size or self.GROUP_SIZE,
            override=override, color=color or self.COLOR,
            model=model, progress=progress, output=output,
            name=name or self.MESH_NAME
        )
    # end __init__

    @property
    def model(self) -> Mesh:
        """
        Returns the id of the result object.

        :return: The result object
        """

        return self._model
    # end model

    @model.setter
    def model(self, mesh: Mesh) -> None:
        """
        Sets the id of the result object.

        :param mesh: The result object
        """

        mesh = mesh or Mesh

        if issubclass(mesh, Mesh) or (mesh == Mesh):
            mesh: Type[Mesh]

            self._model = mesh(
                source=self.source,
                destination=self.destination,
                color=self.color
            )

        elif isinstance(mesh, Mesh):
            self._model = mesh

        else:
            raise TypeError(
                f"model must be an instance or a "
                f"subclass of '{Mesh}', not '{type(mesh)}'."
            )
        # end

        if self.model not in self.models:
            self.models.append(self.model)
        # end if
    # end model

    @property
    def path(self) -> str:
        """
        Returns the location path of the bin source files.

        :return: The path to the bin folder.
        """

        return self._path
    # end bin_path

    @path.setter
    def path(self, p: str) -> None:
        """
        Returns the location path of the bin source files.

        :return: The path to the bin folder.
        """

        if os.path.exists(p):
            for file in [
                str(Path(p) / Path(MESHROOM_NAME)),
                str(Path(p) / Path(MESHROOM_SOURCE))
            ]:
                if not os.path.exists(file):
                    raise FileNotFoundError(
                        f"'{MESHROOM_NAME}' must exist in "
                        f"the path directory '{p}'."
                    )
                # end if
            # end for

            self._path = p

            if isinstance(self.command_generator, CommandsGenerator):
                self.command_generator.path = p
            # end if

        else:
            raise FileNotFoundError(
                f"{p} must be a valid path to "
                f"meshroom source scripts."
            )
        # end if
    # end bin_path

    @property
    def commands(self) -> list:
        """
        Returns the location path of the bin source files.

        :return: The path to the bin folder.
        """

        return self._commands[:]
    # end commands

    @property
    def commands_names(self) -> list:
        """
        Returns the location path of the bin source files.

        :return: The path to the bin folder.
        """

        return self._commands_names[:]
    # end commands_names

    def initialize(
            self,
            destination: str,
            source: str,
            group_size: Optional[int] = None,
            path: Optional[str] = None,
            color: Optional[bool] = None,
            override: Optional[bool] = False,
            model: Optional[Mesh] = None,
            progress: Optional[bool] = True,
            output: Optional[str] = None,
            name: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes for the process.

        :param destination: The destination directory to save the process in.
        :param source: The directory of the input images of the object.
        :param group_size: The number of images to include in a group.
        :param color: The value to add the texture to the model.
        :param path: The source directory path.
        :param model: The results object to obtain the process data.
        :param override: The value to remove existing content from the directories.
        :param progress: The value to silence the destination.
        :param output: The output directory.
        :param name: The name of the mesh file.
        """

        if output is None:
            with tempfile.TemporaryDirectory() as directory:
                output = str(Path(directory)) + "/"
            # end TemporaryDirectory

        else:
            output = (output + "/").replace("//", "/")
        # end if

        self.group_size = group_size or self.group_size

        self.color = color or self.color
        self.override = override
        self.progress = progress

        self.destination = destination or self.destination
        self.source = source or self.source
        self.output = output
        self.name = name or self.name

        self.model = model

        build_directory(self.output, self.override)

        self.path = build_scripts(path=path or self.path, progress=progress)

        self.images_count = len(os.listdir(self.source))

        self.command_generator = CommandsGenerator(
            output=self.output, source=self.source, path=self.path,
            images_count=self.images_count, name=self.name
        )

        self._commands[:] = [
            self.camera_initialization, self.features_extraction,
            self.images_matching, self.features_matching,
            self.structure_from_motion_building, self.dense_scene_preparation,
            self.camera_connection, self.depth_mapping,
            self.depth_map_filtering, self.meshing, self.mesh_filtering
        ]
        self._commands_names[:] = [
            process_name(method) for method in self._commands
        ]

        if self.color:
            self._commands.append(self.texturing)
            self._commands_names.append(process_name(self.texturing))
        # end if
    # end initialize_model

    def _execute(self, command: Callable[[], str]) -> None:
        """
        Executes the command from the function to return the string to run.

        :param command: The function to call and get the command string from.
        """

        build_directory(self.output + command.__name__, self.override)

        execute(command(), process=process_name(command))
    # end _execute

    def camera_initialization(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.camera_initialization)
    # end camera_initialization

    def features_extraction(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.features_extraction)
    # end features_extraction

    def images_matching(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.images_matching)
    # end images_matching

    def features_matching(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.features_matching)
    # end features_matching

    def structure_from_motion_building(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.structure_from_motion_building)
    # end structure_from_motion_building

    def dense_scene_preparation(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.dense_scene_preparation)
    # end dense_scene_preparation

    def camera_connection(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.camera_connection)
    # end camera_connection

    def depth_mapping(self) -> None:
        """Runs the process in the command line."""

        build_directory(
            self.output + self.command_generator.depth_mapping.__name__,
            self.override
        )

        commands = self.command_generator.depth_mapping_groups()

        commands_iter = tqdm.tqdm(
            commands, leave=True,
            desc="(8.0) Depth Mapping of Images Groups",
            bar_format=(
                (
                    "{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} "
                    "[{remaining}s, {rate_fmt}{postfix}]"
                ) % (Fore.LIGHTWHITE_EX, Fore.LIGHTWHITE_EX)
            )
        ) if self.progress else commands

        for i, command in enumerate(commands_iter):
            message = f"(8.{i + 1}) Images Group Number {i + 1}"

            if self.progress:
                commands_iter.set_description(message)
            # end if

            execute(command, process=process_name(self.depth_mapping) + f" {message}")
        # end for
    # end depth_mapping

    def depth_map_filtering(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.depth_map_filtering)
    # end depth_map_filtering

    def meshing(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.meshing)
    # end meshing

    def mesh_filtering(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.mesh_filtering)
    # end mesh_filtering

    def texturing(self) -> None:
        """Runs the process in the command line."""

        self._execute(self.command_generator.texturing)
    # end texturing

    def render_generator(
            self,
            destination: Optional[str] = None,
            source: Optional[str] = None,
            override: Optional[bool] = False,
            group_size: Optional[int] = None,
            color: Optional[bool] = None,
            path: Optional[str] = None,
            progress: Optional[bool] = True,
            output: Optional[str] = None
    ) -> Generator[Mesh, ..., ...]:
        """
        Defines the class attributes for the process and runs it.

        :param destination: The destination directory to save the process in.
        :param source: The directory of the input images of the object.
        :param group_size: The number of images to include in a group.
        :param color: The value to add the texture to the model.
        :param path: The bin location folder
        :param progress: The value to show the progress in the command line.
        :param override: The value to remove existing content from the directories.
        :param output: The output directory.
        """

        self.initialize(
            destination=destination or self.destination,
            source=source or self.source,
            override=override or self.override,
            path=path, group_size=group_size,
            color=color or self.color,
            progress=progress, output=output
        )

        start_time = datetime.now()

        self.model.start_time = start_time

        if progress:
            print(
                "\nAuto Meshroom - Automatic Photogrammetry "
                "(2D Images to 3D Model)\n"
            )

            if self.path != scripts():
                print(f"Bin Directory: {self.path}")
            # end if

            print(f"Output Directory: {self.destination}")
            print(f"Source Directory: {self.source}")
            print(f"Process Directory: {self.output}")
            print(f"Images Count: {self.images_count}")
            print(f"Coloring: {self.color}")
            print(f"\nProcess Starting.\nStart Time: {start_time}\n")
        # end if

        output = Path(self.output)

        if not self.override and output.exists():
            warnings.warn(
                f"A directory with the saving path '{output}', "
                f"already exists. This might cause errors. "
                f"Make sure to specify a non-existing output path, "
                f"or use the 'override' value to remove pre-existing content."
            )

        elif output.exists():
            remove_content(str(output))
        # end if

        commands_iter = tqdm.tqdm(
            self.commands, bar_format=(
                (
                    "{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} "
                    "[{remaining}s, {rate_fmt}{postfix}]"
                ) % (Fore.LIGHTWHITE_EX, Fore.LIGHTWHITE_EX)
            ), desc="3D Reconstruction"
        ) if progress else self.commands

        for i, command_name, command in zip(
            range(1, len(commands_iter) + 1),
            self.commands_names, commands_iter
        ):
            if progress:
                commands_iter.set_description(f"({i}) {command_name}")
            # end if

            yield command()
        # end for

        end_time = datetime.now()
        total_time = end_time - start_time

        if progress:
            print(
                f"\nProcess Complete.\nEnd Time: {end_time}"
                f"\nTotal Time: {total_time}\n"
            )
        # end if

        results = [self.command_generator.mesh_filtering.__name__]

        if self.color:
            results.append(self.command_generator.texturing.__name__)
        # end if

        for result in results:
            output_directory = output / Path(result)

            build_directory(self.destination, override=override)

            for file in os.listdir(output_directory):
                shutil.copy2(
                    str(output_directory / Path(str(file))),
                    str(Path(self.destination) / Path(str(file)))
                )
            # end for
        # end for

        if (
            os.path.exists(self.output) and
            (
                os.path.split(
                    Path(tempfile.TemporaryDirectory().name)
                )[0] in self.output
            )
        ):
            remove_content(self.output)

            os.remove(self.output)
        # end if

        self.model.end_time = end_time
        self.model.total_time = total_time

        return self.model
    # end render_generator

    def render(
            self,
            destination: Optional[str] = None,
            source: Optional[str] = None,
            override: Optional[bool] = False,
            group_size: Optional[int] = None,
            color: Optional[bool] = None,
            path: Optional[str] = None,
            progress: Optional[bool] = True,
            output: Optional[str] = None
    ) -> Mesh:
        """
        Defines the class attributes for the process and runs it.

        :param destination: The destination directory to save the process in.
        :param source: The directory of the input images of the object.
        :param group_size: The number of images to include in a group.
        :param color: The value to add the texture to the model.
        :param path: The bin location folder
        :param progress: The value to show the progress in the command line.
        :param override: The value to remove existing content from the directories.
        :param output: The output directory.
        """

        generator = self.render_generator(
            destination=destination, source=source,
            override=override, group_size=group_size,
            color=color, path=path, progress=progress,
            output=output
        )

        list(generator)

        return self.model
    # end render
# ModelBuilder

def render(
        destination: Optional[str] = None,
        source: Optional[str] = None,
        override: Optional[bool] = False,
        group_size: Optional[int] = None,
        color: Optional[bool] = None,
        output: Optional[str] = None,
        path: Optional[str] = None,
        progress: Optional[bool] = True
) -> Mesh:
    """
    Runs the client requests with the server to get the 3d reconstruction.

    :param destination: The destination directory to save the process in.
    :param source: The directory of the input images of the object.
    :param group_size: The number of images to include in a group.
    :param color: The value to add the texture to the model.
    :param path: The source directory path.
    :param override: The value to remove existing content from the directories.
    :param progress: The value to silence the destination
    :param output: The output directory.
    """

    return Modeler().render(
        destination=destination, source=source,
        override=override, path=path,
        group_size=group_size, color=color,
        progress=progress, output=output
    )
# end render