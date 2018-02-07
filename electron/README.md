## copy application folder
`cp -r ../web pgadmin4`

## Create the bundle files
`cd pgadmin4 && yarn bundle`

## Clean not needed files:
```
rm -rf pgadmin4/node_modules
find pgadmin4 | grep .pyc$ | xargs -I '{}' rm '{}'
```

## Other cleaning:
```
rm -rf pgadmin4/pgadmin/static/js/generated/.cache
```

## Create the package
```
./node_modules/.bin/electron-packager . --overwrite --ignore=".*\.zip" --ignore="pgAdmin4-darwin-x64" --icon=logo-256.icns
```
