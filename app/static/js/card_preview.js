// static/js/card_preview.js

// logic to open card previews
document.addEventListener('DOMContentLoaded', function() {
    // get the page elements
    const modalElement = new bootstrap.Modal(document.getElementById('card-preview'));
    const frontElement = document.getElementById('preview-front');
    const backElement = document.getElementById('preview-back');

    const thumbnailLinks = document.querySelectorAll('.thumbnail-link');

    // variables for interactivity
    const card = document.querySelector('.flashcard');
    const container = document.querySelector('.flashcard-container');

    // transition durations
    const TRANSITION_ENTER_DURATION = 200;
    const TRANSITION_RESET_DURATION = 400;
    const TRANSITION_FLIP_DURATION = 500;
    const TRANSITION_POST_FLIP_DURATION = 400;

    // tilt sensitivity
    const TILT_SENSITIVITY = 20;

    let isFlipped = false;
    let isAnimating = false;
    let tilt = { x: 0, y: 0 };

    // don't do anything if there are no cards on the page
    if (thumbnailLinks.length === 0) {
        return;
    }

    // open the card preview
    thumbnailLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // make sure the card shows the front
            if (isFlipped === true) {
                isFlipped = false;
                updateTransform();
            }

            // fetch data
            const frontData = link.getAttribute('data-front');
            const backData = link.getAttribute('data-back');

            // parse to markdown
            const frontDataMd = marked.parse(frontData);
            const backDataMd = marked.parse(backData);

            // change the data in the preview
            frontElement.innerHTML = frontDataMd;
            backElement.innerHTML = backDataMd;

            // open the preview
            modalElement.show();
        });
    });

    // add interactivity to card preview

    // update the card's transformation based on flip state and tilt
    const updateTransform = () => {
        const flipY = isFlipped ? 180 : 0;
        card.style.transform = `rotateY(${flipY + tilt.y}deg) rotateX(${tilt.x}deg)`;
    };

    // calculate tilt based on mouse position
    const calculateTilt = (event) => {
        const rect = container.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        tilt.x = -(mouseY - centerY) / TILT_SENSITIVITY;
        tilt.y = (mouseX - centerX) / TILT_SENSITIVITY;

        if (isFlipped) {
            tilt.x = -tilt.x;
        }

        updateTransform();
    };

    // handle smooth transition when mouse enters the container
    const handleMouseEnter = () => {
        if (isAnimating) return;

        card.style.transition = `transform ${TRANSITION_ENTER_DURATION}ms ease-out`;

        // remove the transition after it's completed
        setTimeout(() => {
            if (isAnimating) return;
            card.style.transition = 'none';
        }, TRANSITION_ENTER_DURATION);
    };

    // handle tilt effect on mouse move
    const handleMouseMove = (event) => {
        if (isAnimating) return;
        calculateTilt(event);
    };

    // reset tilt smoothly when mouse leaves the container
    const resetTilt = () => {
        if (isAnimating) return;

        card.style.transition = `transform ${TRANSITION_RESET_DURATION}ms ease-in-out`;
        tilt = { x: 0, y: 0 };
        updateTransform();

        setTimeout(() => {
            if (isAnimating) return;
            card.style.transition = 'none';
        }, TRANSITION_RESET_DURATION);
    };

    // handle card flip on click
    const handleFlip = () => {
        if (isAnimating) return;
        isAnimating = true;

        card.style.transition = `transform ${TRANSITION_FLIP_DURATION}ms ease-out`;
        isFlipped = !isFlipped;
        updateTransform();

        setTimeout(() => {
            isAnimating = false;
            if (container.matches(':hover')) {
                card.style.transition = `transform ${TRANSITION_POST_FLIP_DURATION}ms ease-out`;

                setTimeout(() => {
                    if (isAnimating) return;
                    card.style.transition = 'none';
                }, TRANSITION_POST_FLIP_DURATION);
            } else {
                resetTilt();
            }
        }, TRANSITION_FLIP_DURATION);

    };

    // attach event listeners
    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', resetTilt);
    container.addEventListener('click', handleFlip);
});