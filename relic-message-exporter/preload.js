const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {
  exportMessages: () => ipcRenderer.invoke("export-messages")
});