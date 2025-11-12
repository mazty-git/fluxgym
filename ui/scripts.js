/**
 * FluxGym Custom JavaScript
 * Handles autoscroll, debounced refresh, and training button state
 */

function() {
    // Autoscroll functionality for training logs
    let autoscroll = document.querySelector("#autoscroll")

    // Clear any existing interval
    if (window.iidxx) {
        window.clearInterval(window.iidxx);
    }

    // Check for training output and handle autoscroll
    window.iidxx = window.setInterval(function() {
        let text = document.querySelector(".codemirror-wrapper .cm-line").innerText.trim()
        let img = document.querySelector("#logo")

        if (text.length > 0) {
            autoscroll.classList.remove("hidden")

            if (autoscroll.classList.contains("on")) {
                autoscroll.textContent = "Autoscroll ON"
                window.scrollTo(0, document.body.scrollHeight, { behavior: "smooth" });
                img.classList.add("rotate")
            } else {
                autoscroll.textContent = "Autoscroll OFF"
                img.classList.remove("rotate")
            }
        }
    }, 500);

    console.log("autoscroll", autoscroll)

    // Toggle autoscroll on click
    autoscroll.addEventListener("click", (e) => {
        autoscroll.classList.toggle("on")
    })

    /**
     * Debounce utility function
     * Delays function execution until after a specified time has elapsed
     */
    function debounce(fn, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => fn(...args), delay);
        };
    }

    /**
     * Handle refresh on input change
     * Debounced to avoid excessive updates
     */
    function handleClick() {
        console.log("refresh")
        document.querySelector("#refresh").click();
    }

    const debouncedClick = debounce(handleClick, 1000);
    document.addEventListener("input", debouncedClick);

    /**
     * Update training button state when clicked
     */
    document.querySelector("#start_training").addEventListener("click", (e) => {
        e.target.classList.add("clicked")
        e.target.innerHTML = "Training..."
    })
}
