const electron = require('electron');
const {globalShortcut, ipcMain, shell} = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const waitOn = require('wait-on');

const pythonApplicationUrl = 'localhost:7895';

var waitForPythonProcessToStart = {
    resources: [
        'http-get://' + pythonApplicationUrl
    ],
    delay: 1000, // initial delay in ms, default 0
    interval: 100, // poll interval in ms, default 250ms
    timeout: 30000, // timeout in ms, default Infinity
    window: 1000, // stabilization time in ms, default 750ms
};


let allWindows = {};


/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = 'pgadmin4';
const PY_MODULE = 'pgAdmin4.py';

let pyProc = null;
let pyPort = null;
let activeWindow = null;
let loadingWindow = null;

const guessPackaged = () => {
    const fullPath = path.join(__dirname, PY_DIST_FOLDER);
    return require('fs').existsSync(fullPath);
};

pythonExecPath = path.join(__dirname, 'venv', 'bin', 'python');

const getScriptPath = () => {
    if (process.platform === 'win32') {
        return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE);
    }
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE);
};

const selectPort = () => {
    pyPort = 7894;
    return pyPort;
};
const fs = require('fs');
let access = null;
let error = null;
if (!guessPackaged()) {
    access = fs.createWriteStream(__dirname + '/node.access.log', {flags: 'a'});
    error = fs.createWriteStream(__dirname + '/node.error.log', {flags: 'a'});
}

const createPyProc = () => {
    let script = getScriptPath();
    let port = '' + selectPort();

    // clone the actual env vars to avoid overrides
    let env = Object.create(process.env);
    env.PGADMIN_PORT = 7895;

    pyProc = require('child_process').spawn(
        pythonExecPath,
        [script, port],
        {env: env}
    );

    if (pyProc != null) {
        console.log('child process success on port ' + port);
        pyProc.stdout.on('data', function (buf) {
            console.log('[STR] stdout "%s"', String(buf));
        });
        pyProc.stderr.on('data', function (buf) {
            console.log('[STR] stderr "%s"', String(buf));
        });
        if (!guessPackaged()) {
            pyProc.stdout.pipe(access);
            pyProc.stderr.pipe(error);
        }
        pyProc.on('close', function (code, stdout, stderr) {
            try {

                console.log('[END] code', code);
                console.log('[END] stdout "%s"', stdout);
                console.log('[END] stderr "%s"', stderr);
            } catch (err) {
            }
        });
    }
};

const exitPyProc = () => {
    console.log('Going to exit');
    if (pyProc != null) {
        pyProc.kill();
        pyProc = null;
        pyPort = null;
    } else {
        app.exit();
    }
};

app.on('ready', createPyProc);
app.on('will-quit', exitPyProc);
app.on('before-quit', () => {
    console.log('before-quit');
    exitPyProc();

    app.quit();
});
app.on('quit', () => {
    console.log('quit')
});


/*************************************************************
 * window management
 *************************************************************/

let mainWindow = null;

const createMainWindow = () => {
    mainWindow = createNewWindow('http://' + pythonApplicationUrl);
    const Menu = electron.Menu;

    // Create the Application's main menu
    let template = [{
        label: "PGAdmin4",
        submenu: [
            {
                label: "New window",
                accelerator: "CommandOrControl+N",
                selector: "newwindow:",
                click: () => {
                    createNewWindow();
                }
            }, {
                label: "New tab",
                accelerator: "CommandOrControl+t",
                selector: "newtab:",
                click: () => {
                    activeWindow.webContents.send(
                        'tabs-channel',
                        'create',
                        'pgAdmin4',
                        pythonApplicationUrl
                    )
                }
            },
            {type: "separator"},
            {
                label: "About PGAdmin4",
                selector: "orderFrontStandardAboutPanel:"
            },
            {type: "separator"},
            {
                label: "Quit", accelerator: "Command+Q", click: function () {
                    app.quit();
                }
            }
        ]
    }, {
        label: "Edit",
        submenu: [
            {label: "Undo", accelerator: "CmdOrCtrl+Z", selector: "undo:"},
            {
                label: "Redo",
                accelerator: "Shift+CmdOrCtrl+Z",
                selector: "redo:"
            },
            {type: "separator"},
            {label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:"},
            {label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:"},
            {label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:"},
            {
                label: "Select All",
                accelerator: "CmdOrCtrl+A",
                selector: "selectAll:"
            },
            {type: "separator"},
            {
                label: 'Dev Tools',
                accelerator: 'CmdOrCtrl+Alt+I',
                click: () => {
                    if (activeWindow !== null) {
                        activeWindow.webContents.openDevTools();
                    }
                }
            }
        ]
    }
    ];

    if (process.platform === 'darwin') {
        template.unshift({
            label: app.getName(),
            submenu: [
                {role: 'about'},
                {type: 'separator'},
                {role: 'services', submenu: []},
                {type: 'separator'},
                {role: 'hide'},
                {role: 'hideothers'},
                {role: 'unhide'},
                {type: 'separator'},
                {role: 'quit'}
            ]
        })
    }

    Menu.setApplicationMenu(Menu.buildFromTemplate(template));

    globalShortcut.register('CommandOrControl+N', () => {
        console.log('CommandOrControl+N is pressed');
        createNewWindow();
    });
};


const createNewWindow = (url) => {
    const windowId = Math.random().toString();
    let webPreferences = {
        nativeWindowOpen: true

    };

    let newWindow = new BrowserWindow({
        width: 800,
        height: 600,
        icon: path.join(__dirname, 'assets/icons/mac/logo-256.png.icns'),
        webPreferences: webPreferences,
        show: false,
    });
    let urlToLoad = require('url').format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    });
    if (url !== undefined && url !== null) {
        urlToLoad = url;
        if (activeWindow !== null) {
            newWindow.webContents.session =
                Object.assign({}, activeWindow.webContents.session);
        }
    }
    // newWindow.webContents.openDevTools({mode: "undocked"});
    newWindow.loadURL(urlToLoad);

    newWindow.on('closed', () => {
        newWindow = null;
        delete allWindows[windowId];
    });

    newWindow.on('close', () => {
        newWindow.hide();
        delete allWindows[windowId];
    });

    newWindow.on('focus', () => {
        activeWindow = newWindow;
    });
    newWindow.webContents.once('dom-ready', () => {
        newWindow.show();
        loadingWindow.hide();
        loadingWindow.close();
    });

    activeWindow = newWindow;

    allWindows[windowId] = newWindow;

    return newWindow;
};

ipcMain.on('ELECTRON_GUEST_WINDOW_MANAGER_WINDOW_OPEN', (event, url) => {
    if (url.includes('localhost:7894')) {
        createNewWindow(url)
    } else {
        shell.openExternal(url)
    }
});

app.on('ready', () => {
    loadingWindow = new BrowserWindow({show: false, frame: false});
    loadingWindow.once('show', () => {
        waitOn(waitForPythonProcessToStart, function (err) {
            if (err) {
                return console.log(err);
            }
            // once here, all resources are available
            createMainWindow();
        });
    });
    loadingWindow.loadURL(require('url').format({
        pathname: path.join(__dirname, 'app/html/loading.html'),
        protocol: 'file:',
        slashes: true
    }));
    loadingWindow.show()
});

app.on('window-all-closed', () => {
    console.log('perhaps going to close windows');
    if (process.platform !== 'darwin') {
        app.quit()
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createMainWindow()
    }
});
