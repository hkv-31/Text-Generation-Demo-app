"""Gradio user interface for the OpenAI text-generation demo."""

from __future__ import annotations

import os

import gradio as gr

from llm import DEFAULT_MODEL, generate_text


DEFAULT_TASK = "Creative Writing"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 300

EXAMPLES = {
    "Creative Writing": [
        "Write a short story about a student who discovers an AI assistant that can predict the future.",
        "Write a creative paragraph describing a city on Mars.",
    ],
    "Question Answering": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain transformers in simple terms.",
    ],
    "Summarization": [
        (
            "Artificial intelligence is a field of computer science focused on building "
            "systems that can perform tasks that normally require human intelligence. "
            "These systems can learn from data, recognize patterns, understand language, "
            "and support decision-making. AI is used in areas such as healthcare, "
            "education, transportation, and customer service."
        ),
        (
            "Machine learning allows computers to learn patterns from examples instead of "
            "following only explicitly programmed rules. A model is trained on data, "
            "evaluated on examples it has not seen, and then used to make predictions "
            "or generate useful outputs."
        ),
    ],
}


def clear_form() -> tuple[str, str, str, float, int]:
    """Restore the task, prompt, output, and controls to their defaults."""

    return DEFAULT_TASK, "", "", DEFAULT_TEMPERATURE, DEFAULT_MAX_OUTPUT_TOKENS


def build_demo() -> gr.Blocks:
    """Create the Gradio application without starting the server."""

    with gr.Blocks(title="AI Text Generation App") as demo:
        gr.Markdown("# AI Text Generation App")
        gr.Markdown(
            "Generate creative writing, answers, or summaries with an OpenAI language model. "
            "Choose a task, enter text, adjust the controls, and select **Generate**."
        )
        gr.Markdown(
            f"**Model:** `{DEFAULT_MODEL}`  \n"
            "**Inference:** OpenAI Responses API (server-side)"
        )

        with gr.Row():
            with gr.Column(scale=1):
                task_dropdown = gr.Dropdown(
                    choices=list(EXAMPLES),
                    value=DEFAULT_TASK,
                    label="Task",
                    info="The selected task changes the model instructions.",
                )
                prompt_input = gr.Textbox(
                    label="Input",
                    placeholder="Enter your prompt or text here...",
                    lines=10,
                )
                temperature_slider = gr.Slider(
                    minimum=0.0,
                    maximum=1.5,
                    value=DEFAULT_TEMPERATURE,
                    step=0.1,
                    label="Temperature",
                    info="Lower values are more predictable; higher values are more varied.",
                )
                max_tokens_slider = gr.Slider(
                    minimum=50,
                    maximum=500,
                    value=DEFAULT_MAX_OUTPUT_TOKENS,
                    step=10,
                    label="Maximum Output Tokens",
                    info="Limits the maximum length of the generated response.",
                )
                with gr.Row():
                    generate_button = gr.Button("Generate", variant="primary")
                    clear_button = gr.Button("Clear")

            with gr.Column(scale=1):
                output_text = gr.Textbox(
                    label="Generated Response",
                    lines=20,
                    show_copy_button=True,
                )

        gr.Markdown("### Example Prompts")
        for task_name, prompts in EXAMPLES.items():
            gr.Examples(
                examples=[[task_name, prompt] for prompt in prompts],
                inputs=[task_dropdown, prompt_input],
                label=task_name,
                cache_examples=False,
            )

        generation_inputs = [
            prompt_input,
            task_dropdown,
            temperature_slider,
            max_tokens_slider,
        ]
        generate_button.click(
            fn=generate_text,
            inputs=generation_inputs,
            outputs=output_text,
            show_progress="full",
        )
        clear_button.click(
            fn=clear_form,
            inputs=None,
            outputs=[
                task_dropdown,
                prompt_input,
                output_text,
                temperature_slider,
                max_tokens_slider,
            ],
        )

    return demo


def launch_app() -> None:
    """Launch locally or on Render using the platform-provided port."""

    server_port = int(os.getenv("PORT", "7860"))
    demo = build_demo()
    demo.queue().launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
        server_port=server_port,
        show_error=True,
    )


if __name__ == "__main__":
    launch_app()
