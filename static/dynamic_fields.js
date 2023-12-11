document.addEventListener('DOMContentLoaded', function() {
    let searchInput = document.getElementById('quickSearchInput');
    let searchButton = document.getElementById('searchButton');

    searchInput.addEventListener('input', event => fetchSuggestions(event.target));
    searchButton.addEventListener('click', () => performSearch(searchInput.value));
    document.addEventListener("click", e => closeAllLists(e.target));
});

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
        window.location.href = '/search-results?q=' + encodeURIComponent(searchTerm);
    }
}