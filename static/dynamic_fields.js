document.addEventListener('DOMContentLoaded', function() {
    let searchInput = document.getElementById('quickSearchInput');
    let searchButton = document.getElementById('searchButton');
    let minRatingSelect = document.getElementById('minRating');
    let minRatingCountSlider = document.getElementById('minRatingCount');
    let sortOptionSelect = document.getElementById('sortOption');

    searchInput.addEventListener('input', event => fetchSuggestions(event.target));
    searchButton.addEventListener('click', () => performSearch(searchInput.value));
    minRatingSelect.addEventListener('change', () => updateSearchResults());
    minRatingCountSlider.addEventListener('change', () => updateSearchResults());
    sortOptionSelect.addEventListener('change', () => updateSearchResults());

    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch(searchInput.value);
        }
    });

    document.addEventListener("click", e => closeAllLists(e.target));
});

function updateSearchResults() {
    let searchTerm = document.getElementById('quickSearchInput').value;
    let minRating = document.getElementById('minRating').value;
    let minRatingCount = document.getElementById('minRatingCount').value;
    let sortOption = document.getElementById('sortOption').value;

    let searchParams = new URLSearchParams({
        q: searchTerm,
        minRating: minRating,
        minRatingCount: minRatingCount,
        sortOption: sortOption
    });

    fetch('/?'+ searchParams.toString())
        .then(response => response.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            let newResults = doc.getElementById('searchResults');
            let currentResults = document.getElementById('searchResults');
            currentResults.innerHTML = newResults.innerHTML;
        })
        .catch(error => console.error('Error updating search results:', error));
}


function fetchSuggestions(inputElement) {
    let searchTerm = inputElement.value;
    if (searchTerm.length < 1) return closeAllLists();

    fetch('/search?q=' + encodeURIComponent(searchTerm))
        .then(response => response.json())
        .then(suggestions => showSuggestions(inputElement, suggestions))
        .catch(error => console.error('Error fetching suggestions:', error));
}

function showSuggestions(inputElement, suggestions) {
    closeAllLists();
    if (!suggestions.length) return;

    let list = createList(inputElement);
    suggestions.forEach(suggestion => createListItem(inputElement, list, suggestion));
}

function createList(inputElement) {
    let list = document.createElement("DIV");
    list.setAttribute("id", inputElement.id + "autocomplete-list");
    list.setAttribute("class", "autocomplete-items");
    list.style.position = 'absolute';
    list.style.left = inputElement.getBoundingClientRect().left + 'px';
    list.style.top = (inputElement.getBoundingClientRect().top + inputElement.offsetHeight) + 'px';
    document.body.appendChild(list);
    return list;
}

function createListItem(inputElement, list, suggestion) {
    let item = document.createElement("DIV");
    item.innerHTML = highlightTerm(inputElement.value, suggestion);
    item.addEventListener("click", () => {
        performSearch(suggestion);
        closeAllLists();
    });
    list.appendChild(item);
}

function highlightTerm(term, text) {
    return text.replace(new RegExp("(" + term + ")", "gi"), "<strong>$1</strong>");
}

function closeAllLists(elmnt) {
    let items = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < items.length; i++) {
        if (elmnt != items[i]) items[i].parentNode.removeChild(items[i]);
    }
}

function performSearch(searchTerm) {
    if (searchTerm.length > 0) {
        window.location.href = '/?q=' + encodeURIComponent(searchTerm);
    }
}
