// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const fs = require('fs');

// Enable live reload for all the files inside your project directory
require('electron-reload')(__dirname);

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      preload: path.join(__dirname, 'preload.js')
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

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
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

const commandFilePath = "./command.txt";
// const storage = require("./components/storage.js");
const storage = require('electron-localstorage');
ipcMain.on("saveText", (event, txtval) => {
  let currentCommand = fs.readFileSync(commandFilePath, "utf8");
  if (currentCommand != "run") {
    fs.unwatchFile(commandFilePath);
    console.log("Writing file...");
    fs.writeFile(commandFilePath, txtval.toString(), (err) => {
      if (!err) {
        currentCommand = fs.readFileSync(commandFilePath, "utf8");
        console.log("File written! currentCommand =",currentCommand);
        fs.watchFile(commandFilePath, () => {
          currentCommand = fs.readFileSync(commandFilePath, "utf8");
          console.log("Data file changed to",currentCommand);
          storage.setItem("elasticity",currentCommand);
          console.log(storage.getItem("elasticity"));
          // return currentCommand;
        });
      } else {
        console.log(err);
      }
    })
  } else {
    console.log("Already running");
  }

  
});