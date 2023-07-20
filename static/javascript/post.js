var post_id = document.querySelector('.main-post').id
console.log(post_id)

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

sendReportButton = document.getElementById('confirm-report')
if (sendReportButton) {
    sendReportButton.addEventListener('click', e => {
        e.preventDefault()
        var reportDetails = document.getElementById('report-details').value

        var data = {
            hateful: document.querySelector('input[name="hateful"]').checked,
            spam: document.querySelector('input[name="spam"]').checked,
            violence: document.querySelector('input[name="violence"]').checked,
            explicit: document.querySelector('input[name="explicit"]').checked,
            other: document.querySelector('input[name="other"]').checked,
            other_data: reportDetails
        };

        console.log(data)

        fetch(`/post/${post_id}/report_post`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(response => {
            if (response.ok) {
                window.location.href = `/post/${post_id}`;
            } else {
                alert('Error submitting report')
            }
        }).catch(error => {
            console.log(error)
        })
    })
}

