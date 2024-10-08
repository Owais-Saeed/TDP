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

// store the generated json data
let generatedData = null;

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

        // update status
        statusIcon.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
        statusText.innerHTML = 'Generated outline about \'' + topic + '\'';

        // store the data
        generatedData = data;

        // display the response in the DOM
        displayOutline(data);
    })
    .catch(error => {
        // update status
        statusIcon.innerHTML = '<i class="bi bi-exclamation-circle-fill"></i>';
        statusText.innerHTML = 'Uh oh, something went wrong.';

        console.error('Error fetching data: ', error);
    })
}

function displayOutline(data) {
    const dataContainer = document.getElementById('outline');

    dataContainer.innerHTML = '';

    // create the heading
    let outlineTitle = document.createElement('h2');
    outlineTitle.classList.add('m-0');
    outlineTitle.textContent = data.output.topic;
    dataContainer.appendChild(outlineTitle);

    // loop through units and create the cards
    data.output.units.forEach((unit) => {
        // create card div
        let cardDiv = document.createElement('div');
        cardDiv.classList.add('card');

        // create card header
        let cardHeader = document.createElement('div');
        cardHeader.classList.add('card-header');
        cardHeader.textContent = `Unit ${unit.id}`;

        // create card body
        let cardBody = document.createElement('div');
        cardBody.classList.add('card-body');
        let cardTitle = document.createElement('h3');
        cardTitle.classList.add('card-title', 'm-0');
        cardTitle.textContent = unit.title;
        cardBody.appendChild(cardTitle);

        // create list for outline concepts
        let listGroup = document.createElement('ul');
        listGroup.classList.add('list-group', 'list-group-flush');

        unit.outline.forEach((item) => {
            let listItem = document.createElement('li');
            listItem.classList.add('list-group-item');
            listItem.textContent = item.concept;
            listGroup.appendChild(listItem);
        });

        // append everything together
        cardDiv.appendChild(cardHeader);
        cardDiv.appendChild(cardBody);
        cardDiv.appendChild(listGroup);

        // add card to outline
        dataContainer.appendChild(cardDiv);
    });

    // show the save button
    document.getElementById('confirm').classList.remove('visually-hidden');
}

function save_deck() {
    if (generatedData !== null) {
        // save the data
        console.log("Saving...");
        // disable the save button
        document.getElementById('save-button').disabled = true;
        document.getElementById('save-button').innerHTML = 'Saving...';
        // send the data to flask
        fetch('./save_deck', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(generatedData),
        })
        .then(response => response.json())
        .then(data => {
            // redirect
            if (data.status === 'success') {
                window.location.href = data.redirect_url;
            } else {
                console.log('Did not receive response.');
            }
        })
        .catch((error) => {
            console.error('Error: ', error);
        });
    } else {
        console.log("No data to save.");
    }
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