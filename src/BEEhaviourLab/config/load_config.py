import logging
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import yaml


def get_config(data: Union[Path, dict, None]) -> SimpleNamespace:
    """Given a path to a YAML file or a dictionary object, returns a 
    simple namespace object holding config data. If the data is None, 
    an empty namespace is returned.
    """
    if data is None:
        return SimpleNamespace()
    elif isinstance(data, Path):
        logging.info(f"Loading config from {data}")
        if data.exists():
            with open(data, "r") as stream:
                config_dict = yaml.safe_load(stream)
            return SimpleNamespace(**config_dict)
        else:
            logging.error("Couldn't find config file... Exiting!")
            sys.exit(1)
    elif isinstance(data, dict):
        return SimpleNamespace(**data)
