const { app, BrowserWindow } = require("electron");

function createWindow() {
  const win = new BrowserWindow({
    width: 600,
    height: 850,
    resizable: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: false,
    },
  });

  win.loadURL("http://localhost:5000/tag");
}

app.whenReady().then(() => {
  createWindow();
});
