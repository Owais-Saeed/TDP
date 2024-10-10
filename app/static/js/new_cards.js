// static/js/new_deck.js

let deckId = null;

const langserveUrl = 'http://localhost:8001';

// store all the generate links on the page
let generating = false;
let generateLinks = null;

// store the generated json data
let generatedData = null;

// fetch data from langserve
function generate_cards(linkElement, level, topic, unit, concept, concepts_to_avoid = ["none"]){
    if (deckId === null) {
        console.error('No deck id.');
        return;
    }

    // only generate once
    if (generating === true) {
        console.error('There is already a generation process occurring.');
        return;
    }
    generating = true;

    // disable all the links
    generateLinks.forEach(link => {
        link.disabled = true;
        if (link !== linkElement) {
            link.classList.add('btn-outline-secondary');
        }
    });

    linkElement.innerHTML = '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span><span>Generating...</span>';
    console.log([linkElement, level, topic, unit, concept, concepts_to_avoid]);

    fetch(langserveUrl + '/cards/generator/invoke', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "input": {
                "level": "high-school",
                "topic": topic,
                "unit": unit,
                "concept": concept,
                "concepts_to_avoid": concepts_to_avoid
            },
            "config": {},
            "kwargs": {}
        })
    })
    .then (response => {
        if (!response.ok) {
            // update status
            linkElement.innerHTML = '<i class="bi bi-exclamation-circle-fill me-2"></i><span>An error occurred</span>';

            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // parse the response
    })
    .then(data => {
        // send the data to the server
        saveData(linkElement, unit, concept, data);
    })
    .catch(error => {
        // update status
        linkElement.innerHTML = '<i class="bi bi-exclamation-circle-fill me-2"></i><span>An error occurred</span>';

        console.error('Error fetching data: ', error);
    })
}

function saveData(linkElement, unitTitle, conceptTitle, cardData) {
    console.log("Saving...");
    linkElement.innerHTML = '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span><span>Saving...</span>';
    console.log(cardData);
    console.log(cardData['output']['cards']);

    const send = {
        'id': deckId,
        'unit': unitTitle,
        'concept': conceptTitle,
        'cards': cardData['output']['cards']
    }
    console.log(send);

    // send the data to flask
    fetch('/dashboard/deck/save_cards', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(send),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // redirect
        if (data.status === 'success') {
            window.location.href = data.redirect_url;
        } else {
            console.log('Did not receive response.');
        }
    })
    .catch((error) => {
        linkElement.innerHTML = '<i class="bi bi-exclamation-circle-fill me-2"></i><span>Could not save</span>';
        console.error('Error: ', error);
    });
}

// add data to generate buttons on page load
document.addEventListener('DOMContentLoaded', function() {
    // get the deck id
    deckId = document.getElementById('deck-id').innerHTML;

    generateLinks = document.querySelectorAll('.cards-generate-button');

    // don't do anything if there are no generate links
    if (generateLinks.length === 0) {
        return;
    }

    generateLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // get the elements containing data for generation
            const conceptElement = link.closest('.deck-concept');
            const unitElement = conceptElement.closest('.deck-unit');
            const courseElement = unitElement.closest('.deck-course');

            // fetch data
            const level = courseElement.getAttribute('data-cards-level');
            const topic = courseElement.getAttribute('data-cards-topic');
            const unit = unitElement.getAttribute('data-cards-unit');
            const concept = conceptElement.getAttribute('data-cards-concept');

            // fetch the other concepts
            const otherConcepts = Array.from(unitElement.querySelectorAll('.deck-concept')).filter(concept => concept !== conceptElement);
            let otherConceptsData = [];
            otherConcepts.forEach(concept => {
                otherConceptsData.push(concept.getAttribute('data-cards-concept'));
            });

            generate_cards(link, level, topic, unit, concept, otherConceptsData);
        });
    });
});