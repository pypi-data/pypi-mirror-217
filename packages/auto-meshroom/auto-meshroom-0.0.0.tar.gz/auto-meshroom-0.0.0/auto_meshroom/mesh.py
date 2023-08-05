# mesh.py

from typing import List, Dict, Optional
import datetime as dt
import os

from represent import BaseModel

class Mesh(BaseModel):
    """
    A class to represent the result object.

    This class represent the results object returned
    from the complete modeling process.

    This class acts as a data class mainly, to isolate different
    models and process results.

    The constractor parameters:

    - destination:
        The destination directory in which to save the result files.

    - source:
        The path to the directory of the source images of an object to 3D model,
        taken by a digital camera.

    - color:
        The value to add a colored texture to the 3D model.

    >>> from auto_meshroom import Modeler
    >>>
    >>> modeler = Modeler(...)
    >>>
    >>> mesh = modeler.render(...)
    >>>
    >>> print(mesh.output_files)
    """

    def __init__(self, source: str, destination: str, color: bool) -> None:
        """
        Defines the class attributes of the class.

        :param source: The directory with the input images.
        :param destination: The directory to save the results in.
        :param color: The value to create color.
        """

        self.start_time: Optional[dt.datetime] = None
        self.end_time: Optional[dt.datetime] = None
        self.total_time: Optional[dt.timedelta] = None

        self.source_files_data: Dict[str, bytes] = {}
        self.output_files_data: Dict[str, bytes] = {}

        self.source = source
        self.destination = destination

        self.color = color
    # end __init__

    @property
    def source_files(self) -> List[str]:
        """
        Returns the list of files.

        :return:  # returns the list of files.
        """

        if (
            (self.source is not None) and
            os.path.exists(self.source) and
            (source_files := os.listdir(self.source))
        ):
            return [
                os.path.join(self.source, path)
                for path in source_files
            ]
        # end if
    # end source_files

    @property
    def output_files(self) -> List[str]:
        """
        Returns the list of files.

        :return:  # returns the list of files.
        """

        if (
            (self.destination is not None) and
            os.path.exists(self.destination) and
            (output_files := os.listdir(self.destination))
        ):
            return [
                os.path.join(self.destination, path)
                for path in output_files
            ]
        # end if
    # end output_files

    def load_source_files_data(self) -> Dict[str, bytes]:
        """
        Loads the data of the source files.

        :return: The bytes' data of the files, in a list.
        """

        for path in self.source_files:
            with open(path, "rb") as file:
                self.source_files_data[path] = file.read()
            # end open
        # end for

        return self.source_files_data
    # end load_source_files_data

    def load_output_files_data(self) -> Dict[str, bytes]:
        """
        Loads the data of the source files.

        :return: The bytes' data of the files, in a list.
        """

        for path in self.output_files:
            with open(path, "rb") as file:
                self.output_files_data[path] = file.read()
            # end open
        # end for

        return self.output_files_data
    # end load_output_files_data
# end Mesh