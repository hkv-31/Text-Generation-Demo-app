# AI Text Generation App

## Overview

This beginner-friendly application demonstrates real text generation through an OpenAI language model. It uses Gradio so a user can select a task, enter a prompt or source text, adjust generation controls, and receive a response.

The application uses the OpenAI API instead of downloading or running a local model. This keeps the deployed Python service lightweight and suitable for a small Render instance. Render hosting and OpenAI API usage are separate: free hosting does not necessarily make API usage free, so review your OpenAI account limits and billing before sharing the app publicly.

## Features

- Creative writing, question answering, and summarization modes
- Task-specific model instructions
- Temperature control from 0.0 to 1.5
- Maximum output token control from 50 to 500
- Generate and Clear buttons
- Example prompts for every task
- Server-side API key handling
- Friendly messages for missing keys, rate limits, connection failures, and invalid inputs
- Render-compatible host and port configuration

## Tech Stack

- Python 3
- Gradio
- OpenAI Python SDK
- OpenAI Responses API
- Render for lightweight web hosting

The project intentionally does not use Transformers, PyTorch, TensorFlow, or downloaded model weights.

## Architecture

```text
User
  ↓
Gradio UI
  ↓
Python Application
  ↓
OpenAI Responses API
  ↓
OpenAI Language Model
  ↓
Generated Response
  ↓
Gradio UI
```

## Supported Tasks

### Creative Writing

The model creates coherent content based on the requested topic, tone, format, and length.

### Question Answering

The model answers a question clearly and uses simple explanations when appropriate.

### Summarization

The model condenses supplied text while preserving the main ideas and important details.

## How It Works

1. The user selects a task and enters a prompt or source text.
2. Gradio sends the values to the Python callback.
3. The callback validates the input and selects task-specific instructions.
4. The OpenAI Responses API receives the instructions, input, temperature, and output-token limit.
5. The returned text is displayed in the Gradio output box.

The tokenizer and model inference are handled by OpenAI's hosted model service. This application has no local model-loading step and does not download model weights during deployment.

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

Clone the repository and create a virtual environment:

```bash
git clone <repository-url>
cd text-generation-app
python -m venv venv
```

On Windows PowerShell, activate it with:

```powershell
venv\Scripts\activate
```

On macOS/Linux, activate it with:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a local `.env` file from `.env.example` and add your own values:

```text
OPENAI_API_KEY=your_actual_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Required variables:

- `OPENAI_API_KEY`: your private OpenAI API key
- `OPENAI_MODEL`: the OpenAI text model to call; the default is `gpt-4.1-mini`

Never commit `.env`, paste a key into source code, or expose a key in frontend JavaScript. The `.env` file is ignored by Git.

## Running the App

After creating `.env`, run:

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

- Paste a paragraph about artificial intelligence and ask the app to summarize it.
- Paste a project description and use the Summarization mode to extract its key points.

## Generation Parameters

### Temperature

Temperature ranges from 0.0 to 1.5. Lower values generally make responses more predictable, while higher values generally allow more variation. It does not guarantee a particular answer.

### Maximum Output Tokens

This limits the maximum amount of generated text. A larger value allows longer responses and may use more API capacity. The demo limits the control to 50–500 tokens.

Different settings can produce different outputs because they change how the model selects likely next tokens. The exact result also depends on the prompt and model.

## Deployment

### GitHub

Create an empty GitHub repository, then run these commands from the project folder. Replace the placeholder with your own repository URL:

```bash
git init
git add .
git status
git commit -m "Build OpenAI text generation demo app"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

Before committing, confirm that `.env` is not listed as a tracked file. Do not commit an API key.

### Render Web Service

1. Push the project to GitHub.
2. In Render, choose **New → Web Service** and connect the repository.
3. Use a Python runtime.
4. Set the Build Command to `pip install -r requirements.txt`.
5. Set the Start Command to `python app.py`.
6. In Render **Environment Variables**, add `OPENAI_API_KEY` and `OPENAI_MODEL`.
7. Deploy and open the generated Render URL.

The app listens on `0.0.0.0` and reads Render's `PORT` variable automatically. Render does not need to download an LLM because inference happens through the OpenAI API. Free Render services can sleep or have resource limits, and OpenAI API charges or account limits are separate from Render hosting.

## Limitations

- The app needs a valid OpenAI API key to generate a real response.
- Output quality and response time depend on the selected model and service availability.
- Public deployments can consume API quota if the URL is shared.
- A free hosting service may sleep when idle.
- The application is a learning demonstration, not a production safety or fact-checking system.

## Future Improvements

- Add conversation history
- Add streaming output
- Add an optional system-prompt editor for advanced users
- Add usage monitoring and authentication before public sharing
- Add automated tests around API error responses

## References

- [OpenAI Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI GPT-4.1 mini model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini)
- [OpenAI API pricing](https://openai.com/api/pricing/)
- [Gradio documentation](https://www.gradio.app/docs)
- [Render web services documentation](https://render.com/docs/web-services)
