
class KeyPad extends HTMLElement {
    constructor() {
      super();
      this.showDec = true;
    }
  
    connectedCallback() {
      this.showDec = eval(this.getAttribute("showDec")) ?? true;
      console.log(this.showDec);
      this.render();
    }
    
    render() {
      
      this.innerHTML = `
        <div>
            <div class="numpad">
                <button id="numpad-1">1</button>
                <button id="numpad-2">2</button>
                <button id="numpad-3">3</button>
            </div>
            <div>
                <button id="numpad-4">4</button>
                <button id="numpad-5">5</button>
                <button id="numpad-6">6</button>
            </div>
            <div>
                <button id="numpad-7">7</button>
                <button id="numpad-8">8</button>
                <button id="numpad-9">9</button>
            </div>
            
        </div>
        `;
        if (this.showDec) {
            this.innerHTML += `
            <div>
                <button id="numpad-.">.</button>
                <button id="numpad-0">0</button>
                <button id="numpad-d">del</button>
            </div>
            `
        } else {
            this.innerHTML += `
            <div>
                <button id="numpad-0" style="margin-left:136px">0</button>
                <button id="numpad-d">del</button>
            </div>
            `
        }
    }
  }
  
customElements.define("my-keypad", KeyPad);
  
document.getElementById("numpad-1").addEventListener("click", () => addKey(1));
document.getElementById("numpad-2").addEventListener("click", () => addKey(2));
document.getElementById("numpad-3").addEventListener("click", () => addKey(3));
document.getElementById("numpad-4").addEventListener("click", () => addKey(4));
document.getElementById("numpad-5").addEventListener("click", () => addKey(5));
document.getElementById("numpad-6").addEventListener("click", () => addKey(6));
document.getElementById("numpad-7").addEventListener("click", () => addKey(7));
document.getElementById("numpad-8").addEventListener("click", () => addKey(8));
document.getElementById("numpad-9").addEventListener("click", () => addKey(9));
document.getElementById("numpad-0").addEventListener("click", () => addKey(0));
if (document.getElementById("numpad-.")) {
    document.getElementById("numpad-.").addEventListener("click", () => addDec());

}
document.getElementById("numpad-d").addEventListener("click", () => delKey());

function addKey(num) {
    console.log("pressed",num);
    let prevVal = document.getElementById("input-value").innerText;
    console.log("prevVal",prevVal);
    document.getElementById("input-value").innerHTML = prevVal + num;
    updateNextButton();
}
function addDec() {
    console.log("pressed decimal point");
    let prevVal = document.getElementById("input-value").innerText;
    console.log("prevVal",prevVal);
    if (prevVal.includes(".")) {
        console.log("already have decimal point");
    } else {
        document.getElementById("input-value").innerHTML = prevVal + ".";
    }
    updateNextButton();
}
function delKey() {
    console.log("pressed delete");
    let prevVal = document.getElementById("input-value").innerText;
    document.getElementById("input-value").innerHTML = prevVal.slice(0,-1);
    updateNextButton();
}

function updateNextButton() {
    let val = document.getElementById("input-value").innerText;
    let newButton = (val == "") ? `<button class="button-hollow">Skip</button>` : `<button>Next</button>`;
    // if (val == "") {
    //     newButton = `<button class="button-hollow">Skip</button>`;
    // } else {
    //     newButton = `<button>Next</button>`;
    // }

    // if (document.getElementById("next-bmi")) {
    //     document.getElementById("next-bmi").innerHTML = newButton;
    // } else if (document.getElementById("next-platelet")) {
    //     document.getElementById("next-platelet").innerHTML = newButton;
    // }
    document.getElementById("next").innerHTML = newButton;
}