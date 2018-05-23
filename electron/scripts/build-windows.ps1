function New-TemporaryDirectory {
    $parent = [System.IO.Path]::GetTempPath()
    $name = [System.IO.Path]::GetRandomFileName()
    New-Item -ItemType Directory -Path (Join-Path $parent $name)
}

$dir  = "C:\Users\IEUser\workspace\pgadmin4\"
$tempdir = New-TemporaryDirectory
cd $tempdir

echo "## Copying Electron Folder to the temporary directory..."
cp -r C:\Users\IEUser\workspace\pgadmin4\electron .

pushd .\electron > $null
echo "## Copying pgAdmin folder to the temporary directory..."
rm -r web
cp -r $dir\web .

echo "## Creating Virtual Environment..."
rm -r venv
mkdir -p venv > $null
virtualenv.exe venv
. .\venv\Scripts\activate
pip install -r $dir\requirements.txt


echo "## Compiling web folder"
pushd web
 rm node_modules
 yarn bundle-app-js
popd
yarn install
yarn dist:windows

rm ${dir}/electron/out/make/*.msi
mkdir -p ${dir}/electron/out/make
mv ${tmp_dir}/electron/out/make/*.msi ${dir}/electron/out/make