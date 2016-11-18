This is a simple file storage and permanent archive service.
It allows people to drop off files which are then assigned a uuid to link to.

=Install dependencies=

export VENV=/path/to/venv
python3 -m venv $VENV
$VENV/bin/pip install -e .

=Run the application stand-alone=

$VENV/bin/pserve settings.ini --reload

