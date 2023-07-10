function autoResize() {
    const textarea = document.getElementById("new-comment-input");
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

likeButton = document.getElementById('like-button')
favoriteButton = document.getElementById('favorite-button')
starButton = document.getElementById('star-button')

// like button click
likeButton.addEventListener('click', e => {
    e.preventDefault()

    if (e.target.value == 'false') {
        e.target.classList.remove('like-button')
        e.target.classList.add('like-button-pressed')
        e.target.value = 'true';
    } else {
        e.target.classList.remove('like-button-pressed')
        e.target.classList.add('like-button')
        e.target.value = 'false';
    }
})

// like button click
favoriteButton.addEventListener('click', e => {
    e.preventDefault()

    if (e.target.value == 'false') {
        e.target.classList.remove('favorite-button')
        e.target.classList.add('favorite-button-pressed')
        e.target.value = 'true';
    } else {
        e.target.classList.remove('favorite-button-pressed')
        e.target.classList.add('favorite-button')
        e.target.value = 'false';
    }
})

// like button click
starButton.addEventListener('click', e => {
    e.preventDefault()

    if (e.target.value == 'false') {
        e.target.classList.remove('star-button')
        e.target.classList.add('star-button-pressed')
        e.target.value = 'true';
    } else {
        e.target.classList.remove('star-button-pressed')
        e.target.classList.add('star-button')
        e.target.value = 'false';
    }
})