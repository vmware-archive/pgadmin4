function New-TemporaryDirectory {
    $parent = [System.IO.Path]::GetTempPath()
    $name = [System.IO.Path]::GetRandomFileName()
    New-Item -ItemType Directory -Path (Join-Path $parent $name)
}

$dir  = pwd
$full_folder_tempdir = New-TemporaryDirectory
$tempdir = "P:"
subst $tempdir $full_folder_tempdir
cd $tempdir

echo "## Copying Electron Folder to the temporary directory..."
cp -Recurse -force $dir\electron .

pushd .\electron > $null
    echo "## Copying pgAdmin folder to the temporary directory..."
    rm -erroraction 'silentlycontinue' web
    cp -Recurse -force $dir\web .

    echo "## Creating Virtual Environment..."
    rm -erroraction 'silentlycontinue' venv
    mkdir -p venv > $null
    virtualenv.exe venv
    . .\venv\Scripts\activate
    python -m pip install -r $dir\requirements.txt


    echo "## Compiling web folder"
    pushd web
     rm -erroraction 'silentlycontinue' node_modules
     yarn bundle-app-js
    popd
    yarn install
    yarn dist:windows
popd

rm ${dir}/electron/out/make/*.exe
mkdir ${dir}/electron/out/make
mv ${tempdir}/electron/out/make/squirrel.windows/x64/*.exe ${dir}/electron/out/make

cd $dir

subst $tempdir /D