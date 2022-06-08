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
      this.line4 = "pb-line ";
      this.stage5 = "pb-stage ";
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
      } else if (this.current > 3) {
        this.stage4 += "pb-done";
      } 
      if (this.current == 5) {
        this.stage5 += "pb-current";
      } else if (this.current < 5) {
        this.stage5 += "pb-right-margin";
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
      if (this.current > 4) {
        this.line4 += "pb-line-done ";
      } 
      if (this.current == 4 || this.current == 5) {
        this.line4 += "pb-line-short ";
      } 

      this.render();
    }
    
    
  
    render() {
      
      this.innerHTML = `
      <div id="progress-bar-wrapper">
        <div id="progress-bar" class="pb">
          <a href="./height.html"class="${this.stage1}" id="stage1">
            <p>Height</p>
            <img src="../media/none.png"/>
          </a>
          <div class="${this.line1}"></div>
          <a href="./weight.html" class="${this.stage2}" id="stage2">
            <p>Weight</p>
            <img src="../media/none.png"/>
          </a>
          <div class="${this.line2}"></div>
          <a href="./platelet.html" class="${this.stage3}" id="stage3">
            <p>Platelet</p>
            <img src="../media/none.png"/>
          </a>
          <div class="${this.line3}"></div>
          <a href="./screening.html" class="${this.stage4}" id="stage4">
            <p>Screening</p>
            <img src="../media/none.png"/>
          </a>
          <div class="${this.line4}"></div>
          <a href="./results.html" class="${this.stage5}" id="stage5">
            <p>Result</p>
            <img src="../media/none.png"/>
          </a>
        </div>
      </div>
      `;
    }
  }
  
  customElements.define("progress-bar", ProgressBar);