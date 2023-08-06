# read-and-chat

### Installation 

Run the following series of commands in a shell, such as bash.

```
git clone git@github.com:hssrobotics23/read-and-chat.git
cd read-and-chat
```

Install the repository locally with python `3.8` or above.

```
python3 -m pip install -e .
```

Then, run the command line tool `read-and-chat`.

```
read-and-chat
```

### Publishing

Bundle the source code and the wheels.

```
python3 -m pip install build
python3 -m build --sdist
python3 -m build --wheel
```

To publish to pypi [with credentials][creds] in your `.pypirc`, run:

```
python3 -m twine upload dist/*
```

[creds]: https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#id71
