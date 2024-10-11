// static/js/scripts.js

// convert to markdown
document.addEventListener('DOMContentLoaded', function() {
    const markdownElements = document.querySelectorAll('.md');
    if (markdownElements.length === 0) {
        return;
    }
    markdownElements.forEach(markdownElement => {
        originalData = markdownElement.innerHTML.trim();
        console.log(originalData);
        markdownElement.innerHTML = marked.parse(originalData);
    })
});

let keys = [];
document.addEventListener('keydown', function(event) {
    keys.push(event.key);
    if (keys.slice(-9).join('') === 'powpowpow') { document.body.classList.toggle('loading-indicator'); keys = []; }
    if (keys.length > 9) { keys.shift(); }
});