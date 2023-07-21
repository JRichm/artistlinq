postRows = document.querySelectorAll('.problem-post-row')

postRows.forEach(element => {
    element.addEventListener('click', e => {
        post_id = e.target.id;
        if (post_id === '') {
            post_id = e.target.parentElement.id;
        }

        post_id = post_id.split('-')[1]
        window.location.href = (`/post/${post_id}`)
    })
});

userSearchButton = document.getElementById('search-user-button')
if (userSearchButton) {
    userSearchButton.addEventListener('click', adminUserSearch)
}

userSearchInput = document.getElementById('search-user-button')
if (userSearchInput) {
    userSearchButton.addEventListener('keyup', e => {
        if (e.key === 'Enter' || e.keyCode === 13)
        adminUserSearch(e)
    })
}

function adminUserSearch() {
    
    userSearchInputValue = document.getElementById('search-user-input').value
    if (userSearchInputValue.length < 6) return

    window.location.href=`/admin/user_settings/${userSearchInputValue}`
}