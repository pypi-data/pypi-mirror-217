"""
CLI for venv manager
====================
"""


import os
import click

from . import venvmgr
from . import config


__version__ = "0.1.1"


def get_venv_names(ctx, args, incomplete):
    return os.listdir(config.VENV_DIR)


@click.group()
@click.version_option(__version__)
def commands():
    pass


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('file', required=False, default=None,
                type=click.Path(exists=True))
@click.option('--venv',
              type=click.STRING,
              default=None,
              required=False,
              shell_complete=get_venv_names,
              help="Name of venv")
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def python(file, venv, args):
    """
    Python though with a venv argument

    If no VENV provided but a FILE is provided, uses a VENV inferred from FILE
    """
    venvmgr.python(venv, file, *args)


@click.command()
@click.option('-l', '--long', type=bool, default=False,
              is_flag=True, help='long listing format')
@click.argument('name', nargs=-1, required=False,
                type=click.STRING, shell_complete=get_venv_names)
def ls(long, name):
    """
    List information about venvmgr known venvs
    """
    click.echo_via_pager("\n".join(venvmgr.ls(name, long)))


@click.command()
@click.argument('name', type=click.STRING, shell_complete=get_venv_names)
@click.argument('file', type=click.Path(exists=True), nargs=-1)
def associate(name, file):
    """
    Associate venv NAME with FILE
    """
    venvmgr.associate(name, file)


@click.command()
@click.argument('name', type=click.STRING, shell_complete=get_venv_names)
@click.option('-r', '--requirement',
              type=click.Path(exists=True),
              default=None,
              required=False,
              help="Install from the given requirements file")
def create(name, requirement):
    """
    Create NAME venv
    """
    venvmgr.create(name, requirement)


@click.command()
@click.argument('name', type=click.STRING, shell_complete=get_venv_names)
def rm(name):
    """
    Remove NAME venv
    """
    venvmgr.rm(name)


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--venv', type=click.STRING, required=True,
              shell_complete=get_venv_names, help="Name of venv")
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def pip(venv, args):
    """
    Pip though with venv argument
    """
    venvmgr.pip(venv, *args)


@click.command()
@click.argument('dir', type=click.STRING)
def add(dir):
    """
    Add a venv from DIR created outside of vm
    """
    venvmgr.add(dir)


@click.command()
@click.argument('name', type=click.STRING, shell_complete=get_venv_names)
def annotate(name):
    """
    Annotate NAME venv
    """
    venvmgr.annotate(name)


@click.command()
def home():
    """
    Location of venvmgr home directory
    """
    click.echo(config.VENV_DIR)


@click.command()
def dotfile():
    """
    Location of venvmgr configuration file
    """
    click.echo(config.CONFIG_FILE)


@click.command()
@click.argument('name', type=click.STRING, shell_complete=get_venv_names)
def activate(name):
    """
    Activate NAME venv
    """
    venvmgr.activate(name)


commands.add_command(create)
commands.add_command(rm)
commands.add_command(python)
commands.add_command(ls)
commands.add_command(pip)
commands.add_command(add)
commands.add_command(annotate)
commands.add_command(associate)
commands.add_command(home)
commands.add_command(dotfile)
commands.add_command(activate)
