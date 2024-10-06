# Flashcard App

Our application is designed to generate educational STEM flashcards for high-school students. The application utilises proven study techniques including retrieval practice, and incremental rehearsal.

![Application screenshot](./app/static/images/screenshot.png)

## Technologies used

- **Flask**: Back-end web framework.
- **MongoDB**: NoSQL database.
- **Bootstrap**: Front-end framework.
- **LangChain**: LLM integration framework.
- **Gemini**: The model used to generate content.
- **Docker**: For containerisation.

## Getting Started

### Prerequisites

- Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop/) is recommended)
- Git ([GitHub Desktop](https://desktop.github.com/download/) is recommended)

### Installation

1. Clone the repository.

2. Set up the Environment Variables.

3. Build and run the application using Docker Compose.

```sh
docker-compose up --build
```

### Environment Variables

To use the application's AI features, a Gemini API key is _required_. Place your API keys in a `.env` file in the root directory (`/.env`).

#### Google Gemini API (required)

1. Create a [Google AI Studio](https://aistudio.google.com) API key.

2. Add your Gemini API key to the `.env` file:

```
export GOOGLE_API_KEY="your_api_key_here"
```

#### LangSmith (optional)

Use LangSmith to see a detailed breakdown of the LLM's generation process.

1. Create a [LangSmith](https://www.langchain.com/langsmith) API key.

2. Add your LangSmith API key to the `.env` file:

```
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your_api_key_here"
```
