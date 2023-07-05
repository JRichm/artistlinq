
const postBox = document.querySelector('.new-post-box');
const postInputBox = document.querySelector('.post-input');
const postPreviewBox = document.querySelector('.post-preview');

const fileInput = document.getElementById('fileInput');
const customFileLabel = document.querySelector('.custom-file-label');
const previewImg = document.getElementById('post-preview-img');

fileInput.addEventListener('change', function() {

    // TODO add filetype verification

    if (fileInput.files.length <= 0) {
        customFileLabel.textContent = 'Drag file here';
    } else {

        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            previewImg.src = e.target.result;
        } 

        reader.readAsDataURL(file);

        postInputBox.classList.add('hidden');
        postPreviewBox.classList.remove('hidden');
    }
});