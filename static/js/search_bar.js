const input = document.querySelector('#search-bar');
const suggestions = document.querySelector('.suggestions');
const newUl = document.createElement("ul");
const searchAll = [];

async function fetchUsers() {
    const response = await fetch('/get_all_users');
    const data = await response.json();

    const incoming = data.incoming_names;
    const gainers = data.gainer_names;
    const cadre = data.cadre_names;

    searchAll.push(...incoming, ...gainers, ...cadre);

    function search(str) {
        let results = [];
        if (str.length) {
            results = str.map(user => {
                return `<li><a href="/users/show/${user.id}">${user.name}</a></li>`
            });
        }

        return results;
    }

    function searchHandler(e) {
        let chars = input.value;
        let dropResults = [];

        if (chars.length) {
            dropResults = searchAll.filter(searchItem => {
                return searchItem.name.toLowerCase()
                .includes(chars.toLowerCase())
            });
        }

        return showSuggestions(dropResults);
    }

    function showSuggestions(inputVal) {
        let drops = search(inputVal);

        if (drops !== []) {
            suggestions.appendChild(newUl).innerHTML = drops.join('');
        }
    }

    function useSuggestion(e) {
        let pick = newUl.childNodes;
        let pickArr = Array.from(pick);

        for (let i=0; i<pickArr.length; i++) {
            if (pickArr[1] === e.target) {
                input.value = pickArr[i].innerText;
                newUl.remove();
            }
        }
    }

    input.addEventListener('keyup', searchHandler);
    newUl.addEventListener('click', useSuggestion);

}

fetchUsers();