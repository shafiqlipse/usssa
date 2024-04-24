const popper = document.querySelector(".official-form");

const Popup = () => {
  const computedStyle = window.getComputedStyle(popper);

  // Toggle between "flex" and "none" based on the computed style
  popper.style.display = computedStyle.display === "none" ? "flex" : "none";
};
