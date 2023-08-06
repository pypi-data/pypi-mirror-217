import os
from pymilka.templates import BaseTemplate


def test_base_template_init(tmp_path, config):
    project = BaseTemplate(config=config, project_path=tmp_path)
    assert os.path.exists(tmp_path / config["name"])
