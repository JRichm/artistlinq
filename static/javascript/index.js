searchBar = document.getElementById('search-bar');
searchButton = document.getElementById('search-button');

searchButton.addEventListener('click', e => {
  if (searchBar.value) {
    searchTags(searchBar.value)
  }
})

searchBar.addEventListener('keypress', e => {
  if (e.key === 'Enter') {
    searchTags(e.target.value)
  }
})


function searchTags(searchValue) {
  console.log(searchValue)
  
  window.location.href = `/search/${searchValue}`
}

homeButton = document.getElementById('home-button');
homeButton.addEventListener('click', e => {
  window.location.href = '/'
})

postButton = document.getElementById('post-button');
postButton.addEventListener('click', e => {
  window.location.href = '/new_post'
})

messagesButton = document.getElementById('messages-button');


settingsButton = document.getElementById('settings-button');
loginButton = document.getElementById('login-button');