indent = "    "
metadata_params = ("name", "version", "author", "author_email", "description")

setup_cfg_options = f"""
[options]
package_dir =
{indent}= src

python_requires = >=3.8
setup_requires =
install_requires =
"""

dev_requirements = ("black\n", "pytest\n", "-e .\n")

pyproject_toml_settings = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"
"""

gitignore_settings = (
    "venv/\n",
    "/.vscode/\n",
    "*.egg-info\n",
    "build/\n",
    ".idea/\n",
    ".pytest_cache\n",
    "dist/\n",
    "__pycache__/\n",
    "*.log\n",
    "*.db\n",
)
