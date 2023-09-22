const input = document.querySelector('#search-bar');
const suggestions = document.querySelector('.suggestions');
const newUl = document.createElement("ul");
const searchAll = [];

async function fetchUsers() {
    const response = await fetch('/get_all_users');
    const data = await response.json();
    console.log(data);
    const incoming = data.incoming_names;
    const ids = data.DODIDs;
    const unit_ids = data.UICs;
    const gainers = data.gainer_names;
    const cadre = data.cadre_names;

    searchAll.push(...incoming, ...ids, ...unit_ids, ...gainers, ...cadre);

    function search(str) {
        console.log(str)
        let results = [];
        if (str.length) {
            results = str.map(item => {
                console.log(item);
                if (item.hasOwnProperty('name')) {
                    return `<li><a href="/users/show/${item.id}">${item.name}</a></li>`
                } else if (item.hasOwnProperty('DODID')) {
                    return `<li><a href="/users/show/${item.id}">${item.name}</a></li>`
                } else if (item.hasOwnProperty('UIC')) {
                    return `<li><a href="/users/show/${item.id}">${item.name}</a></li>`
                }
            });
        }
        console.log(results[0])
        return results;
    }

    function searchHandler(e) {
        console.log("Function searchHandler is being executed.")
        console.log("All searchable items:", searchAll);
        let chars = input.value;
        console.log("Input value:", chars, " ", "chars.length:", chars.length > 0);
        let dropResults = [];
       
        if (chars.length) {
            dropResults = searchAll.filter(searchItem => {
                console.log('Checking:', searchItem);
                if (searchItem.hasOwnProperty('name') && searchItem.name.toLowerCase().includes(chars.toLowerCase())) {
                    return true;
                }
                if (searchItem.hasOwnProperty('DODID') && searchItem.DODID.toString().includes(chars)) {
                    return true;
                }
                if (searchItem.hasOwnProperty('UIC') && searchItem.UIC.toString().toLowerCase().includes(chars.toLowerCase())) {
                    return true;
                }
                return false;                
            });
            console.log("Filtered items:", dropResults);
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
