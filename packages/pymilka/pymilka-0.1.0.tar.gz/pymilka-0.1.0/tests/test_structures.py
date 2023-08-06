import pytest
import os
from pymilka.structures import ProjectFile, Directory, PythonFile, PythonPackage


def test_directory_init(tmp_path):
    src_dir = Directory("src", tmp_path)
    package_dir = src_dir.create_sub_dir("python_package")
    assert os.path.exists(package_dir.directory_path)


@pytest.mark.parametrize("file_name", ["setup.cfg", "pyproject.toml", ".gitignore"])
@pytest.mark.parametrize("directory", [None, "src", "tests"])
def test_project_file_init(tmp_path, file_name, directory, directories):
    if directory:
        expected_file_path = tmp_path / directory / file_name
        project_file = ProjectFile(file_name=file_name, directory=tmp_path / directory)
    else:
        expected_file_path = tmp_path / file_name
        project_file = ProjectFile(file_name=file_name, directory=tmp_path)
    assert os.path.exists(expected_file_path)
    assert project_file.file_path == str(expected_file_path)


def test_structures_workflow(tmp_path):
    project_dir = Directory("project_dir", tmp_path)
    src_dir = Directory("src", project_dir.directory_path)
    package_dir = Directory("package", src_dir.directory_path)
    file = ProjectFile("setup.cfg", project_dir)
    python_file = PythonFile("constants", package_dir)
    assert os.path.exists(file.file_path)
    assert os.path.exists(python_file.file_path)


def test_python_package(tmp_path):
    src_dir = Directory("src", tmp_path)
    package_dir = PythonPackage("py_package", src_dir.directory_path)
    expected_init_file_path = os.path.join(package_dir.directory_path, "__init__.py")
    assert os.path.exists(expected_init_file_path)
