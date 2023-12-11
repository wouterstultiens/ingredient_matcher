document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('quickSearchInput');
    var searchButton = document.getElementById('searchButton');

    searchInput.addEventListener('input', function(event) {
        fetchSuggestions(event.target);
    });

    searchButton.addEventListener('click', function() {
        performSearch(searchInput.value);
    });

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
});

function fetchSuggestions(inputElement) {
    var searchTerm = inputElement.value;
    if (searchTerm.length < 1) {
        closeAllLists();
        return;
    }

    fetch('/search?q=' + encodeURIComponent(searchTerm))
        .then(response => response.json())
        .then(suggestions => {
            showSuggestions(inputElement, suggestions);
        })
        .catch(error => console.error('Error fetching suggestions:', error));
}

function showSuggestions(inputElement, suggestions) {
    closeAllLists();
    if (!suggestions.length) return;

    var list = document.createElement("DIV");
    list.setAttribute("id", inputElement.id + "autocomplete-list");
    list.setAttribute("class", "autocomplete-items");
    list.style.position = 'absolute';
    list.style.left = inputElement.getBoundingClientRect().left + 'px';
    list.style.top = (inputElement.getBoundingClientRect().top + inputElement.offsetHeight) + 'px';
    document.body.appendChild(list);

    var searchTerm = inputElement.value;
    suggestions.forEach(function(suggestion) {
        var item = document.createElement("DIV");
        var regex = new RegExp("(" + searchTerm + ")", "gi");
        item.innerHTML = suggestion.replace(regex, "<strong>$1</strong>");
        item.addEventListener("click", function() {
            window.location.href = '/search-results?q=' + encodeURIComponent(suggestion);
            closeAllLists();
        });
        list.appendChild(item);
    });
}

function closeAllLists(elmnt) {
    var items = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < items.length; i++) {
        if (elmnt != items[i]) {
            items[i].parentNode.removeChild(items[i]);
        }
    }
}

function performSearch(searchTerm) {
    if (searchTerm.length > 0) {
        window.location.href = '/search-results?q=' + encodeURIComponent(searchTerm);
    }
}