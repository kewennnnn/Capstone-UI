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
    console.log("screening-activate button found!");
    screeningButton.addEventListener('click', (event) => {
      event.preventDefault();
      console.log("am here");
      let isLoading = ipcRenderer.invoke("saveText","run"); 
      event.preventDefault();
      if (isLoading) { 
        console.log("ish loading");
        screeningButton.classList="button-grey";
      } else {
        console.log("nawt loading");
        screeningButton.classList="";
      }
      ipcRenderer.invoke("readText").then((res) => {
        console.log("readRes =",readRes);
        let val = storage.getItem("elasticity");
        document.getElementById('input-value').innerHTML = val;
        event.preventDefault();
      }); 
    });
  } else {
    console.log("screening-activate button not found");
  }
  
})
