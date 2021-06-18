// DARK MODE - ENABLE / DISABLE
let darkMode = localStorage.getItem("darkMode");
const darkModeToggle = document.querySelector("#dark-mode-toggle");

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    document.body.classList.remove("lightmode");
    localStorage.setItem("darkMode", 'enabled');
};
const disableDarkMode = () => {
    document.body.classList.add("lightmode");
    document.body.classList.remove("darkmode");
    localStorage.setItem("darkMode", 'disabled');
};

if (darkMode === 'enabled') {
    enableDarkMode();
}

darkModeToggle.addEventListener('click', () => {
    darkMode = localStorage.getItem("darkMode");
    if (darkMode !== 'enabled') {
        enableDarkMode();
        console.log(darkMode);
    } else {
        disableDarkMode();
        console.log(darkMode);
    }
});
// END
