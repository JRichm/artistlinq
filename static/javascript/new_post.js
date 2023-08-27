const postBox = document.querySelector('.new-post-box');
const postInputBox = document.querySelector('.post-input');
const postPreviewBox = document.querySelector('.post-preview');

const fileInput = document.getElementById('fileInput');
const customFileLabel = document.querySelector('.custom-file-label');
const previewImg = document.getElementById('post-preview-img');

const postTitleInput = document.getElementById('post-title-input')
const tagSearch = document.getElementById('tag-search-input');
const tagContainer = document.getElementById('tag-list-box');

const postButton = document.getElementById('post-button')


postButton.addEventListener('click', (e) => {
  console.log('\n\n\nnew post!')

  let description = '';

  let formData = new FormData();
  formData.append('title', postTitleInput.value);
  formData.append('description', description);
  Array.from(document.getElementsByClassName('added-tag')).forEach(item => {
    formData.append('tags', item.innerText);
  });
  formData.append('file', fileInput.files[0]);

  console.log(formData);

  fetch('/publish_post', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.redirected) {
      // Redirected response, no need to handle further
      window.location.href = response.url;
    } else {
      // Handle other responses (e.g., JSON)
      window.location.href = "/"
      return response.json();
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch(err => {
    console.log(err);
  });
});


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

let timerId;  

// update tag list when user types
tagSearch.addEventListener('input', (e) => {
  var userInput = e.target.value;

  if (tagSearch.value.length <= 2) return;
  clearTags()

  // create tag element for users input
  createTagElement(userInput, 'searched-tag')

  clearTimeout(timerId);
  timerId = setTimeout(() => {

    fetch(`/search_tags?key=${encodeURIComponent(userInput)}`)
    .then(response => response.json())
    .then(data => {

      const filteredData = data.filter(item => item.name !== userInput);

        filteredData.forEach(item => {
          createTagElement(item.name, 'searched-tag');
      });
    })
    .catch(error => {
      console.error(error);
      // handle any errors
    });
  }, 250); // Delay of 1000 milliseconds (1 second)
});


// add tag when user presses enter
tagSearch.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    fetch(`/get_tag_by_name?tag=${encodeURIComponent(e.target.value)}`)
    .then(response => response.json())
    .then(data => {
      if (data.error)
        fetch(`/create_new_tag`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ tag: e.target.value })
        })
        .then(res => res.json())
        .then(dat => createTagElement(e.target.value, 'added-tag'))
    })
  // clear search when the user presses backspace and search is too short
  } else if (e.key === 'Backspace' && tagSearch.value.length <= 2) {
    clearTags();
  }
})


function clearTags() {
  // delete all elements with the 'searched-tag' class
  document.querySelectorAll('.searched-tag').forEach(e => e.remove())
}

function createTagElement(tagName, className) {
  tag = document.createElement('p');
  tag.innerText = tagName;
  tag.classList.add(className);
  tag.addEventListener('click', e => clickTag(e))
  tagContainer.appendChild(tag);
}

function clickTag(e) {
  createTagElement(e.target.innerText, 'added-tag')
  e.target.remove()
  
  fetch(`/get_tag_by_name?tag=${encodeURIComponent(e.target.innerText)}`)
    .then(response => response.json())
    .then(data => {
      if (data.error)
        fetch(`/create_new_tag`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ tag: e.target.innerText })
        })
        .then(res => res.json())
        .then(dat => {
        })
    })
}