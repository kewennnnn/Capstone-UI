function leftArrow(isActive, currentTipNumber, nextTipNumber) {
  let opacity = (isActive) ? "100%" : "40%";
  return (
  `<lord-icon
    src="https://cdn.lordicon.com/iifryyua.json"
    colors="primary:#ffffff"
    style="width:44px;height:44px;transform:rotate(180deg);opacity:${opacity};"
    onclick="navTip(${currentTipNumber},${nextTipNumber})">
  </lord-icon>`)
};
function rightArrow(isActive, currentTipNumber, nextTipNumber) {
  let opacity = (isActive) ? "100%" : "40%";
  return (
  `<lord-icon
    src="https://cdn.lordicon.com/iifryyua.json"
    colors="primary:#ffffff"
    style="width:44px;height:44px;opacity:${opacity};"
    onclick="navTip(${currentTipNumber},${nextTipNumber})">
  </lord-icon>`)
};

class Tooltip extends HTMLElement {
    constructor() {
      super();
      this.content1;
      this.content2;
      this.content3;
      this.tipNumber;
      this.next;
      this.prev;
    }
  
    connectedCallback() {
      this.content1 = this.getAttribute("content1") ? `<p>${this.getAttribute("content1")}</p>` : "";
      this.content2 = this.getAttribute("content2") ? `<p>${this.getAttribute("content2")}</p>` : "";
      this.content3 = this.getAttribute("content3") ?? "";
      this.tipNumber = (this.getAttribute("tipNumber")) ? parseInt(this.getAttribute("tipNumber")) : 1;
      this.numOfTips = (this.getAttribute("numOfTips")) ? parseInt(this.getAttribute("numOfTips")) : null;
      this.next = (this.tipNumber<this.numOfTips) ? (this.tipNumber+1) : null;
      this.prev = (this.tipNumber>1) ? (this.tipNumber-1) : null;
      this.position = (this.getAttribute("position")) ?? "";

      this.nav = (this.numOfTips) 
        ? `<div class="align-center">
            ${leftArrow(this.tipNumber>1, this.tipNumber, this.prev)}
            <span>${this.tipNumber} of ${this.numOfTips}</span>
            ${rightArrow(this.tipNumber<this.numOfTips, this.tipNumber, this.next)}
          </div>` 
        : "";

      this.render();
    }
    
    
  
    render() {
      this.innerHTML = `
      <div id="tooltip-popup-${this.tipNumber}" class="tooltip-popup ${this.position}">
        <lord-icon
          id="tooltip-cross-${this.tipNumber}"
          src="https://cdn.lordicon.com/vfzqittk.json"
          colors="primary:#fff">
        </lord-icon>
        ${this.content1}
        ${this.content2}
        ${this.content3}
        ${this.nav}
      </div>
      `;
      
    }
  }
  
  customElements.define("my-tooltip", Tooltip);

  var allTooltips = document.getElementsByClassName("tooltip-popup");

  function fadeTip(tipNumber=1) {
    const thisTip = document.getElementById("tooltip-popup-"+tipNumber);
    if (!thisTip) {
      console.log("Couldnt find tooltip-popup-"+tipNumber);
      return;
    }
    if (thisTip.style.opacity == 0) {
      thisTip.style.display = "block";
      setTimeout(()=>{thisTip.style.opacity = 1;}, 100);
    } else {
      thisTip.style.opacity = 0;
      setTimeout(()=>{thisTip.style.display = "none";}, 500);
    }
  }

  function toggleTips(tipNumber=1) {
    const thisTip = document.getElementById("tooltip-popup-"+tipNumber);
    if (!thisTip) {
      console.log("Couldnt find tooltip-popup-"+tipNumber);
      return;
    }
    fadeTip(tipNumber);
    for (let i=1; i<4; i++) {
      if (i != tipNumber) {
        closeTip(i);
      }
    }
  }

  function closeTip(tipNumber=1) {
    const thisTip = document.getElementById("tooltip-popup-"+tipNumber);
    if (!thisTip) {
      console.log("Couldnt find tooltip-popup-"+tipNumber);
      return;
    }
    thisTip.style.opacity = 0;
    setTimeout(()=>{thisTip.style.display = "none";}, 500);
  }

  function navTip(currentTipNumber, nextTipNumber) {
    const thisTip = document.getElementById("tooltip-popup-"+currentTipNumber);
    const nextTip = document.getElementById("tooltip-popup-"+nextTipNumber);
    if (!thisTip) {
      console.log("Couldnt find tooltip-popup-"+currentTipNumber);
      return;
    }
    if (!nextTip) {
      console.log("Couldnt find tooltip-popup-"+nextTipNumber);
      return;
    }
    
    thisTip.style.opacity = 0;
    setTimeout(()=>{thisTip.style.display = "none";}, 500);
    
    nextTip.style.display = "block";
    setTimeout(()=>{nextTip.style.opacity = 1;}, 100);
  }

  document.getElementById("pb-help").addEventListener("click", () => {toggleTips(1);});
  document.getElementById("tooltip-cross-1").addEventListener("click", () => {closeTip(1);});
  let cross2 = document.getElementById("tooltip-cross-2");
  if (cross2) cross2.addEventListener("click", () => {closeTip(2);});
  let cross3 = document.getElementById("tooltip-cross-3");
  if (cross3) cross3.addEventListener("click", () => {closeTip(3);});