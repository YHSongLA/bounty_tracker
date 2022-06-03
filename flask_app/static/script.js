// login and registration starts
var loggle = document.getElementById("loginHide");
var roggle = document.getElementById("regisHide");

function loginToggle() {
    roggle.style.display = "none";
    if (loggle.style.display === "block") {
        loggle.style.display = "none";
    }
    else {
        loggle.style.display = "block";
    }
}

function regisToggle() {
    loggle.style.display = "none"
    if (roggle.style.display === "block") {
        roggle.style.display = "none";
    }
    else {
        roggle.style.display = "block";
    }
}
// login and registration ends

// star priority starts
document.addEventListener('DOMContentLoaded', function() {
    let stars = document.querySelectorAll('.star');
    stars.forEach(function(star) {
        star.addEventListener('click', setRating);
    });

    let rating = parseInt(document.querySelector('.stars').getAttribute('value'));
    console.log(rating);
    console.log(stars);
    let target = stars[rating - 1];
    target.dispatchEvent(new MouseEvent('click'));
});

function setRating(ev) {
    console.log(ev);
    let span = ev.currentTarget;
    let stars = document.querySelectorAll('.star');
    let match = false;
    let num = 0;
    stars.forEach(function(star, index) {
        if (match) {
            star.classList.remove('rated');
        }
        else {
            star.classList.add('rated');
        }
        if (star === span) {
            match = true;
            num = index + 1;
        }
    });
    document.querySelector('.priority').setAttribute('value', num);
}
// star priority ends