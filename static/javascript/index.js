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

  fetch(`/search/${searchValue}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(err => console.log(err))
}