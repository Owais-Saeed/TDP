# Flashcard App

A web-based application that generates flashcards using an AI language model.

## Technologies used

- Bootstrap (Front-End)
- Flask (Back-End)
- LangChain (AI-integration)

## Installation Overview

1. Clone the repository.

2. Build and run the application using Docker Compose

```sh
docker-compose up --build
```

3. Access the application using the assigned port.

## Installation Step-by-step

1. **Clone the repository**

    1. [Download GitHub Desktop](https://desktop.github.com/download/).
    2. Install and Sign-in to GitHub Desktop
    3. Navigate to Current Repository > Add > Clone Repository.
    4. Clone this repository to a location on your computer. The default path is `~/Documents/GitHub/` .
    5. Click "Fetch origin" to sync your computer with the latest updates from the repository.

2. **Install Docker**

    1. [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
    2. Install Docker Desktop. You can skip the prompts to sign-in or create an account, we don't need to use those features.

3. **Set up the Docker Container** (I'm assuming PowerShell works 1:1 to the Mac/Linux terminal)

    1. Open terminal (or PowerShell on Windows).
    2. Navigate to your local repository. (if you cloned the repository to the default path you will use `cd ~/Documents/GitHub/TDP/`).
    3. Use the command `docker-compose up --build`.
    4. Docker will automatically install all the dependencies and launch the application on your computer.

4. **Launch the application**

    1. Open Docker Desktop.
    2. If the container is not already running, click the play button next to the container.
    3. Click the open port next to "cardapp-web". If you can't see this, you might need to expand the drop-down under "TDP".
    4. The application should open in your default browser!