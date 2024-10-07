// static/js/scripts.js

let keys = [];
document.addEventListener('keydown', function(event) {
    keys.push(event.key);
    if (keys.slice(-9).join('') === 'powpowpow') { document.body.classList.toggle('loading-indicator'); keys = []; }
    if (keys.length > 9) { keys.shift(); }
});