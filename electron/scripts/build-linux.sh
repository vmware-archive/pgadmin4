#!/usr/bin/env bash

set -e

dir=$(cd `dirname $0` && cd .. && cd .. && pwd)
tmp_dir=$(mktemp -d)

apt update
apt install -y apt-transport-https
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt install -y yarn fakeroot

echo "## Copying Electron Folder to the temporary directory..."
cp -r ${dir}/electron ${tmp_dir}/electron

pushd ${tmp_dir}/electron > /dev/null
  echo "## Copying pgAdmin folder to the temporary directory..."
  rm -rf web; cp -r ${dir}/web web

  echo "## Creating Virtual Environment..."
  rm -rf venv; mkdir -p venv
  python -m venv --copies ./venv
  source ./venv/bin/activate
  pip install -r ${dir}/requirements.txt

  echo "## Building the Javascript of the application..."
  pushd web > /dev/null
    rm -rf node_modules
    yarn bundle-app-js
  popd > /dev/null

  echo "## Creating the deb file..."
  yarn install
  yarn dist:linux
popd > /dev/null

rm -f ${dir}/electron/out/make/*.deb
mkdir -p ${dir}/electron/out/make
mv ${tmp_dir}/electron/out/make/*.deb ${dir}/electron/out/make
