---
title: Text Generation Demo
emoji: ✍️
colorFrom: blue
colorTo: indigo
sdk: gradio
python_version: "3.10"
---

# Text Generation App

## Overview

This beginner-friendly demo shows how to build a real text-generation application with a pretrained Hugging Face causal language model and Gradio. Type an instruction, adjust the generation controls, and click **Generate** to receive a new response from the model.

## Features

- Real local inference with a pretrained instruction-tuned language model.
- Prompt input and generated-text output.
- Temperature, top-p, and maximum-new-token controls.
- Generate and Clear buttons.
- Five example prompts that populate the input box.
- CUDA/CPU auto-detection and inference mode.
- Clear messages for empty prompts, invalid settings, model-loading errors, and generation errors.
- Compatible with local execution and Hugging Face Spaces using the Gradio SDK.

## Tech Stack

- Python 3
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [PyTorch](https://pytorch.org/docs/stable/index.html)
- [Gradio](https://www.gradio.app/docs)
- [Accelerate](https://huggingface.co/docs/accelerate/index)

## Model

The app uses [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), a small instruction-tuned causal language model published under the Apache-2.0 license. Its model card provides the recommended Transformers usage. The model is downloaded from the Hugging Face Hub the first time the app starts and is then kept in memory for later requests.

## How It Works

```text
User Prompt
     ↓
Tokenizer
     ↓
Pretrained Language Model
     ↓
Token Generation
     ↓
Decoded Text
     ↓
Gradio Output
```

1. The user enters a prompt in the Gradio interface.
2. The tokenizer converts the prompt into token IDs, which are numerical inputs for the model.
3. The model predicts likely next tokens and samples a continuation using the selected settings.
4. The app decodes the generated token IDs back into readable text and displays only the new continuation.

The tokenizer is loaded once alongside the model. The model is also loaded once at startup; it is not reloaded for each button click.

## Project Structure

```text
text-generation-app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    └── demo.png
```

## Installation

Create and activate a virtual environment if desired, then install the dependencies:

```bash
pip install -r requirements.txt
```

The dependency ranges target the versions supported by Hugging Face ZeroGPU: Python 3.10 or 3.12, Gradio 4+, and PyTorch 2.8+. They keep Transformers, Gradio, and Accelerate within compatible major versions.

## Usage

Run the application from the project directory:

```bash
python app.py
```

Gradio prints a local URL, usually `http://127.0.0.1:7860`. Open that URL in a browser. The first startup may take longer because the model files must be downloaded and loaded.

## Example Prompts

1. Write a short story about a robot discovering the ocean.
2. Explain machine learning to a beginner in five sentences.
3. Write a professional email asking for a project update.
4. Give me three ideas for a weekend project.
5. Write a short paragraph about the future of artificial intelligence.

## Generation Parameters

- **Temperature** controls how strongly the model favors its most likely next token. Lower values tend to be more predictable; higher values can produce more varied wording. Very high values may reduce coherence.
- **Top-p** limits sampling to the smallest group of likely next tokens whose combined probability reaches the selected value. Lower values restrict the choices more; higher values allow a wider set of choices.
- **Maximum new tokens** caps how many tokens can be generated after the prompt. It is a maximum, not a guarantee that the model will use every token.
- **Do sample** is enabled in the app so temperature and top-p affect the token-selection process. Because sampling is stochastic, repeated runs can differ even when the controls stay the same.

## Sample Output

Sample outputs depend on the model version, runtime, prompt, and sampling settings. For example, the first prompt may produce a short narrative in which a robot observes waves, salt water, and marine life for the first time. Run the app to capture the exact output for your environment.

## Limitations

- The model can produce incorrect, incomplete, repetitive, or biased text.
- CPU generation may be slow, especially with a large maximum-token value.
- The model is small, so output quality may be less consistent than that of larger models.
- The app does not provide fact verification, moderation, conversation history, or persistent storage.
- The first run requires an internet connection to download the model unless the model is already cached.

## Future Improvements

- Add optional conversation history and a chat-style interface.
- Add a deterministic mode using greedy or beam-search decoding.
- Add stop sequences and an output-length estimate.
- Add lightweight input/output moderation and clearer usage guidance.
- Add automated UI tests and a captured screenshot after deployment.

## Deployment

### Option A: Hugging Face ZeroGPU, if available

Your Hugging Face account may show Gradio and Docker as paid while offering only Static Spaces. Do not choose Static or Gradio-Lite for this project: they do not run the Python `app.py` application.

If **ZeroGPU** is available in the hardware choices, use it:

1. Create a new Space at [Hugging Face Spaces](https://huggingface.co/spaces) and select **Gradio** as the SDK.
2. Select **ZeroGPU** hardware.
3. Upload `app.py`, `requirements.txt`, and `README.md` to the root of the Space.
4. Wait for the Space to build and test an example prompt.

The app includes the `@spaces.GPU` decorator required for ZeroGPU. Free personal accounts in good standing can host up to two ZeroGPU Spaces; Hugging Face currently defines this as a verified account that is at least 30 days old. Free accounts have a daily GPU quota, so this is suitable for an internship demo but not unlimited production hosting. See the [ZeroGPU documentation](https://huggingface.co/docs/hub/main/spaces-zerogpu).

### Option B: Render free web service

If ZeroGPU is not available, Render is a practical free hosting alternative for this Python/Gradio app:

1. Create an account at [Render](https://render.com).
2. Choose **New → Web Service**.
3. Connect your GitHub repository.
4. Set the build command to:

   ```text
   pip install -r requirements.txt
   ```

5. Set the start command to:

   ```text
   python app.py
   ```

6. Select the **Free** instance type and deploy.

The app automatically uses Render's `PORT` environment variable and binds to `0.0.0.0`. Render free services sleep after inactivity, so the first request after sleeping may take about a minute while the model loads. Free services are intended for testing, hobby projects, and demos rather than production traffic. See [Render's free service limits](https://render.com/docs/free) and [web-service port requirements](https://render.com/docs/web-services).

### Option C: Temporary Gradio link

For a presentation or internship review, you can share the app temporarily from your own computer:

```powershell
$env:GRADIO_SHARE = "true"
python app.py
```

Gradio prints a public `gradio.live` URL. The link works only while your computer and app are running and normally expires after one week. See the official [Gradio sharing guide](https://gradio.app/guides/sharing-your-app).

The basic app does not require API keys or secrets. Do not claim a deployment is complete until the selected host has actually built and been tested.

See the official [Gradio Spaces guide](https://huggingface.co/docs/hub/en/spaces-sdks-gradio) and [Spaces configuration reference](https://huggingface.co/docs/hub/main/spaces-config-reference) for SDK and runtime configuration details.

## References

- [Transformers documentation](https://huggingface.co/docs/transformers/index)
- [Transformers text-generation documentation](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)
- [Transformers text-generation pipeline documentation](https://huggingface.co/docs/transformers/main/en/main_classes/pipelines#transformers.TextGenerationPipeline)
- [Gradio documentation](https://www.gradio.app/docs)
- [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/en/spaces-overview)
- [Qwen/Qwen2.5-0.5B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
