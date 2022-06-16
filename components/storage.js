function clearAll() {
    localStorage.removeItem("height");
    localStorage.removeItem("weight");
    localStorage.removeItem("platelet");
    localStorage.removeItem("elasticity");
    console.log("storage cleared!");
}

function getBMI() {
    // const bmi = localStorage.getItem("bmi") ?? "";
    // console.log(bmi);
    const height = getHeight() / 100; 
    const weight = getWeight(); 
    if (height=="" || weight=="") {
        return "";
    }
    const bmi = (weight / height / height).toFixed(1);
    return bmi;
}
function setBMI() { // not used since no more bmi screen
    const bmi = document.getElementById("input-value").innerHTML;
    console.log(bmi);
    localStorage.setItem("bmi",bmi);
}

function getHeight() {
    const height = localStorage.getItem("height") ?? "";
    console.log(height);
    return height;
}
function setHeight() {
    const height = document.getElementById("input-value").innerHTML;
    console.log(height);
    localStorage.setItem("height",height);
}

function getWeight() {
    const weight = localStorage.getItem("weight") ?? "";
    console.log(weight);
    return weight;
}
function setWeight() {
    const weight = document.getElementById("input-value").innerHTML;
    console.log(weight);
    localStorage.setItem("weight",weight);
}


function getPlatelet() {
    const platelet = localStorage.getItem("platelet") ?? "";
    console.log(platelet);
    return platelet;
}
function setPlatelet() {
    const platelet = document.getElementById("input-value").innerHTML;
    console.log(platelet);
    localStorage.setItem("platelet",platelet);
}

function getElasticity() {
    const elasticity = localStorage.getItem("elasticity") ?? "";
    console.log(elasticity);
    return elasticity;
}
function setElasticity() {
    // const elasticity = "";
    const elasticity = Math.floor(Math.random()*1000);
    console.log(elasticity);
    localStorage.setItem("elasticity",elasticity);
    displayElasticity();
}
function displayElasticity() {
    const elasticity = getElasticity();
    if (elasticity == "") {
        document.getElementById("input-value").innerHTML = "-";
        document.getElementById("screening-prompt").innerHTML = "Press button to get a reading from probe";
        document.getElementById("screening-done").innerHTML = `<button class="button-grey">Finish</button>`;
    } else {
        document.getElementById("input-value").innerHTML = elasticity;
        document.getElementById("screening-prompt").innerHTML = "Press button again to get another reading";
        document.getElementById("screening-done").innerHTML = `<button onclick="location.href='./results.html';">Finish</button>`;
    }
}