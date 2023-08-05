# exceptions.py

from typing import Optional

from colorama import Fore

class AliceVisionFailError(Exception):
    """An error for AliceVision computation fail."""

    def __init__(
            self,
            command: Optional[str] = None,
            process: Optional[str] = None,
            message: Optional[str] = None
    ) -> None:
        """
        Creates an exception for alice vision failure.

        :param command: The failed command.
        """

        self.message = (
            f"{Fore.LIGHTRED_EX}AliceVision has failed to run the "
            f"'{process}' computation according to the command:\n\n"
            + command.replace(' --', '\n --')
        ) + ("" if message is None else f"\n\n{message}")

        Exception.__init__(self, self.message)
    # end __init__
# end AliceVisionFailError

class DirectoryNotEmptyWarning(UserWarning):
    """An error for AliceVision computation fail."""

    def __init__(self, path: str, paths: list) -> None:
        """
        Creates an exception for alice vision failure.

        :param path: The path to the directory.
        :param paths: The list of items in the directory:
        """

        self.message = (
            f"\n{Fore.LIGHTRED_EX}\nThe '{path}' directory is not "
            f"empty, and its content\nwill not be removed because the "
            f"'override' value was set to 'False'.\nThis might cause some "
            f"issues and result in errors.\n\nInside content:\n" + '\n\t'.join(paths) + "\n"
        )

        UserWarning.__init__(self, self.message)
    # end __init__
# end DirectoryNotEmptyWarning