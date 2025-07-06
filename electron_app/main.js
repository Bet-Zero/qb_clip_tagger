const { app, BrowserWindow } = require("electron");

function createWindow() {
  const win = new BrowserWindow({
    width: 480,
    height: 760,
    resizable: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: false,
    },
  });

  const clipArg = process.argv[2];
  const url = clipArg
    ? `http://localhost:5000/tag?file=${encodeURIComponent(clipArg)}`
    : "http://localhost:5000/tag";
  win.loadURL(url);
}

app.whenReady().then(() => {
  createWindow();
});
