const electron = require('electron');
const path = require('path');
const childProcess = require('child_process');
const logger = require('winston');
const checkPythonServer = require('./check_python_server');

const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let pythonProcess;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
  app.quit();
}

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
  });

  // and load the index.html of the app.
  mainWindow.loadURL(`file://${__dirname}/index.html`);

  // Open the DevTools.
  // mainWindow.webContents.openDevTools();

  // Emitted when the window is closed.
  mainWindow.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
  });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit();
    pythonProcess.kill();
  }
});

app.on('quit', () => {
  pythonProcess.kill();
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow();
  }
});

const createPyProc = () => {
  const pythonPath = path.join(__dirname, '..', 'venv', 'bin', 'python');
  const scriptPath = path.join(__dirname, '..', 'web', 'pgAdmin4.py');
  logger.info('Spawning...');
  pythonProcess = childProcess.spawn(pythonPath, [scriptPath]);

  checkPythonServer.checkIfPythonServerIsRunning(() => { return mainWindow.hide(); });

  pythonProcess.on('error', (error) => {
    logger.error(error.message);
  });

  pythonProcess.stdout.on('data', (data) => {
    logger.info(data);
  });

  pythonProcess.stderr.on('data', (data) => {
    logger.error(data);
  });
};

app.on('ready', createPyProc);
