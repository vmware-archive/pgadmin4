#!/bin/bash


source /pgadmin_venv/bin/activate
pip install -r /pgadmin/requirements.txt

pushd /pgadmin/electron
    yarn install
    cp -r /pgadmin_venv venv
    ## Missing removal of compiled python files
    ## Missing compilation of javascript
    ## Clean webpack cache
    yarn package --platform=linux
popd
