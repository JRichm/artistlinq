const likeButton = document.querySelector('.like-button');
const favoriteButton = document.querySelector('.favorite-button');
const starButton = document.querySelector('.star-button');

if (userLikes[0]) {
    likeButton.classList.remove('like-button');
    likeButton.classList.add('like-button-pressed');
}

if (userLikes[1]) {
    favoriteButton.classList.remove('favorite-button');
    favoriteButton.classList.add('favorite-button-pressed');
}

if (userLikes[2]) {
    starButton.classList.remove('star-button');
    starButton.classList.add('star-button-pressed');
}

function autoResize() {
    const textarea = document.getElementById("new-comment-input");
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

reportButton = document.getElementById('report-post')
if (reportButton) {
    reportButton.addEventListener('click', e => {
        e.preventDefault()
        document.getElementById('report-menu-screen').classList.remove('hidden')
    })
}

closeReportButton = document.getElementById('report-menu-close')
if (closeReportButton) {
    closeReportButton.addEventListener('click', e => {
        e.preventDefault()
        document.getElementById('report-menu-screen').classList.add('hidden')
    })
}