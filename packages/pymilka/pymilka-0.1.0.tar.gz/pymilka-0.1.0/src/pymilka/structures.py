import os
from pymilka.logger import logger
from pathlib import Path
from typing import Union


class Directory:
    def __init__(self, directory_name: str, path: Union[str, Path] = ""):
        self.directory_name = directory_name
        self.directory_path = os.path.join(path, self.directory_name)
        os.mkdir(self.directory_path)
        logger.debug(f"Successfully created directory {self.directory_name}.")

    def create_sub_dir(self, sub_directory_name: str):
        return Directory(sub_directory_name, self.directory_path)

    def __str__(self) -> str:
        return str(self.directory_path)


class ProjectFile:
    def __init__(self, file_name: str, directory: Union[Path, str, Directory] = ""):
        self.file_name = file_name
        if isinstance(directory, Directory):
            directory = directory.directory_path
        self.file_path = os.path.join(directory, self.file_name)
        self.__create_file()

    def __create_file(self):
        with open(self.file_path, "w"):
            logger.debug(f"Successfully created {self.file_name}.")


class PythonFile(ProjectFile):
    def __init__(self, file_name: str, directory: Union[Path, str, Directory] = ""):
        file_name = f"{file_name}.py"
        super().__init__(file_name, directory)


class PythonPackage(Directory):
    def __init__(self, directory_name: str, path: Union[str, Path] = ""):
        super().__init__(directory_name, path)
        self.init_py = PythonFile("__init__", self.directory_path)
