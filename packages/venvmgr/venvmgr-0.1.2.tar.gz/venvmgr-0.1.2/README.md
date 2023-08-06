# venvmgr

_👀 Manage Python virtual environments_

## Install 💥

```bash
pipx install venvmgr
```

# Usage

Create a venv named `example` using venvmgr

```bash
$ vm create example
```
Use it using venvmgr

```bash
$ vm python --venv example code.py
```

The associations between files and venvs are recorded so that

```bash
$ vm python code.py
```
now uses the `example` venv. We might want to install packages in this venv, e.g.,

```bash
$ vm pip --venv example scipy
```

We now might want to check the venvs:

```bash
$ vm ls
example
created at 2023-07-03 12:07:48.872147
activate: source /home/user/.venvmgr/example/bin/activate
used by: /home/user/code.py
```
For more information, try `vm ls -l`.

Lastly, we might want to activate this venv

```bash
$ vm activate example
```


