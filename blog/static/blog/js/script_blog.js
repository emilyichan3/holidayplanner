
document.addEventListener("submit", function(event) {
  let form = event.target;
  let inputs = form.querySelectorAll("input[name]");
  
  inputs.forEach(input => {
      if (!input.value.trim()) {
          input.removeAttribute("name");  // Removes empty inputs from URL
      }
  });
});

addEventListener('load', init);
