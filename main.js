// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const fs = require('fs');

const commandFilePath = "./command.txt";
const storage = require('electron-localstorage');

// Enable live reload for all the files inside your project directory
require('electron-reload')(__dirname);

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    fullscreen: true,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      preload: path.join(__dirname, 'preload.js'),
      alwaysOnTop: true, 
      kiosk: true, 
      autoHideMenuBar: true
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  mainWindow.once('ready-to-show', function (){
    mainWindow.show();
  });
  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();
  fs.writeFile(commandFilePath, "-", (err) => {
    if (err) throw err;
    console.log('Command cleared');
  });
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
    
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  storage.clear();
  fs.writeFile(commandFilePath, "-", (err) => {
    if (err) throw err;
    console.log('Command cleared');
  });
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

ipcMain.handle("saveText", (event, txtval) => {
  event.preventDefault();
  let isLoading = false;
  let currentCommand = fs.readFileSync(commandFilePath, "utf8");
  console.log("saveText: Initial command =",currentCommand);
  if (currentCommand == "-" || txtval != "run") {
    fs.writeFileSync(commandFilePath, txtval.toString());
    let data = fs.readFileSync(commandFilePath, "utf8");
    console.log("File written! currentCommand =",data.toString());
    isLoading = true;
  } else {
    console.log("Already running");
  }
  event.preventDefault();
  console.log("returning", isLoading);
  return isLoading;
});

ipcMain.handle("readText", (event) => {
  let currentCommand = fs.readFileSync(commandFilePath, "utf8");
  console.log("readText: Initial command =",currentCommand);
  fs.unwatchFile(commandFilePath);
  fs.watchFile(commandFilePath, {interval:100}, () => {
    let data = fs.readFileSync(commandFilePath, "utf8");
    console.log("Data file changed to",data.toString());
    fs.unwatchFile(commandFilePath);
    if (isFinite(data)) {
      console.log("hey");
      let raw = data.toString();
      let m = 10.683;
      let c = 4275.7;
      // let e = (raw - 1545.1) / -40.94 * 2;
      let e = (raw - c) / m * 2;
      if (e>14) {
        e = 12.7;
      } else if (e<4) {
        e = 6.4;
      } else {
        e = e.toFixed(1);
      }
      console.log("raw =",raw," | elasticity =",e);
      storage.setItem("elasticity",e);  
    } else {
      console.log("not numbah");
    }
    fs.writeFileSync(commandFilePath, "-");
    data = fs.readFileSync(commandFilePath, "utf8");
    console.log("File written! currentCommand =",data.toString());
  });
});