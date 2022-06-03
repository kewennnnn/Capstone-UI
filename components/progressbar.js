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
        this.stage1 += "pb-done pb-left-margin";
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
      } else if (this.current < 4) {
        this.stage4 += "pb-right-margin";
      }

      // style for lines 
      if (this.current > 1) {
        this.line1 += "pb-line-done ";
      } 
      if (this.current == 1 || this.current == 2) {
        this.line1 += "pb-line-short ";
      } 
      if (this.current > 2) {
        this.line2 += "pb-line-done ";
      } 
      if (this.current == 2 || this.current == 3) {
        this.line2 += "pb-line-short ";
      } 
      if (this.current > 3) {
        this.line3 += "pb-line-done ";
      } 
      if (this.current == 3 || this.current == 4) {
        this.line3 += "pb-line-short ";
      } 


      this.render();
    }
    
    
  
    render() {
      
      this.innerHTML = `
      <div id="progress-bar-wrapper">
        <div id="progress-bar" class="pb">
          <div class="${this.stage1}">
            <p>BMI</p>
            <img src="../media/bmi.png"/>
          </div>
          <div class="${this.line1}"></div>
          <div class="${this.stage2}">
            <p>Platelet</p>
            <img src="../media/platelet.png"/>
          </div>
          <div class="${this.line2}"></div>
          <div class="${this.stage3}">
            <p>Screen</p>
            <img src="../media/screening.png"/>
          </div>
          <div class="${this.line3}"></div>
          <div class="${this.stage4}">
            <p>Result</p>
            <img src="../media/diagnosis.png"/>
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