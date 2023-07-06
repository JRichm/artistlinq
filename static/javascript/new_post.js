


const postBox = document.querySelector('.new-post-box');
const postInputBox = document.querySelector('.post-input');
const postPreviewBox = document.querySelector('.post-preview');

const fileInput = document.getElementById('fileInput');
const customFileLabel = document.querySelector('.custom-file-label');
const previewImg = document.getElementById('post-preview-img');

const tagSearch = document.getElementById('tag-search-input');
const tagContainer = document.getElementById('tag-list-box');

// show preview of file after uploading
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

// update tag list when user types
tagSearch.addEventListener('input', (e) => {
    var userInput = e.target.value;

    fetch(`/search_tags?key=${encodeURIComponent(userInput)}`)
    .then(response => response.json())
    .then(data => {
      console.log(tagContainer.firstChild);
      // delete all child elements from tag box
      while (tagContainer.firstChild) {
        tagContainer.removeChild(tagContainer.firstChild)
      }
      // create element for each tag in the data array
      data.forEach(item => {
        console.log(item);
        tag = document.createElement('p');
        tag.innerText = item.name;
        tag.classList.add('searched-tag');
        tagContainer.appendChild(tag);
      });
    })
    .catch(error => {
      console.error(error);
      // handle any errors
    });
});