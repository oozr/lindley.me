// dark-mode.js

// Check if the user has set a preference for dark mode in the browser
// If the user has already set a preference, use that preference
// If not, check the time of day to decide whether to use dark mode or not
function setInitialDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");

  // Check if the user's preference is set to dark mode
  const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;

  // Check the time of day (morning or night) to decide whether to use dark mode
  const hour = new Date().getHours();
  const isNightTime = hour >= 18 || hour <= 6;

  if (prefersDarkMode || isNightTime) {
    // Enable dark mode
    document.body.classList.add("dark-mode");
    darkModeToggle.checked = true;
  }
}

// Toggle dark mode when the switch is clicked
function toggleDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const isDarkModeEnabled = darkModeToggle.checked;

  if (isDarkModeEnabled) {
    // Enable dark mode
    document.body.classList.add("dark-mode");
  } else {
    // Disable dark mode
    document.body.classList.remove("dark-mode");
  }
}

// Call the function to set the initial dark mode state
setInitialDarkMode();
