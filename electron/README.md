##Initial steps
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
/node_modules/.bin/electron-packager . --overwrite --ignore=".*\.zip" --ignore=".*\.log" --icon=assets/icons/mac/logo-256.png.hqx --package-manager=yarn
```
