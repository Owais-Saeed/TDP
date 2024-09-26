let deck;
let currentCardIndex = 0;
let cardAnswers = [];

function loadDeck() {
    fetch('/api/deck/' + deckTopic)
        .then(response => response.json())
        .then(data => {
            deck = data;
            showCard();
            populateMenu();
        });
}

function showCard() {
    const card = deck.cards[currentCardIndex];
    document.getElementById('question').textContent = card.question;
    document.getElementById('answer').textContent = card.answer;
    document.getElementById('feedback').style.display = 'none';
    document.getElementById('flashcard').classList.remove('flipped');
    updateMenuActiveState();
}

function flipCard() {
    document.getElementById('flashcard').classList.toggle('flipped');
    if (document.getElementById('flashcard').classList.contains('flipped')) {
        document.getElementById('feedback').style.display = 'block';
    }
}

function nextCard(correct) {
    cardAnswers[currentCardIndex] = correct;
    updateMenuIcon(currentCardIndex, correct);
    currentCardIndex++;
    if (currentCardIndex >= deck.cards.length) {
        showSummary();
    } else {
        showCard();
    }
}

function populateMenu() {
    const menu = document.getElementById('cardMenu');
    menu.innerHTML = '';
    deck.cards.forEach((card, index) => {
        const li = document.createElement('li');
        li.className = 'list-group-item menu-item';
        li.innerHTML = `
            <span>Card ${index + 1}</span>
            <span class="icon"></span>
        `;
        li.onclick = () => {
            currentCardIndex = index;
            showCard();
        };
        menu.appendChild(li);
    });
    cardAnswers = new Array(deck.cards.length).fill(null);
}

function updateMenuActiveState() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach((item, index) => {
        if (index === currentCardIndex) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

function updateMenuIcon(index, correct) {
    const menuItems = document.querySelectorAll('.menu-item');
    const icon = menuItems[index].querySelector('.icon');
    if (correct) {
        icon.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
    } else {
        icon.innerHTML = '<i class="bi bi-x-circle-fill text-danger"></i>';
    }
}

function showSummary() {
    const correctAnswers = cardAnswers.filter(answer => answer === true).length;
    const totalCards = deck.cards.length;
    document.getElementById('summaryText').textContent = `Correct answers: ${correctAnswers}/${totalCards}. Do you wish to try again?`;
    document.getElementById('flashcard').style.display = 'none';
    document.getElementById('feedback').style.display = 'none';
    document.getElementById('summary').style.display = 'block';
}

function retryDeck() {
    currentCardIndex = 0;
    cardAnswers = new Array(deck.cards.length).fill(null);
    document.getElementById('summary').style.display = 'none';
    document.getElementById('flashcard').style.display = 'block';
    populateMenu();
    showCard();
}

document.getElementById('flashcard').addEventListener('click', flipCard);
loadDeck();