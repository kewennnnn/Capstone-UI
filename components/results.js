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

function fakeML(plateletResult, elasticityResult) {
    boundaryPlatelet = elasticityResult*60 - 240;
    console.log(boundaryPlatelet);
    let MLResult = 50 + (boundaryPlatelet - plateletResult)/10;
    if (MLResult > 100) {
        return 94;
    }
    return Math.floor(MLResult);
}

function displayResults() {
    let elasticityResult = getElasticity();
    let plateletResult = getPlatelet();
    console.log(plateletResult, elasticityResult);

    if (elasticityResult=="") {
        document.getElementById("result-col").innerHTML = "<h3>Please take elasticity reading to get a generated diagnosis</h3>";
        return;
    }
    
    //TODO: give ML platelet and elasticity, then get MLResult here in terms of confidence score for cirrhosis class
    let MLResult = fakeML(plateletResult, elasticityResult);

    // let MLResult = "high"; 
    // switch (MLResult) {
    //     case "high":
    //         document.getElementById("result-stage").innerHTML = "Stage F3/F4";
    //         document.getElementById("result-advice").innerHTML = "Please refer to specialist";
    //         break;
    //     case "med":
    //         document.getElementById("result-stage").innerHTML = "Stage F2/F3";
    //         document.getElementById("result-advice").innerHTML = "Please refer to specialist";
    //         break;
    //     default:
    //         document.getElementById("result-stage").innerHTML = "Stage F0/F1";
    //         document.getElementById("result-advice").innerHTML = "Patient has low risk of liver issues";
    //         break;
    // }

    if (MLResult >= 50) {
        document.getElementById("result-stage").innerHTML = MLResult+"% (High)";
        document.getElementById("result-advice").innerHTML = "Please refer to specialist";
    } else if (MLResult >= 30) {
        document.getElementById("result-stage").innerHTML = MLResult+"% (Moderate)";
        document.getElementById("result-advice").innerHTML = "Consider referral to specialist";
    } else {
        document.getElementById("result-stage").innerHTML = MLResult+"% (Low)";
        document.getElementById("result-advice").innerHTML = "Specialist referral not required";
    }
    document.getElementById("result-bar-pointer").style.left = MLResult+"%";

    displayPlatelet(plateletResult>150 ? "good" : "bad");
    displayElasticity(elasticityResult<8 ? "good" : "bad");
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
            document.getElementById("platelet-details").innerHTML = "Platelet count is in a healthy range.";
            break;
        case "bad":
            document.getElementById("platelet-section").style.borderColor = "var(--red)";
            document.getElementById("platelet-icon").innerHTML = badIcon;
            document.getElementById("platelet-details").innerHTML = "Low platelet count may indicate health issues, including fatty liver.";
        default: 
            break;
    }
}

function displayElasticity(resultCase="good") {
    let resultDisplay = document.getElementById("elasticity-result");
    let elasticityResult = getElasticity();
    if (elasticityResult == "") {
        resultDisplay.innerHTML = "NA";
        document.getElementById("elasticity-section").style.borderColor = "var(--blue)";
        return;
    } 
    resultDisplay.innerHTML = elasticityResult;
    switch (resultCase) { //TODO: use ML to get resultCase
        case "good":
            document.getElementById("elasticity-section").style.borderColor = "var(--green)";
            document.getElementById("elasticity-icon").innerHTML = goodIcon;
            document.getElementById("elasticity-details").innerHTML = "Liver stiffness is in a healthy range.";
            break;
        case "bad":
            document.getElementById("elasticity-section").style.borderColor = "var(--red)";
            document.getElementById("elasticity-icon").innerHTML = badIcon;
            document.getElementById("elasticity-details").innerHTML = "Liver is relatively stiff, likely due to high fat composition.";
        default: 
            break;
    }

    // document.getElementById("elasticity-result").innerHTML = getElasticity();
    // if (document.getElementById("elasticity-result").innerHTML == "") {
    //     document.getElementById("elasticity-result").innerHTML = "NA";
    //     document.getElementById("elasticity-section").style.borderColor = "var(--blue)";
    // } else {
    //     console.log(document.getElementById("elasticity-result").innerHTML);
    //     document.getElementById("elasticity-section").style.borderColor = "var(--red)";
    //     document.getElementById("elasticity-icon").innerHTML = `
    //         <lord-icon
    //             src="https://cdn.lordicon.com/rslnizbt.json"
    //             trigger="loop"
    //             colors="primary:#e83a30"
    //             style="width:50px;height:50px;padding-left:30px;">
    //         </lord-icon>`
    // }
}