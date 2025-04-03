document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector("#navbarToggle");
    const mainContent = document.querySelector("main"); // Adjust this if your main content uses a different tag

    navbarToggler.addEventListener("click", function () {
        // Wait for the class to be applied
        setTimeout(() => {
            if (navbarCollapse.classList.contains("show")) {
                // If user is logged in, move the main content down fully
                if (isUserLoggedIn) {
                    mainContent.style.marginTop = "350px"; // Adjust as needed based on navbar height
                } else {
                    // If the user is not logged in, move content down by half the height
                    mainContent.style.marginTop = "210px"; // Half of the navbar height
                }
            } else {
                mainContent.style.marginTop = "0"; // Reset margin when collapsed
            }
        }, 400); // Adjust the delay if needed
    });
});