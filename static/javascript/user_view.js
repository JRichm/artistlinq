const mainSection = document.querySelector('.main-section')
const userNav = document.getElementById('user-nav');
const showcaseDiv = document.getElementById('showcase');
const galleryDiv = document.getElementById('gallery');
const commissionDiv = document.getElementById('commission');

const showcaseNav = document.getElementById('showcaseNav')
const galleryNav = document.getElementById('galleryNav')
const commissionNav = document.getElementById('commissionNav')

const followButton = document.getElementById('follow-button')

const userViews = [
    showcaseDiv,
    galleryDiv,
    commissionDiv
]

var currentPage;

for (var child of userNav.children) {
    child.addEventListener('click', onUserNavClick)
}

function onUserNavClick(e) {
    buttonName = e.target.innerHTML.toLowerCase()

    if (buttonName == currentPage) return
    else {
        changeViews(buttonName)
    }
}

function changeViews(changeToName) {
    for (var child of userNav.children) {
        child.classList.remove('nav-button-highlighted')
    }

    userViews.forEach(div => {
        div.classList.add('hidden')
    })

    switch (true) {
        case changeToName == 'showcase':
            currentPage = 'showcase'
            showcaseDiv.classList.remove('hidden')
            showcaseNav.classList.add('nav-button-highlighted')
            break;
        case changeToName == 'gallery':
            currentPage = 'gallery'
            galleryDiv.classList.remove('hidden')
            galleryNav.classList.add('nav-button-highlighted')
            break;
        case changeToName == 'commission':
            currentPage = 'commission'
            commissionDiv.classList.remove('hidden')
            commissionNav.classList.add('nav-button-highlighted')
            break;
    }
}

changeViews('gallery')
if (followButton) {
    followButton.title = 'follow'
    
    followButton.addEventListener('click', e => {
        if (followButton.value == 'true') {
            followButton.innerHTML = 'Follow'
            followButton.id = 'follow-button'
            followButton.value = 'false'
            followButton.title = 'follow'
    
        }
        else if (followButton.value == 'false') {
            followButton.innerHTML = '<i class="fa-solid fa-check"></i>'
            followButton.id = 'followed-button'
            followButton.value = 'true'
            followButton.title = 'already following user'
        }
    })
}