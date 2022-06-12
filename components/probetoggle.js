class ProbeToggle extends HTMLElement {
    constructor() {
      super();
      // this.current = 0;
    }
  
    connectedCallback() {
      // this.current = this.getAttribute("current");

      this.render();
    }
    
    
  
    render() {
      
      this.innerHTML = `
      <div id="probe-toggle" class="section flex-row">
        <h2 class="no-margin">Probe Size:</h2>
        <div>
          <button>M</button>
          <button>XL</button>
        </div>
      </div>
      `;
    }
  }
  
  customElements.define("probe-toggle", ProbeToggle);