// static/js/new_deck.js

const langserveUrl = 'http://localhost:8001';


// fetch data from langserve
function generate_deck(){
    const topic = DOMPurify.sanitize(document.getElementById('title').value);

    // show status
    document.getElementById('status-container').classList.remove('visually-hidden');
    document.getElementById('status-icon').innerHTML = '<div class="spinner-border spinner-border-sm" aria-hidden="true"></div>';
    document.getElementById('status-description').innerHTML = 'Generating...';

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
            // update status
            document.getElementById('status-icon').innerHTML = '<i class="bi bi-exclamation-circle-fill"></i>';
            document.getElementById('status-description').innerHTML = 'Uh oh, something went wrong.';

            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // parse the response
    })
    .then(data => {
        // handle the response
        console.log('API response: ', data);

        // update status
        document.getElementById('status-icon').innerHTML = '<i class="bi bi-check-circle-fill"></i>';
        document.getElementById('status-description').innerHTML = 'Generated Course Outline.';

        // display the response in the DOM
        const dataContainer = document.getElementById('api-data');
        dataContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        // update status
        document.getElementById('status-icon').innerHTML = '<i class="bi bi-exclamation-circle-fill"></i>';
        document.getElementById('status-description').innerHTML = 'Uh oh, something went wrong.';

        console.error('Error fetching data: ', error);
    })
}

document.addEventListener('keydown', function(event) {
   if (event.key === 'Enter') {
       generate_deck();
   }
});