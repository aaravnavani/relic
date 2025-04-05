const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { exec } = require("child_process");

function createWindow() {
  const win = new BrowserWindow({
    width: 500,
    height: 300,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true
    }
  });
  win.loadFile("index.html");
}

ipcMain.handle("export-messages", async () => {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, "export_messages.py");
    const command = `python3 \"${scriptPath}\"`;
    exec(command, {
      env: { ...process.env, PATH: process.env.PATH + ":/usr/local/bin:/opt/homebrew/bin" }
    }, (error, stdout, stderr) => {
      if (error) {
        reject(stderr || error.message);
      } else {
        resolve(stdout);
      }
    });
  });
});

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});