"""
Manager for virtual environments
================================
"""

import datetime
import functools
import os
import shutil
import subprocess
import tempfile

import venv
import click

from . import config


def locate(venv_name, bin_):
    """
    @brief Path to venv binaries
    """
    return os.path.realpath(
        os.path.join(
            config.VENV_DIR,
            venv_name,
            "bin",
            bin_))


def isvenv(venv_name):
    """
    @brief Whether a venv with such a name exists
    """
    for f in ["activate", "python", "pip"]:
        if not os.path.isfile(locate(venv_name, f)):
            return False
    return True


def default_venv_name(file_name):
    """
    @brief Default name for a venv
    """
    abs_ = os.path.abspath(file_name)
    return abs_.replace(os.path.sep, "_").replace(".", "_").strip("_")


def create(venv_name, reqs=None):
    """
    @brief Create a new virtual environment
    """
    if isvenv(venv_name) and not click.confirm(
            f"'{venv_name}' already exists. Continue?"):
        return

    env = venv.EnvBuilder(with_pip=True)
    dir_env = os.path.join(config.VENV_DIR, venv_name)
    env.create(dir_env)
    config.set(config.TIME, venv_name, datetime.datetime.now())

    if reqs is None and os.path.isfile("requirements.txt"):
        reqs = "requirements.txt"

    if reqs is not None:
        pip(venv_name, "install", "-r", reqs)


def ls(venv_names, long_=False):
    """
    @brief List known virtual environments
    """
    if not venv_names:
        venv_names = os.listdir(config.VENV_DIR)

    for venv_name in sorted(venv_names):

        yield click.style(venv_name, fg='green', bold=True)

        if time := config.get(config.TIME).get(venv_name):
            yield click.style(f"created at {time}", fg='green', italic=True)

        if annotation := config.get(config.ANNOTATION).get(venv_name):
            for line in annotation.split("\n"):
                yield click.style(line, fg='green', italic=True)

        if not isvenv(venv_name):
            yield click.style("broken", fg='red', bold=True)

        a = click.format_filename(locate(venv_name, "activate"))
        yield click.style("activate: " + click.style(f"source {a}", fg='red'))

        file_names = [
            click.format_filename(k) for k,
            v in config.get(
                config.ASSOCIATION).items() if v == venv_name]

        if file_names:
            yield click.style("used by: " + click.style(", ".join(file_names), fg='red'))
        else:
            yield click.style("no known users", fg='red')

        if long_:
            try:
                res = pip(
                    venv_name,
                    "list",
                    verbose=False,
                    stdout=subprocess.PIPE)
                table = res.stdout.decode('utf-8')
                for line in table.split("\n"):
                    yield click.style(line)
            except RuntimeError as r:
                yield click.style(r, fg='red', bold=True)

        yield click.style("")


def create_if_not_exist(venv_name):
    """
    @brief Create a venv if it does not exist
    """
    if not isvenv(venv_name):
        if click.confirm(f"Create new venv '{venv_name}'?"):
            create(venv_name)
        else:
            raise RuntimeError(f"Does not exist - {venv_name}")


def venv_must_exist(func):
    """
    @brief Raise error if venv does not exist
    """
    @functools.wraps(func)
    def with_venv_must_exist(venv_name, *args, **kwargs):
        create_if_not_exist(venv_name)
        return func(venv_name, *args, **kwargs)
    return with_venv_must_exist


@venv_must_exist
def associate(venv_name, file_names):
    """
    @brief Associate a venv with file names
    """
    for file_name in file_names:
        config.set(config.ASSOCIATION, os.path.abspath(file_name), venv_name)


@venv_must_exist
def annotate(venv_name):
    """
    @brief Leave an annotation about a venv
    """
    marker = f'# Annotation for {venv_name}\n'
    start = config.get(config.ANNOTATION).get(venv_name, marker)
    message = click.edit(start)

    if message is not None:
        annotation = message.split(marker, 1)[-1].strip()
        config.set(config.ANNOTATION, venv_name, annotation)


def add(venv_name):
    """
    @brief Add a venv created outside of vm
    """
    os.symlink(
        os.path.abspath(venv_name),
        os.path.join(
            config.VENV_DIR,
            os.path.basename(venv_name)))
    config.set(config.TIME, venv_name, datetime.datetime.now())


def rm(venv_name):
    """
    @brief Removes a venv
    """
    d = f"{config.VENV_DIR}/{venv_name}"
    if click.confirm(f"Are you sure you wish to remove '{d}'?"):
        shutil.rmtree(d)


def python(venv_name, file_name, *args, verbose=True, **kwargs):
    """
    @brief Run a Python file in a virtual environment
    """
    abs_file_name = os.path.abspath(file_name)

    if file_name is None and venv_name is None:
        raise RuntimeError("Require venv name or file name")

    if venv_name is None:
        venv_name = config.get(
            config.ASSOCIATION).get(
            abs_file_name,
            default_venv_name(file_name))

    create_if_not_exist(venv_name)

    config.set(config.ASSOCIATION, abs_file_name, venv_name)

    bin_python = locate(venv_name, "python")

    if verbose:
        click.secho(
            f"python = {click.format_filename(bin_python)}",
            fg='green',
            bold=True)
    return subprocess.run([bin_python] + list(args) + [file_name], check=False, **kwargs)


@venv_must_exist
def pip(venv_name, *cmds, verbose=True, **kwargs):
    """
    @brief Run a Python file in a virtual environment
    """
    bin_pip = locate(venv_name, "pip")

    if verbose:
        click.secho(
            f"pip = {click.format_filename(bin_pip)}",
            fg='green',
            bold=True)

    return subprocess.run([bin_pip] + list(cmds), check=False, **kwargs)


@venv_must_exist
def activate(venv_name):
    """
    Activate venv in new shell
    """
    activation = locate(venv_name, "activate")

    bashrc = f"""
    #!/bin/bash

    source $HOME/.bashrc
    source {activation}
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
        tf.write(bashrc)
        command = f'bash --rcfile {tf.name}'

    os.system(command)
