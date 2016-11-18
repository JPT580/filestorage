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

##Adapt the configuration
Check the contents of `settings.ini` to define what interface the service shall bind to.
Also location for files and the shelve database can be configured in there.

##Run the application

```
$VENV/bin/pserve settings.ini --reload
```

The `--reload` option is optional and helpful for development purposes.
Also, different wsgi servers can be used. (More about that later)
