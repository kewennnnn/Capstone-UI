const goodIcon = `
    <lord-icon
        src="https://cdn.lordicon.com/epurqyya.json"
        trigger="loop"
        colors="primary:#16c72e"
        style="width:50px;height:50px;padding-left:30px;">
    </lord-icon>`;

const badIcon = `
    <lord-icon
        src="https://cdn.lordicon.com/rslnizbt.json"
        trigger="loop"
        colors="primary:#e83a30"
        style="width:50px;height:50px;padding-left:30px;">
    </lord-icon>`;

function displayResults() {
    let plateletResult = getPlatelet();
    let elasticityResult = getElasticity();
    
    let MLResult = "high"; //TODO: give ML platelet and elasticity, then get MLResult here
    switch (MLResult) {
        case "high":
            document.getElementById("result-stage").innerHTML = "Stage F3/F4";
            document.getElementById("result-advice").innerHTML = "Please refer to specialist";
            break;
        case "med":
            document.getElementById("result-stage").innerHTML = "Stage F2/F3";
            document.getElementById("result-advice").innerHTML = "Please refer to specialist";
            break;
        default:
            document.getElementById("result-stage").innerHTML = "Stage F0/F1";
            document.getElementById("result-advice").innerHTML = "Patient has low risk of liver issues";
            break;
    }
    

}

function displayPlatelet(resultCase="good") {
    let resultDisplay = document.getElementById("platelet-result");
    let plateletResult = getPlatelet();
    if (plateletResult == "") {
        resultDisplay.innerHTML = "NA";
        document.getElementById("platelet-section").style.borderColor = "var(--blue)";
        return;
    } 
    resultDisplay.innerHTML = plateletResult;
    switch (resultCase) { //TODO: use ML to get resultCase
        case "good":
            document.getElementById("platelet-section").style.borderColor = "var(--green)";
            document.getElementById("platelet-icon").innerHTML = goodIcon;
            document.getElementById("platelet-details").innerHTML = "Normal liver function. However, low platelet count may indicate other health issues.";
            break;
        case "bad":
            document.getElementById("platelet-section").style.borderColor = "var(--red)";
            document.getElementById("platelet-icon").innerHTML = badIcon;
        default: 
            break;
    }
}

function displayElasticity() {
    document.getElementById("elasticity-result").innerHTML = getElasticity();
    if (document.getElementById("elasticity-result").innerHTML == "") {
        document.getElementById("elasticity-result").innerHTML = "NA";
        document.getElementById("elasticity-section").style.borderColor = "var(--blue)";
    } else {
        console.log(document.getElementById("elasticity-result").innerHTML);
        document.getElementById("elasticity-section").style.borderColor = "var(--red)";
        document.getElementById("elasticity-icon").innerHTML = `
            <lord-icon
                src="https://cdn.lordicon.com/rslnizbt.json"
                trigger="loop"
                colors="primary:#e83a30"
                style="width:50px;height:50px;padding-left:30px;">
            </lord-icon>`
    }
}