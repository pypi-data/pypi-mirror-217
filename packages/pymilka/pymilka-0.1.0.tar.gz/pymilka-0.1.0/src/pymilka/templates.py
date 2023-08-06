from typing import Union, Dict
from pathlib import Path
from pymilka.structures import ProjectFile, Directory, PythonFile, PythonPackage
from pymilka.constants import (
    dev_requirements,
    setup_cfg_options,
    pyproject_toml_settings,
    gitignore_settings,
)


class BaseTemplate:
    def __init__(self, config: Dict[str, str], project_path: Union[Path, str] = ""):
        self.project_name = config["name"]
        self.project_dir = Directory(self.project_name, project_path)
        self.src_dir = Directory("src", self.project_dir.directory_path)
        self.python_package_dir = PythonPackage(
            self.project_name, self.src_dir.directory_path
        )
        self.tests_dir = self.__create_tests_dir()
        self.requirements_file = self.__create_requirements()
        self.readme_file = ProjectFile("README.md", self.project_dir)
        self.changelog_file = ProjectFile("CHANGELOG.md", self.project_dir)
        self.setup_cfg_file = self.__create_setup_cfg(config=config)
        self.pyproject_toml = self.__create_pyproject_toml()
        self.gitignore = self.__create_gitignore()
        self.license_file = ProjectFile("LICENSE", self.project_dir)

    def __create_tests_dir(self) -> PythonPackage:
        tests_dir = PythonPackage("tests", self.project_dir.directory_path)
        self.conftest_file = PythonFile("conftest", tests_dir)
        return tests_dir

    def __create_requirements(self) -> ProjectFile:
        requirements_file = ProjectFile("requirements.txt", self.project_dir)
        with open(requirements_file.file_path, "w") as requirements_f:
            requirements_f.writelines(dev_requirements)
        return requirements_file

    def __create_setup_cfg(self, config) -> ProjectFile:
        setup_cfg = ProjectFile("setup.cfg", self.project_dir)
        with open(setup_cfg.file_path, "w") as setup_cfg_file:
            setup_cfg_file.write("[metadata]\n")
            for param, value in config.items():
                setup_cfg_file.write(f"{param} = {value}\n")
            setup_cfg_file.write(setup_cfg_options)
        return setup_cfg

    def __create_pyproject_toml(self) -> ProjectFile:
        pyproject_toml = ProjectFile("pyproject.toml", self.project_dir)
        with open(pyproject_toml.file_path, "w") as pyproject_toml_file:
            pyproject_toml_file.write(pyproject_toml_settings)
        return pyproject_toml

    def __create_gitignore(self) -> ProjectFile:
        gitignore = ProjectFile(".gitignore", self.project_dir)
        with open(gitignore.file_path, "w") as gitignore_file:
            gitignore_file.writelines(gitignore_settings)
        return gitignore
