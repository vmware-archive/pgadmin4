## Building

### Prerequisites
* [Docker](https://www.docker.com/)

### Linux
1. `cd` into the root directory of the project.
1. Execute the `./electron/scripts/build-linux` script in the corresponding docker image to compile utilities (python, javascript) to be bundled with the application.
   ```
   $ docker run -v $PWD:$PWD -w $PWD --rm -t python:3.6 ./electron/scripts/build-linux.sh
   ```

   The linux distributable will be found in the `out/make` directory of the previous electron folder.