// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('toggle-mode');
    if (btn) {
        btn.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
        });
    }
});

// Weather Background Function
function setWeatherBackground(description) {
    const bgDiv = document.getElementById('background-animation');
    let bgHTML = '';
    description = description ? description.toLowerCase() : '';

    if (description.includes('rain')) {
        bgHTML = `<img src="https://media.giphy.com/media/26xBwdIuBJiCqSsBW/giphy.gif" alt="Rain">`;
    } else if (description.includes('clear')) {
        bgHTML = `<img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" alt="Clear">`;
    } else if (description.includes('cloud')) {
        bgHTML = `<img src="https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif" alt="Clouds">`;
    } else if (description.includes('snow')) {
        bgHTML = `<img src="https://media.giphy.com/media/xT0GqFzH6F0XWQj2xO/giphy.gif" alt="Snow">`;
    } else {
        bgHTML = `<img src="https://media.giphy.com/media/3oEjHGrVGrqgFFknfO/giphy.gif" alt="Weather">`;
    }
    bgDiv.innerHTML = bgHTML;
}
