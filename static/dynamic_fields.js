document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addIngredientBtn').addEventListener('click', addIngredientField);
    document.addEventListener('input', function(event) {
        if (event.target.matches('.ingredientInput')) {
            fetchIngredientSuggestions(event.target);
        }
    });
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
});

function addIngredientField() {
    var newField = document.createElement('div');
    newField.className = 'ingredientField';
    newField.innerHTML = '<label>Ingredient:</label> <input type="text" name="ingredient" class="ingredientInput" autocomplete="off">';
    document.getElementById('ingredientFields').appendChild(newField);
}

function fetchIngredientSuggestions(inputElement) {
    var searchTerm = inputElement.value;
    if (searchTerm.length < 1) {
        closeAllLists();
        return;
    }

    fetch('/ingredient-suggestions?q=' + encodeURIComponent(searchTerm))
        .then(response => response.json())
        .then(suggestions => {
            showSuggestions(inputElement, suggestions);
        })
        .catch(error => console.error('Error fetching ingredient suggestions:', error));
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

    suggestions.forEach(function(suggestion) {
        var item = document.createElement("DIV");
        item.innerHTML = suggestion;
        item.addEventListener("click", function() {
            inputElement.value = suggestion;
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
