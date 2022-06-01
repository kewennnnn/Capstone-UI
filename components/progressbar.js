class ProgressBar extends HTMLElement {
    constructor() {
      super();
      this.current = 0;
      this.stage1 = "pb-stage ";
      this.line1 = "pb-line ";
      this.stage2 = "pb-stage ";
      this.line2 = "pb-line ";
      this.stage3 = "pb-stage ";
      this.line3 = "pb-line ";
      this.stage4 = "pb-stage ";
    }
  
    connectedCallback() {
      this.current = this.getAttribute("current");
      
      // style for stage 
      if (this.current == 1) {
        this.stage1 += "pb-current";
      } else if (this.current > 1) {
        this.stage1 += "pb-done";
      } 
      if (this.current == 2) {
        this.stage2 += "pb-current";
      } else if (this.current > 2) {
        this.stage2 += "pb-done";
      } 
      if (this.current == 3) {
        this.stage3 += "pb-current";
      } else if (this.current > 3) {
        this.stage3 += "pb-done";
      } 
      if (this.current == 4) {
        this.stage4 += "pb-current";
      } 

      // style for lines 
      if (this.current > 1) {
        this.line1 += "pb-line-done";
      } 
      if (this.current > 2) {
        this.line2 += "pb-line-done";
      } 
      if (this.current > 3) {
        this.line3 += "pb-line-done";
      } 

      this.render();
    }
    
    
  
    render() {
      
      this.innerHTML = `
      <div id="progress-bar-wrapper">
        <div id="progress-bar" class="pb">
          <div class="${this.stage1}">
            <img src="../media/bmi.png"/>
            <p>BMI</p>
          </div>
          <div class="${this.line1}"></div>
          <div class="${this.stage2}">
            <img src="../media/platelet.png"/>
            <p>Platelet</p>
          </div>
          <div class="${this.line2}"></div>
          <div class="${this.stage3}">
            <img src="../media/screening.png"/>
            <p>Screen</p>
          </div>
          <div class="${this.line3}"></div>
          <div class="${this.stage4}">
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