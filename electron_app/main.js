const { app, BrowserWindow } = require("electron");

async function createWindow() {
  const Store = (await import("electron-store")).default;

  const store = new Store();
  const defaultBounds = { width: 480, height: 620, x: undefined, y: undefined };
  const savedBounds = store.get("windowBounds") || defaultBounds;

  const win = new BrowserWindow({
    width: savedBounds.width,
    height: savedBounds.height,
    x: savedBounds.x,
    y: savedBounds.y,
    resizable: true,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  const clipArg = process.argv[2];
  const url = clipArg
    ? `http://localhost:5000/tag?file=${encodeURIComponent(clipArg)}`
    : "http://localhost:5000/tag";

  win.loadURL(url);

  const saveBounds = () => {
    if (!win.isMinimized() && !win.isMaximized()) {
      store.set("windowBounds", win.getBounds());
    }
  };

  win.on("resize", saveBounds);
  win.on("move", saveBounds);
}

app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
