# AI Text Generation App

## Overview

This beginner-friendly Gradio application demonstrates real text generation through the Groq API. Users can choose a task, enter a prompt or source text, adjust generation settings, and receive a response from a Groq-hosted language model.

The app does not download or run a local model. Groq provides the hosted inference service, which keeps this Python application lightweight for Render.

## Features

- Creative writing, question answering, and summarization modes
- Task-specific system instructions
- Temperature control from 0.0 to 1.5
- Maximum output token control from 50 to 500
- Generate and Clear buttons
- Example prompts for every task
- Server-side API key handling
- Friendly error messages
- Render-compatible host and port configuration

## Tech Stack

- Python 3
- Gradio
- Groq Python SDK
- Groq Chat Completions API
- Render

No Transformers, PyTorch, TensorFlow, or downloaded model weights are used.

## Architecture

```text
User
  ↓
Gradio UI
  ↓
Python Application
  ↓
Groq Chat Completions API
  ↓
Groq-hosted Language Model
  ↓
Generated Response
  ↓
Gradio UI
```

## Supported Tasks

### Creative Writing

Generates coherent creative content based on the user's request.

### Question Answering

Answers questions clearly and uses simple explanations when appropriate.

### Summarization

Condenses supplied text while preserving its main ideas and important details.

## How It Works

1. The user selects a task and enters a prompt.
2. Gradio sends the values to the Python callback.
3. The callback validates the input and selects task-specific instructions.
4. The Groq API receives system and user messages plus temperature and maximum-token settings.
5. The generated response is displayed in Gradio.

## Project Structure

```text
text-generation-app/
├── app.py
├── llm.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── screenshots/
    └── demo.png
```

## Local Setup

```bash
git clone <repository-url>
cd text-generation-app
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create `.env` from `.env.example`:

```text
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Required variables:

- `GROQ_API_KEY` — private Groq API key
- `GROQ_MODEL` — Groq model ID; the default is `openai/gpt-oss-20b`

Never commit `.env` or place the API key in source code or frontend JavaScript.

## Running the App

```bash
python app.py
```

Open the local Gradio URL shown in the terminal, normally `http://127.0.0.1:7860`.

## Example Prompts

### Creative Writing

- Write a short story about a student who discovers an AI assistant that can predict the future.
- Write a creative paragraph describing a city on Mars.

### Question Answering

- What is the difference between supervised and unsupervised learning?
- Explain transformers in simple terms.

### Summarization

- Paste a paragraph about artificial intelligence and summarize it.
- Paste a project description and extract its key points.

## Generation Parameters

### Temperature

Temperature controls randomness. Lower values generally produce more predictable responses, while higher values generally produce more variation.

### Maximum Output Tokens

This limits the maximum length of the generated response. The demo allows values from 50 to 500.

Different settings can produce different outputs because they change how the model selects possible next tokens. The prompt and selected model also affect the result.

## Deployment

### GitHub

From the project folder:

```bash
git add .
git status
git commit -m "Switch text generation demo to Groq API"
git push origin main
```

Confirm that `.env` is not tracked before pushing.

### Render Web Service

1. Open your Render service connected to this GitHub repository.
2. Trigger a new deployment after pushing these changes.
3. Use this Build Command:

   ```bash
   pip install -r requirements.txt
   ```

4. Use this Start Command:

   ```bash
   python app.py
   ```

5. In Render **Environment Variables**, remove the old `OPENAI_API_KEY` and `OPENAI_MODEL` variables if present.
6. Add:

   ```text
   GROQ_API_KEY=your_private_groq_key
   GROQ_MODEL=openai/gpt-oss-20b
   ```

7. Save the variables and redeploy.
8. Open the Render URL and test all three modes.

The application listens on `0.0.0.0` and reads Render's `PORT` automatically. No local model is downloaded during deployment.

## Limitations

- A valid Groq API key is required for real generation.
- Groq rate limits and model availability depend on the account and selected model.
- A public app can consume API quota if shared widely.
- Render free services may sleep when idle.
- API usage policies and free-tier limits can change.

## Future Improvements

- Add conversation history
- Add streaming output
- Add usage monitoring
- Add authentication before public sharing
- Add automated API-error tests

## References

- [Groq Quickstart](https://console.groq.com/docs/quickstart)
- [Groq Python SDK](https://github.com/groq/groq-python)
- [Groq API Reference](https://console.groq.com/docs/api-reference)
- [Groq Supported Models](https://console.groq.com/docs/models)
- [Gradio documentation](https://www.gradio.app/docs)
- [Render web services documentation](https://render.com/docs/web-services)
