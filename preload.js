// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.

const { ipcRenderer } = require("electron");

window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }

  for (const type of ['chrome', 'node', 'electron']) {
    replaceText(`${type}-version`, process.versions[type])
  }

  const screeningButton = document.getElementById('screening-activate');
  const storage = require('electron-localstorage');
  if (screeningButton) {
    screeningButton.addEventListener('click', (event) => {
      console.log("am here");
      let res = ipcRenderer.send("saveText","run");
      let val = storage.getItem("elasticity");
      document.getElementById('input-value').innerHTML = val;
    });
  }
  
})
