// static/js/new_deck.js

const langserveUrl = 'http://localhost:8001';


// fetch data from langserve
function generate_deck(){
    const topic = DOMPurify.sanitize(document.getElementById('title').value);

    fetch(langserveUrl + '/outline/generator/invoke', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "input": {
                "topic": topic
            },
            "config": {},
            "kwargs": {}
        })
    })
    .then (response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // parse the response
    })
    .then(data => {
        // handle the response
        console.log('API response: ', data);

        // display the response in the DOM
        const dataContainer = document.getElementById('api-data');
        dataContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        console.error('Error fetching data: ', error);
    })
}