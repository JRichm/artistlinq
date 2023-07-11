function autoResize() {
    const textarea = document.getElementById("new-comment-input");
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

document.getElementById('post-buttons').addEventListener('submit', e => {
    console.log('fart')
})