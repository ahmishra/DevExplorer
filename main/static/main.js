// DARK MODE - ENABLE / DISABLE
let darkMode = localStorage.getItem("darkMode");
const darkModeToggle = document.querySelector("#dark-mode-toggle");

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    document.getElementById("nav").classList.add("bg-dark");
    document.getElementById("nav").classList.add("navbar-dark");


    document.body.classList.remove("lightmode");
    document.getElementById("nav").classList.add("navbar-light");
    document.getElementById("nav").classList.remove("bg-light");


    localStorage.setItem("darkMode", 'enabled');
};
const disableDarkMode = () => {
    document.body.classList.add("lightmode");
    document.getElementById("nav").classList.add("bg-light");
    document.getElementById("nav").classList.add("navbar-light");


    document.body.classList.remove("darkmode");
    document.getElementById("nav").classList.remove("navbar-dark");
    document.getElementById("nav").classList.remove("bg-dark");

    
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



// Fade Text In When Scroll
$(window).on("load", function () {
    $(window).scroll(function () {
        var windowBottom = $(this).scrollTop() + $(this).innerHeight();
        $(".fade").each(function () {
            /* Check the location of each desired element */
            var objectBottom = $(this).offset().top + $(this).outerHeight();

            /* If the element is completely within bounds of the window, fade it in */
            if (objectBottom < windowBottom) { //object comes into view (scrolling down)
                if ($(this).css("opacity") == 0) { $(this).fadeTo(200, 1); }
            } else { //object goes out of view (scrolling up)
                if ($(this).css("opacity") == 1) { $(this).fadeTo(200, 0); }
            }
        });
    }).scroll();
});

// END


// Fade in nav when scroll
$(window).scroll(function(){
    $('nav').toggleClass('scrolled', $(this).scrollTop() > 200);
});
