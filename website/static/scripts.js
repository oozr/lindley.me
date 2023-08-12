// dark-mode.js

// Function to set dark mode and update toggle state
function setDarkModePreference(enabled) {
  const darkModeToggle = document.getElementById("darkModeToggle");
  if (enabled) {
    document.body.classList.add("dark-mode");
    darkModeToggle.checked = true;
    localStorage.setItem("darkMode", "enabled");
  } else {
    document.body.classList.remove("dark-mode");
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
  
  if (storedPreference === "enabled") {
    setDarkModePreference(true);
  } else if (storedPreference === "disabled") {
    setDarkModePreference(false);
  } else {
    // Check if the user's preference is set to dark mode
    const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
    // Check the time of day (morning or night) to decide whether to use dark mode
    const hour = new Date().getHours();
    const isNightTime = hour >= 18 || hour <= 6;
    
    if (prefersDarkMode || isNightTime) {
      setDarkModePreference(true);
    } else {
      setDarkModePreference(false);
    }
  }
}

// Call the function to set the initial dark mode state
setInitialDarkMode();
