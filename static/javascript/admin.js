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