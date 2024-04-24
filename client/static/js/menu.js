// menu toggle scripts
const navbar = document.querySelector(".navbarnav");

const menuToggle = () => {
  if (navbar.classList.contains("nav-menu-off")) {
    navbar.classList.add("nav-menu-on");
    navbar.classList.remove("nav-menu-off");
  } else {
    navbar.classList.remove("nav-menu-on");
    navbar.classList.add("nav-menu-off");
  }
  console.log(navbar.classList);
};

// mobile sports

const notifications = document.querySelector(".more");
const dropdown = document.querySelector(".chomp-nav");

notifications.addEventListener("click", () => {
  dropdown.classList.remove("none");
  console.log(dropdown.classList);
});

document.addEventListener("click", (event) => {
  const isClickInsideDropdown = dropdown.contains(event.target);
  const isClicked = notifications.contains(event.target);

  if (!isClickInsideDropdown && !isClicked) {
    dropdown.classList.add("none");
    // console.log(isClickInsideDropdown);
  }
});
