"""Groq API logic for the text-generation demo."""

from __future__ import annotations

import logging
import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

TASK_INSTRUCTIONS = {
    "Creative Writing": (
        "Create coherent, engaging writing based on the user's request. "
        "Follow the requested tone, format, and length."
    ),
    "Question Answering": (
        "Answer the user's question clearly and accurately. "
        "Use simple explanations when helpful and state uncertainty when needed."
    ),
    "Summarization": (
        "Summarize the supplied text concisely while preserving its main ideas, "
        "important details, and original meaning."
    ),
}


def _friendly_api_error(error: Exception) -> str:
    """Convert common Groq SDK errors into a message suitable for the UI."""

    error_name = type(error).__name__.lower()
    error_message = str(error).lower()

    if any(term in error_name or term in error_message for term in ("auth", "api key", "unauthorized", "permission")):
        return "The Groq API key was rejected. Check the key in your environment settings."
    if any(term in error_name or term in error_message for term in ("rate", "quota", "429", "resource")):
        return "The Groq rate limit or quota was reached. Please wait and try again."
    if any(term in error_name or term in error_message for term in ("connection", "timeout", "network")):
        return "The connection to Groq failed. Check your network and try again."
    if any(term in error_name or term in error_message for term in ("badrequest", "invalid", "notfound", "400")):
        return "Groq rejected the request. Check the selected model and input values."
    return "Unable to generate a response right now. Please check your configuration and try again."


def generate_text(
    prompt: str,
    task: str,
    temperature: float,
    max_output_tokens: int,
    client: Any | None = None,
) -> str:
    """Generate text with task instructions and the Groq chat completions API."""

    if not isinstance(prompt, str) or not prompt.strip():
        return "Please enter a prompt or some text before generating a response."

    if task not in TASK_INSTRUCTIONS:
        return "Please select a valid task."

    try:
        temperature_value = float(temperature)
        max_tokens_value = int(max_output_tokens)
    except (TypeError, ValueError):
        return "Temperature and maximum output tokens must be valid numbers."

    if not 0.0 <= temperature_value <= 1.5:
        return "Temperature must be between 0.0 and 1.5."
    if not 50 <= max_tokens_value <= 500:
        return "Maximum output tokens must be between 50 and 500."

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key and client is None:
        return "Groq API key is not configured. Add GROQ_API_KEY and try again."

    try:
        groq_client = client or Groq(api_key=api_key)
        completion = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": TASK_INSTRUCTIONS[task]},
                {"role": "user", "content": prompt.strip()},
            ],
            temperature=temperature_value,
            max_tokens=max_tokens_value,
        )
        generated_text = (completion.choices[0].message.content or "").strip()
        return generated_text or "The model returned an empty response. Please try again."
    except Exception as error:  # noqa: BLE001 - keep unexpected SDK errors user-friendly.
        LOGGER.error("Groq request failed with %s", type(error).__name__)
        return _friendly_api_error(error)
