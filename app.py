"""Small Gradio demo for local text generation with a Hugging Face model."""

from __future__ import annotations

import os
from typing import Any

import gradio as gr

# Hugging Face Spaces provides this module for ZeroGPU. The fallback keeps the
# same file runnable locally without installing the Spaces-only helper.
try:
    import spaces
except ImportError:
    class _LocalSpaces:
        @staticmethod
        def GPU(function=None, **_kwargs):
            if function is not None:
                return function
            return lambda wrapped_function: wrapped_function

    spaces = _LocalSpaces()

import torch

# This app uses the PyTorch backend. Disabling optional TensorFlow discovery
# avoids importing an unrelated TensorFlow installation if one is present.
os.environ["USE_TF"] = "0"

from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = os.getenv(
    "MODEL_NAME", "HuggingFaceTB/SmolLM2-135M-Instruct"
)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_MAX_NEW_TOKENS = 128

EXAMPLE_PROMPTS = [
    "Write a short story about a robot discovering the ocean.",
    "Explain machine learning to a beginner in five sentences.",
    "Write a professional email asking for a project update.",
    "Give me three ideas for a weekend project.",
    "Write a short paragraph about the future of artificial intelligence.",
]


def load_model() -> tuple[Any | None, Any | None, str | None]:
    """Load the tokenizer and model once, using the best available device."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model_kwargs = {
            "torch_dtype": (
                torch.float16
                if DEVICE == "cuda"
                else torch.bfloat16
            ),
            "low_cpu_mem_usage": True,
        }
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, **model_kwargs)
        model.to(DEVICE)
        model.eval()

        if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
            tokenizer.pad_token = tokenizer.eos_token

        return tokenizer, model, None
    except Exception as error:  # Keep the UI available so it can show the problem.
        return None, None, str(error)


TOKENIZER, MODEL, MODEL_LOAD_ERROR = load_model()


def _prepare_inputs(prompt: str) -> Any:
    """Format an instruction prompt when the tokenizer supports chat templates."""
    if hasattr(TOKENIZER, "apply_chat_template"):
        messages = [{"role": "user", "content": prompt.strip()}]
        return TOKENIZER.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True,
        )

    return TOKENIZER(prompt.strip(), return_tensors="pt")


@spaces.GPU(duration=120)
def generate_text(
    prompt: str,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
    progress: gr.Progress = gr.Progress(track_tqdm=True),
) -> str:
    """Generate a continuation for a prompt and return a user-friendly message."""
    if not isinstance(prompt, str) or not prompt.strip():
        return "Please enter a prompt before clicking Generate."

    if MODEL is None or TOKENIZER is None:
        detail = MODEL_LOAD_ERROR or "The model is not available."
        return f"Model loading failed. Restart the app after fixing the issue.\n\nDetails: {detail}"

    try:
        temperature = float(temperature)
        top_p = float(top_p)
        max_new_tokens = int(max_new_tokens)
    except (TypeError, ValueError):
        return "Generation settings must be numeric. Please check the sliders."

    if not 0.1 <= temperature <= 2.0:
        return "Temperature must be between 0.1 and 2.0."
    if not 0.1 <= top_p <= 1.0:
        return "Top-p must be between 0.1 and 1.0."
    if not 16 <= max_new_tokens <= 512:
        return "Maximum new tokens must be between 16 and 512."

    try:
        progress(0, desc="Preparing prompt")
        model_inputs = _prepare_inputs(prompt)
        model_inputs = {key: value.to(DEVICE) for key, value in model_inputs.items()}
        prompt_token_count = model_inputs["input_ids"].shape[-1]

        progress(0.25, desc="Generating response")
        with torch.inference_mode():
            generated_ids = MODEL.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=TOKENIZER.pad_token_id,
            )

        continuation_ids = generated_ids[:, prompt_token_count:]
        response = TOKENIZER.decode(
            continuation_ids[0],
            skip_special_tokens=True,
        ).strip()
        progress(1, desc="Done")

        return response or "The model returned an empty response. Try another prompt."
    except Exception as error:
        return f"Generation failed. Please try again.\n\nDetails: {error}"


def reset_interface() -> tuple[str, str, float, float, int]:
    """Clear the prompt and output and restore the starter settings."""
    return "", "", DEFAULT_TEMPERATURE, DEFAULT_TOP_P, DEFAULT_MAX_NEW_TOKENS


MODEL_STATUS = (
    f"Model: `{MODEL_NAME}` · Device: `{DEVICE}`"
    if MODEL is not None
    else f"Model unavailable: `{MODEL_NAME}` · Device: `{DEVICE}`"
)


with gr.Blocks(title="Text Generation") as demo:
    gr.Markdown("# Text Generation")
    gr.Markdown(
        "A simple demonstration of text generation using a pretrained "
        "language model. Adjust the controls to explore how generation changes."
    )
    gr.Markdown(MODEL_STATUS)

    with gr.Row():
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(
                label="Input prompt",
                placeholder="Enter an instruction or question...",
                lines=10,
            )
            temperature_slider = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=DEFAULT_TEMPERATURE,
                step=0.1,
                label="Temperature",
                info="Higher values make responses more varied.",
            )
            top_p_slider = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=DEFAULT_TOP_P,
                step=0.05,
                label="Top-p",
                info="Limits sampling to the most likely token choices.",
            )
            max_tokens_slider = gr.Slider(
                minimum=16,
                maximum=512,
                value=DEFAULT_MAX_NEW_TOKENS,
                step=8,
                label="Maximum new tokens",
                info="Sets the maximum length of the generated continuation.",
            )
            with gr.Row():
                generate_button = gr.Button("Generate", variant="primary")
                clear_button = gr.Button("Clear")

        with gr.Column(scale=1):
            output_text = gr.Textbox(
                label="Generated text",
                lines=19,
                show_copy_button=True,
            )

    gr.Markdown("### Example prompts")
    gr.Examples(
        examples=EXAMPLE_PROMPTS,
        inputs=prompt_input,
        label="Click an example to populate the prompt",
        cache_examples=False,
    )

    generate_button.click(
        fn=generate_text,
        inputs=[
            prompt_input,
            temperature_slider,
            top_p_slider,
            max_tokens_slider,
        ],
        outputs=output_text,
        show_progress="full",
    )
    clear_button.click(
        fn=reset_interface,
        inputs=None,
        outputs=[
            prompt_input,
            output_text,
            temperature_slider,
            top_p_slider,
            max_tokens_slider,
        ],
    )


def launch_app() -> None:
    """Launch locally, on Render, or with an optional temporary share link."""
    launch_kwargs = {"show_error": True}

    if os.getenv("GRADIO_SHARE", "").lower() in {"1", "true", "yes"}:
        launch_kwargs["share"] = True

    if os.getenv("PORT"):
        launch_kwargs["server_name"] = os.getenv(
            "GRADIO_SERVER_NAME", "0.0.0.0"
        )
        launch_kwargs["server_port"] = int(os.environ["PORT"])

    demo.queue().launch(**launch_kwargs)


if __name__ == "__main__":
    launch_app()
