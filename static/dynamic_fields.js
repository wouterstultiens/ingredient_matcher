document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    const searchInput = document.getElementById('quickSearchInput');
    const searchButton = document.getElementById('searchButton');
    const minRatingCountInput = document.getElementById('minRatingCount');
    const sortOptionSelect = document.getElementById('sortOption');

    searchInput.addEventListener('input', event => fetchSuggestionsAsync(event.target));
    searchButton.addEventListener('click', () => performSearchAsync(searchInput.value));
    minRatingCountInput.addEventListener('change', () => updateSearchResultsAsync());
    sortOptionSelect.addEventListener('change', () => updateSearchResultsAsync());
    document.addEventListener("click", e => closeAllLists(e.target));
}

async function updateSearchResultsAsync() {
    const searchTerm = document.getElementById('quickSearchInput').value;
    const minRatingCount = document.getElementById('minRatingCount').value;
    const sortOption = document.getElementById('sortOption').value;

    const searchParams = new URLSearchParams({
        q: searchTerm,
        minRatingCount: minRatingCount,
        sortOption: sortOption
    });

    const gridContainer = document.getElementById('searchResults');
    gridContainer.innerHTML = '<div class="loader-container"><div class="loader"></div></div>';
    gridContainer.style.height = '100vh';

    try {
        const response = await fetch('/?' + searchParams.toString());
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newResults = doc.getElementById('searchResults');
        gridContainer.innerHTML = newResults.innerHTML;
        gridContainer.style.height = 'auto';
    } catch (error) {
        console.error('Error updating search results:', error);
        gridContainer.innerHTML = '<p>Error loading recipes. Please try again.</p>';
        gridContainer.style.height = 'auto';
    }
}

async function fetchSuggestionsAsync(inputElement) {
    const searchTerm = inputElement.value;
    if (searchTerm.length < 1) return closeAllLists();

    try {
        const response = await fetch('/search?q=' + encodeURIComponent(searchTerm));
        const suggestions = await response.json();
        showSuggestions(inputElement, suggestions);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function showSuggestions(inputElement, suggestions) {
    closeAllLists();
    if (!suggestions.length) return;

    const list = createList(inputElement);
    suggestions.forEach(suggestion => createListItem(inputElement, list, suggestion));
}

function createList(inputElement) {
    const list = document.createElement("DIV");
    list.setAttribute("id", inputElement.id + "autocomplete-list");
    list.setAttribute("class", "autocomplete-items");
    list.style.position = 'absolute';
    list.style.left = inputElement.getBoundingClientRect().left + 'px';
    list.style.top = (inputElement.getBoundingClientRect().top + inputElement.offsetHeight) + 'px';
    document.body.appendChild(list);
    return list;
}

function createListItem(inputElement, list, suggestion) {
    const item = document.createElement("DIV");
    item.innerHTML = highlightTerm(inputElement.value, suggestion);
    item.addEventListener("click", () => {
        inputElement.value = suggestion;
        performSearchAsync(suggestion);
        closeAllLists();
    });
    list.appendChild(item);
}

function highlightTerm(term, text) {
    return text.replace(new RegExp("(" + term + ")", "gi"), "<strong>$1</strong>");
}

function closeAllLists(elmnt, inputElement) {
    const items = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < items.length; i++) {
        if (elmnt != items[i] && elmnt != inputElement) {
            items[i].parentNode.removeChild(items[i]);
        }
    }
}

async function performSearchAsync(searchTerm) {
    if (searchTerm.length > 0) {
        const minRatingCount = document.getElementById('minRatingCount').value;
        const sortOption = document.getElementById('sortOption').value;

        const searchParams = new URLSearchParams({
            query: searchTerm,
            minRatingCount: minRatingCount,
            sortOption: sortOption
        });

        const gridContainer = document.getElementById('searchResults');
        gridContainer.style.opacity = 0;
        try {
            const response = await fetch('/?' + searchParams.toString());
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newResults = doc.getElementById('searchResults');

            setTimeout(() => {
                gridContainer.innerHTML = newResults.innerHTML;
                gridContainer.style.opacity = 1;
            }, 500);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    }
    closeAllLists();
}

