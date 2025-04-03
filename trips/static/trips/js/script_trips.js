document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector("#navbarToggle");
    const mainContent = document.querySelector("main"); // Adjust this if your main content uses a different tag

    navbarToggler.addEventListener("click", function () {
      setTimeout(() => {
        if (navbarCollapse.classList.contains("show")) {
            console.log('show');
          mainContent.style.marginTop = "320px"; // Adjust based on navbar height
        } else {
            console.log('hide');
          mainContent.style.marginTop = "0px";
        }
      }, 500); // Delay to ensure class changes first
    });
  });
