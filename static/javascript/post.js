const likeButton = document.querySelector('.like-button');
const favoriteButton = document.querySelector('.favorite-button');
const starButton = document.querySelector('.star-button');

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