const sidebar = document.querySelector(".sidebar");

const SideToggle = () => {
  // Assuming 'sidebar' is the correct reference to your sidebar element
// Replace 'yourSidebarId' with the actual ID of your sidebar

  if (sidebar.style.display === "none" || sidebar.style.display === "") {
    sidebar.style.display = "block";
  } else {
    sidebar.style.display = "none";
    console.log(sidebar);
  }
};

// Example usage:
// Add a button or any element that triggers the toggle
document.getElementById('toggleButton').addEventListener('click', SideToggle);
