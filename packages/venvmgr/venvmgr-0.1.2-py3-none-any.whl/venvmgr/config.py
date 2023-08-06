"""
Config file for venvs
=====================
"""

import os
import configparser
from contextlib import contextmanager


VENV_DIR = os.path.join(os.environ['HOME'], '.venvmgr')
CONFIG_FILE = os.path.join(os.environ['HOME'], '.venvmgr.conf')
ASSOCIATION = "ASSOCIATION"
ANNOTATION = "ANNOTATION"
TIME = "TIME"


@contextmanager
def open_config():
    """
    @brief Context to open and save config file
    """
    os.makedirs(VENV_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'a'):
        pass

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    yield config

    with open(CONFIG_FILE, 'w') as f:
        config.write(f)


def set(section, key, value):
    """
    @brief Alter the config
    """
    with open_config() as o:
        if not o.has_section(section):
            o.add_section(section)
        o[section][key] = str(value)


def get(section):
    """
    @brief Alter the config
    """
    with open_config() as o:

        if not o.has_section(section):
            return {}

        return o[section]
