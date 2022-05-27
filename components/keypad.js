
class KeyPad extends HTMLElement {
    constructor() {
      super();
      this.current = 0;
    }
  
    connectedCallback() {
      this.current = this.getAttribute("current");
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

function addKey(num) {
    console.log("pressed",num);
    let prevVal = document.getElementById("input-value").innerText;
    console.log("prevVal",prevVal);
    document.getElementById("input-value").innerHTML = prevVal + num;
}
