class Tooltip extends HTMLElement {
    constructor() {
      super();
      this.content1;
      this.content2;
      this.tipNumber;
    }
  
    connectedCallback() {
      this.content1 = this.getAttribute("content1");
      this.content2 = this.getAttribute("content2");
      this.tipNumber = this.getAttribute("tipNumber") ?? 1;

      this.render();
    }
    
    
  
    render() {
      this.innerHTML = `
      <div id="tooltip-popup">
        <lord-icon
          id="tooltip-cross"
          src="https://cdn.lordicon.com/vfzqittk.json"
          colors="primary:#fff">
        </lord-icon>
        <p>${this.content1}</p>
        <p>${this.content2}</p>
      </div>
      `;
      
    }
  }
  
  customElements.define("my-tooltip", Tooltip);

  document.getElementById("pb-help").addEventListener("click", () => {
    if (document.getElementById("tooltip-popup").style.opacity == 0) {
      document.getElementById("tooltip-popup").style.display = "block";
      setTimeout(()=>{document.getElementById("tooltip-popup").style.opacity = 1;}, 100)
    } else {
      document.getElementById("tooltip-popup").style.opacity = 0;
      setTimeout(()=>{document.getElementById("tooltip-popup").style.display = "none";}, 500)
    }
  });
  document.getElementById("tooltip-cross").addEventListener("click", () => {
    document.getElementById("tooltip-popup").style.opacity = 0;
    setTimeout(()=>{document.getElementById("tooltip-popup").style.display = "none";}, 500)
  });