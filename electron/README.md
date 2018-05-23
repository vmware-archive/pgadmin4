## Building

### Prerequisites
* [Docker](https://www.docker.com/)
* [Python Virtual Environment](https://docs.python.org/3/library/venv.html) for python < 3.3

### Create the virtual environment 
1. `cd` into the electron folder of the project
1. Execute the following command to create the distributable version of Python
    ```bash
    $ python -m venv --copies venv
    ```
1. Install all packages needed by the application
    ```bash
    $ venv/bin/pip install -r ../requirements.txt
    ```

### Linux
1. `cd` into the root directory of the project.
1. Execute the `./electron/scripts/build-linux` script in the corresponding docker image to compile utilities (python, javascript) to be bundled with the application.
   ```
   $ docker run -v $PWD:$PWD -w $PWD --rm -t python:3.6 ./electron/scripts/build-linux.sh
   ```

   The linux distributable will be found in the `out/make` directory of the previous electron folder.