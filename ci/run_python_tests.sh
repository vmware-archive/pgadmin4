#!/bin/sh

echo "EXECUTING: Python tests"
echo

echo "Creating Python ${PYTHON_VERSION} virtual environment..."
echo

cd $WORKSPACE/

PYTHON_SUFFIX=""

if [[ "$PYTHON_VERSION" == 3* ]]; then
    PYTHON_SUFFIX="3"
fi

/usr/bin/virtualenv -p /usr/local/python-$PYTHON_VERSION/bin/python$PYTHON_SUFFIX $WORKSPACE/pgadmin-venv || { echo 'ERROR: Failed to create the Python virtual environment.' ; exit 1; }
. $WORKSPACE/pgadmin-venv/bin/activate || { echo 'ERROR: Failed to activate the Python virtual environment.' ; exit 1; }
$WORKSPACE/pgadmin-venv/bin/pip install -r requirements.txt || { echo 'ERROR: Failed to install the application requirements.' ; exit 1; }
$WORKSPACE/pgadmin-venv/bin/pip install -r web/regression/requirements.txt || { echo 'ERROR: Failed to install the regression test requirements.' ; exit 1; }

echo "Running regression tests..."
echo

$WORKSPACE/pgadmin-venv/bin/python $WORKSPACE/web/regression/runtests.py  --exclude feature_tests || { echo 'ERROR: Error detected when running the Python tests.' ; exit 1; }

