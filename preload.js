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
  screeningButton.addEventListener('click', (event) => {
    console.log("am here");
    let res = ipcRenderer.send("saveText","run");
    // console.log("res =",res);
    // localStorage.setItem("elasticity",res);
    // document.getElementById('input-unit').innerHTML = res;
    let val = storage.getItem("elasticity");
    document.getElementById('input-value').innerHTML = val;
  });

  const endButton = document.getElementById("end-screening");
  endButton.addEventListener("click", () => {
    let res = ipcRenderer.send("clearMemory");
    // localStorage.clear();
  });


})
