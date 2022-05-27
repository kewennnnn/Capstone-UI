class ProgressBar extends HTMLElement {
    constructor() {
      super();
      this.current = 0;

      // switch(this.current) {
      //   case 1: 
      //     this.
      //     break; 
          
      // }
    }
  
    connectedCallback() {
      this.current = this.getAttribute("current");
      this.color1 = "orange";
      this.color2 = (this.current > 1) ? "orange" : "black";
      this.color3 = (this.current > 2) ? "orange" : "black";
      this.color4 = (this.current > 3) ? "orange" : "black";
      this.render();
    }
    
    
  
    render() {
      
      this.innerHTML = `
      <div id="progress-bar-wrapper">
        <div id="progress-bar" class="pb">
          <div class="pb-stage pb-done">
            <img src="../media/bmi.png"/>
            <p>BMI</p>
          </div>
          <div class="pb-line pb-line-done"></div>
          <div class="pb-stage pb-current">
            <img src="../media/platelet.png"/>
            <p>Platelet</p>
          </div>
          <div class="pb-line"></div>
          <div class="pb-stage">
            <img src="../media/screening.png"/>
            <p>Screen</p>
          </div>
          <div class="pb-line"></div>
          <div class="pb-stage">
            <img src="../media/diagnosis.png"/>
            <p>Result</p>
          </div>
        </div>
      </div>
      `;
        // <div id="progress-bar">
        //   <h1 style="color:${this.color1}">BMI</h1>
        //   <h1 style="color:${this.color2}">Platelet</h1>
        //   <h1 style="color:${this.color3}">Screen</h1>
        //   <h1 style="color:${this.color4}">Results</h1>
        // </div>
    }
  }
  
  customElements.define("progress-bar", ProgressBar);