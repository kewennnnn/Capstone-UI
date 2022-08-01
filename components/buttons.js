function backButton(text="Back") {
    return (
    `<button class="button-secondary">
        <lord-icon
            src="https://cdn.lordicon.com/iifryyua.json"
            colors="primary:#ffffff"
            style="width:44px;height:44px;transform:rotate(180deg);">
        </lord-icon>
        ${text}
    </button>`)
}

function skipButton() {
    return (
    `<button class="button-secondary" style="width:270px">
        Skip
        <lord-icon
            src="https://cdn.lordicon.com/iifryyua.json"
            colors="primary:#ffffff"
            style="width:44px;height:44px;">
        </lord-icon>
    </button>`)
}

function nextButton(text="Next") {
    return (
    `<button style="width:270px">
        ${text}
        <script src="https://cdn.lordicon.com/xdjxvujz.js"></script>
        <lord-icon
            src="https://cdn.lordicon.com/iifryyua.json"
            trigger="loop"
            colors="primary:#ffffff"
            state="hover-1"
            style="width:44px;height:44px;">
        </lord-icon>
    </button>`)
}

function finishButton(active) {
    console.log("finish",active);
    if (!active) {
        return (
        `<button class="button-grey">
            Next
            <lord-icon
                src="https://cdn.lordicon.com/iifryyua.json"
                colors="primary:#ffffff"
                style="width:44px;height:44px;">
            </lord-icon>
        </button>`)
    }
        
    return (
    `<button onclick="location.href='./results.html';">
        Next
        <script src="https://cdn.lordicon.com/xdjxvujz.js"></script>
        <lord-icon
            src="https://cdn.lordicon.com/iifryyua.json"
            trigger="loop"
            colors="primary:#ffffff"
            state="hover-1"
            style="width:44px;height:44px;">
        </lord-icon>
    </button>`)
    
}