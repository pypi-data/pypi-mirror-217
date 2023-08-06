from typing import Dict
from pymilka.constants import metadata_params


def __validate_config(config):
    if config["name"] == "":
        raise Exception


def project_config(quick=False) -> Dict[str, str]:
    if quick:
        config = {param: "" for param in metadata_params}
        config["name"] = input("name: ")
    else:
        config = {param: input(f"{param}: ") for param in metadata_params}
    __validate_config(config)
    return config
