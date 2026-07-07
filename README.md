# GuruvAI

GuruvAI is an AI-powered teaching assistant designed to deliver methodology-driven learning support through natural language, handwriting recognition, and spoken output.

Built with FastAPI, Python, HTML, CSS, and browser-based handwriting tooling, the project demonstrates how an educational assistant can combine conversational AI, math input, and accessibility features into one interactive experience.

## Why This Project Stands Out

- Focused on the learning experience, not just chat automation.
- Supports handwritten math input and LaTeX-style conversion.
- Generates speech output with Amazon Polly for accessibility and engagement.
- Uses a clean separation between backend AI orchestration and front-end interaction.
- Demonstrates a practical full-stack workflow suitable for product or internship review.

## Core Features

- AI teaching assistant for tutoring-style, methodology-driven responses.
- FastAPI backend that routes prompts to Conva AI.
- Handwriting-enabled math canvas powered by iink.js assets.
- Speech synthesis support through Amazon Polly.
- Lightweight browser demos for testing input, conversion, and interaction.

## Tech Stack

- Python 3.12+
- FastAPI
- boto3 / Amazon Polly
- Conva AI
- HTML, CSS, JavaScript
- iink.js / iink-ts

## Architecture Overview

- `server.py` handles API requests, assistant orchestration, and speech generation.
- `index.html` provides a handwriting math demo with conversion controls.
- `test.html` contains an alternate interactive UI prototype.
- `iinkTS/` stores the handwriting and math recognition assets used by the demos.
- Environment variables keep credentials and assistant configuration out of source control.

## Environment Variables

Create a local `.env` file in the project root:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
CONVA_ASSISTANT_ID=your_conva_assistant_id
CONVA_API_KEY=your_conva_api_key
CONVA_ASSISTANT_VERSION=46.0.0
```

The repository ignores `.env`, so secrets remain local to your machine.

## Setup

1. Install Python dependencies.

```bash
pip install -e . uvicorn
```

2. Install front-end dependencies.

```bash
npm install
```

3. Add your `.env` file to the project root.

## Run Locally

Start the FastAPI backend:

```bash
uvicorn server:app --reload
```

Serve the HTML demos in a browser:

```bash
python -m http.server 8000
```

Then open:

- `http://localhost:8000/index.html`
- `http://localhost:8000/test.html`

## API Endpoints

- `POST /invoke_capability/`
- `POST /invoke_capability_name/{capability_name}`

Both endpoints accept JSON input with a `text` field and return the assistant response, parameters, and optional voice output.

## Resume-Ready Summary

GuruvAI is an AI-powered teaching assistant that combines FastAPI, Conva AI, handwriting-to-LaTeX style input, and Amazon Polly speech synthesis to create a more accessible and interactive learning experience.

It showcases full-stack development, AI integration, and thoughtful UX for education-focused applications.

