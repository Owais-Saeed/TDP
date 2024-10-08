// static/js/new_deck.js

const langserveUrl = 'http://localhost:8001';

// page elements
const inputField = document.getElementById('title');
const inputFeedback = document.getElementById('input-lg-feedback');
const statusContainer = document.getElementById('status-container');
const statusIcon = document.getElementById('status-icon');
const statusText = document.getElementById('status-description');

// for pressing enter to submit
let inputFieldFocus = false;

// fetch data from langserve
function generate_deck(){
    const topic = DOMPurify.sanitize(inputField.value).trim();

    // refuse if field is empty
    if (topic.length <= 4){
        inputFeedback.innerHTML = '<i class="bi bi-exclamation-circle-fill me-1"></i>Topic must be at least 4 characters long';
        return;
    }
    // make sure input feedback is empty if valid
    inputFeedback.innerHTML = '';

    // show status
    statusContainer.classList.remove('visually-hidden');
    statusIcon.innerHTML = '<div class="spinner-border spinner-border-sm" aria-hidden="true"></div>';
    statusText.innerHTML = 'Generating...';

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
            statusIcon.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i>';
            statusText.innerHTML = 'Uh oh, something went wrong.';

            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // parse the response
    })
    .then(data => {
        // handle the response
        console.log('API response: ', data);

        // update status
        statusIcon.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
        statusText.innerHTML = 'Generated outline about \'' + topic + '\'';

        // display the response in the DOM
        const dataContainer = document.getElementById('api-data');
        dataContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        // update status
        statusIcon.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i>';
        statusText.innerHTML = 'Uh oh, something went wrong.';

        console.error('Error fetching data: ', error);
    })
}

// when the field is in focus, take enter input to start generation
document.addEventListener('keydown', function(event) {
   if (event.key === 'Enter' && inputFieldFocus === true) {
       generate_deck();
   }
});
inputField.addEventListener('focusin', function(event) {
    inputFieldFocus = true;
});
inputField.addEventListener('focusout', function(event) {
    inputFieldFocus = false;
});