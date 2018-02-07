const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')


/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = 'pgadmin4'
const PY_MODULE = 'pgAdmin4.py'

let pyProc = null
let pyPort = null

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

pythonExecPath = path.join(__dirname, 'venv', 'bin', 'python')

const getScriptPath = () => {
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE)
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE)
}

const selectPort = () => {
  pyPort = 7894
  return pyPort
}
var fs = require('fs');
var access = fs.createWriteStream(__dirname + '/node.access.log', {flags: 'a'})
  , error = fs.createWriteStream(__dirname + '/node.error.log', {flags: 'a'});

const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  pyProc = require('child_process').spawn(pythonExecPath, [script, port])

  if (pyProc != null) {
    console.log('child process success on port ' + port)
    pyProc.stdout.on('data', function (buf) {
      console.log('[STR] stdout "%s"', String(buf));
    });
    pyProc.stderr.on('data', function (buf) {
      console.log('[STR] stderr "%s"', String(buf));
    });
    pyProc.stdout.pipe(access);
    pyProc.stderr.pipe(error);
    pyProc.on('close', function (code) {
      try {

        console.log('[END] code', code);
        console.log('[END] stdout "%s"', stdout);
        console.log('[END] stderr "%s"', stderr);
      } catch (err) {
      }
    });
  }
}

const exitPyProc = () => {
  console.log('Going to exit')
  if (pyProc != null) {
    pyProc.kill()
    pyProc = null
    pyPort = null
  } else {
    app.exit();
  }
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)
app.on('before-quit', () => {
  console.log('before-quit')
  exitPyProc()

  app.quit()
})
app.on('quit', () => {
  console.log('quit')
})


/*************************************************************
 * window management
 *************************************************************/

let mainWindow = null

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, 'assets/icons/png/64x64.png')
  })
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))
  // mainWindow.webContents.openDevTools()

  mainWindow.on('closed', () => {
    mainWindow = null
  })


  const Menu = electron.Menu;

// Create the Application's main menu
  var template = [{
    label: "PGAdmin4",
    submenu: [
      {label: "About PGAdmin4", selector: "orderFrontStandardAboutPanel:"},
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
      {label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", selector: "redo:"},
      {type: "separator"},
      {label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:"},
      {label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:"},
      {label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:"},
      {label: "Select All", accelerator: "CmdOrCtrl+A", selector: "selectAll:"}
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
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  console.log('perhaps going to close windows')
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

