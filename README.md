# Filestorage

This is a simple file storage and permanent archive service written in python using pyramid.
It allows people to drop off files through a REST API which are then assigned a UUIDv4 to link to.
This allows to easily achieve permanent links to files.

An easy to use web frontend for the api using jQuery is TBD.

##Install dependencies

```
export VENV=/path/to/venv
python3 -m venv $VENV
$VENV/bin/pip install -e .
```
##Run the application

```
$VENV/bin/pserve settings.ini --reload
```

The `--reload` option is optional and helpful for development purposes.
Also, different wsgi servers can be used. (More about that later)
