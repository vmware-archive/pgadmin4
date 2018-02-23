## Initial steps
 - Create a venv environment that will be shipped with pgAdmin4
 - Copy it to a folder called venv in the current folder

_Caveat_: Because we ship the Python build we need to replace or create a better way to store the python venv folder
for each type of OS

### After this step the folder should look like:

```
electron
 |
 + - assets/
 + - venv/
 + - .gitignore
 + - index.html
 + - main.js
 + - package.json
 + - README.md
 + - yarn.lock
```

## Packages generation

### Pre requirements
You should have installed Python, VirtualEnv, Node.js and Yarn.
Also you should create a python environment using Python and VirtualEnv

If `venv` folder exists remove it

Inside electron folders do:
```commandline
python -m venv venv
```

This will create the venv folder.

### Windows
Unfortunately for windows we need to use a psycopg2 and pycrypto prebuild binaries this mean that we need 
to installed them first and change `..\requirements.txt` to point to those versions.
Only found versions for Python 3.4 so we need to install that

#### Package generation steps
Step 1 - Install python dependencies, inside the folder `electron`
```commandline
venv\Scripts\pip.exe install -r ..\requirements
```

Step 2 - Copy python source, copy configuration and create javascript bundle, inside the folder `electron`
```commandline
yarn build:windows
```

Step 3 - Remove package.json. Only needed in windows, due to some strange behavior of the electron-builder
```commandline
rm pgadmin4\package.json
```

Step 4 - Create package
```commandline
yarn dist
```

### Mac and Linux

#### Package generation steps
Step 1 - Install python dependencies, inside the folder `electron`
```commandline
venv/bin/pip install -r ../requirements
```

Step 2 - Copy python source, copy configuration and create javascript bundle, inside the folder `electron`
```commandline
yarn build:nix
```

Step 3 - Create package
```commandline
yarn dist
```

## Installation

### Windows and Mac
No special instructions, just follow the installer

### Linux

Need to install the following libraries:
- /bin/sh
- libXScrnSaver
- libappindicator
- libnotify
- GLIBC == 2.25


## Old instruction set

### Install electron and dependencies
`yarn install`

### copy application folder
`cp -r ../web pgadmin4`

### Remove the node_modules from the pgadmin folder and reinstall the dependencies
```bash
cd pgadmin4
rm -rf node_modules
yarn install
```

### Create the bundle files
```cd pgadmin4 && yarn bundle```

I noticed some issues on this step so I run the yarn bundle on
the `web` folder instead before copying over

### Clean not needed files:
```
rm -rf pgadmin4/node_modules
find pgadmin4 | grep .pyc$ | xargs -I '{}' rm '{}'
rm -rf pgadmin4/pgadmin/static/js/generated/.cache
```

### Run the application without packaging it for debug
```
./node_modules/.bin/electron .
```

### Create the package
```
./node_modules/.bin/electron-packager . --overwrite --ignore=".*\.zip" --ignore=".*\.log" --icon=assets/icons/mac/logo-256.png.hqx --package-manager=yarn
```
