// Function to set dark mode and update toggle state
function setDarkModePreference(enabled) {
  const darkModeToggle = document.getElementById("darkModeToggle");
  if (enabled) {
    document.documentElement.classList.add("dark-mode");
    darkModeToggle.checked = true;
    localStorage.setItem("darkMode", "enabled");
  } else {
    document.documentElement.classList.remove("dark-mode");
    darkModeToggle.checked = false;
    localStorage.setItem("darkMode", "disabled");
  }
}

// Toggle dark mode when the switch is clicked
function toggleDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  setDarkModePreference(darkModeToggle.checked);
}

// Function to set the initial dark mode state
function setInitialDarkMode() {
  const darkModeToggle = document.getElementById("darkModeToggle");
  const storedPreference = localStorage.getItem("darkMode");
  const hour = new Date().getHours();
  const isNightTime = hour >= 18 || hour <= 6;

  // Sync the toggle with the current state
  if (document.documentElement.classList.contains("dark-mode")) {
    darkModeToggle.checked = true;
  } else if (storedPreference === "disabled") {
    setDarkModePreference(false);
  } else if (isNightTime && storedPreference === null) {
    setDarkModePreference(true);
  }
}

// Call the function to set the initial dark mode state when DOM is ready
document.addEventListener("DOMContentLoaded", setInitialDarkMode);