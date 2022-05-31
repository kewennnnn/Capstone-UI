function getBMI() {
    const bmi = localStorage.getItem("bmi") ?? "";
    console.log(bmi);
    return bmi;
}
function setBMI() {
    const bmi = document.getElementById("input-value").innerHTML;
    console.log(bmi);
    localStorage.setItem("bmi",bmi);
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