const mainSection = document.querySelector('.main-section')
const userNav = document.getElementById('user-nav');
const showcaseDiv = document.getElementById('showcase');
const gallaryDiv = document.getElementById('gallary');
const commissionDiv = document.getElementById('commission');

const userViews = [
    showcaseDiv,
    gallaryDiv,
    commissionDiv
]

var currentPage;

for (var child of userNav.children) {
    child.addEventListener('click', onUserNavClick)
}

function onUserNavClick(e) {
    buttonName = e.target.innerHTML.toLowerCase()

    if (buttonName == currentPage) return

    userViews.forEach(div => {
        div.classList.add('hidden')
    })

    switch (true) {
        case buttonName == 'showcase':
            currentPage = 'showcase'
            showcaseDiv.classList.remove('hidden')
            break;
        case buttonName == 'gallary':
            currentPage = 'gallary'
            gallaryDiv.classList.remove('hidden')
            break;
        case buttonName == 'commission':
            currentPage = 'commission'
            commissionDiv.classList.remove('hidden')
            break;
    }
}