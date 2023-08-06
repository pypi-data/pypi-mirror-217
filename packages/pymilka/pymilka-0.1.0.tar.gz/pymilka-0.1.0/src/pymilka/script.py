import argparse
from pymilka.templates import BaseTemplate
from pymilka.user_input import project_config


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="", help="Path for your new project.")
    parser.add_argument(
        "-q", "--quick", help="Quick project setup.", action="store_true"
    )
    args = parser.parse_args()
    return args


def main():
    args = __parse_args()
    try:
        config = project_config(quick=args.quick)
        try:
            project = BaseTemplate(config=config, project_path=args.target)
        except FileNotFoundError:
            print("Invalid project path!")
    except Exception:
        print("Invalid config!")
