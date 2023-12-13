document.addEventListener('DOMContentLoaded', function() {
    let searchInput = document.getElementById('quickSearchInput');
    let searchButton = document.getElementById('searchButton');
    let minRatingCountInput = document.getElementById('minRatingCount');
    let sortOptionSelect = document.getElementById('sortOption');

    searchInput.addEventListener('input', event => fetchSuggestions(event.target));
    searchButton.addEventListener('click', () => performSearch(searchInput.value));
    minRatingCountInput.addEventListener('change', () => updateSearchResults());
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
    let minRatingCount = document.getElementById('minRatingCount').value;
    let sortOption = document.getElementById('sortOption').value;

    let searchParams = new URLSearchParams({
        q: searchTerm,
        minRatingCount: minRatingCount,
        sortOption: sortOption
    });

    let gridContainer = document.getElementById('searchResults');
    // Set grid container to loading animation
    gridContainer.innerHTML = '<div class="loader-container"><div class="loader"></div></div>';
    gridContainer.style.height = '100vh'; // Adjust height to cover the grid

    fetch('/?' + searchParams.toString())
        .then(response => response.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            let newResults = doc.getElementById('searchResults');
            let currentResults = document.getElementById('searchResults');
            currentResults.innerHTML = newResults.innerHTML;
            currentResults.style.height = 'auto'; // Reset height after loading
        })
        .catch(error => {
            console.error('Error updating search results:', error);
            gridContainer.innerHTML = '<p>Error loading recipes. Please try again.</p>';
            gridContainer.style.height = 'auto'; // Reset height on error
        });
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
        inputElement.value = suggestion; // Set input value to the clicked suggestion
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

// Add the updated performSearch function
function performSearch(searchTerm) {
    if (searchTerm.length > 0) {
        let searchParams = new URLSearchParams({
            query: searchTerm,
            sortOption: 'name' // Default sort by name
        });
        fetch('/?' + searchParams.toString())
            .then(response => response.text())
            .then(html => {
                let parser = new DOMParser();
                let doc = parser.parseFromString(html, 'text/html');
                let newResults = doc.getElementById('searchResults');
                let currentResults = document.getElementById('searchResults');

                // Add animation here
                currentResults.style.opacity = 0;
                setTimeout(() => {
                    currentResults.innerHTML = newResults.innerHTML;
                    currentResults.style.opacity = 1;
                }, 500); // Adjust time for desired animation effect
            })
            .catch(error => console.error('Error fetching search results:', error));
    }
    closeAllLists();
}

