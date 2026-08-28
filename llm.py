"""OpenAI Responses API logic for the text-generation demo."""

from __future__ import annotations

import logging
import os
from typing import Any

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    BadRequestError,
    OpenAI,
    RateLimitError,
)


load_dotenv()

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

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
    """Convert common SDK errors into messages suitable for the UI."""

    if isinstance(error, AuthenticationError):
        return "The OpenAI API key was rejected. Check the key in your environment settings."
    if isinstance(error, RateLimitError):
        return "The OpenAI rate limit was reached. Please wait a moment and try again."
    if isinstance(error, APIConnectionError):
        return "The connection to OpenAI failed. Check your network and try again."
    if isinstance(error, BadRequestError):
        return "OpenAI rejected the request. Check the selected model and input values."
    if isinstance(error, APIError):
        return "OpenAI is temporarily unavailable. Please try again shortly."
    return "Unable to generate a response right now. Please check your configuration and try again."


def generate_text(
    prompt: str,
    task: str,
    temperature: float,
    max_output_tokens: int,
    client: Any | None = None,
) -> str:
    """Generate text using task-specific instructions and the OpenAI Responses API."""

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

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key and client is None:
        return "OpenAI API key is not configured. Add OPENAI_API_KEY and try again."

    try:
        openai_client = client or OpenAI(api_key=api_key)
        response = openai_client.responses.create(
            model=DEFAULT_MODEL,
            instructions=TASK_INSTRUCTIONS[task],
            input=prompt.strip(),
            temperature=temperature_value,
            max_output_tokens=max_tokens_value,
            store=False,
        )
        generated_text = response.output_text.strip()
        return generated_text or "The model returned an empty response. Please try again."
    except (AuthenticationError, RateLimitError, APIConnectionError, BadRequestError, APIError) as error:
        LOGGER.error("OpenAI request failed with %s", type(error).__name__)
        return _friendly_api_error(error)
    except Exception as error:  # Defensive boundary for a user-facing demo.
        LOGGER.error("Unexpected generation failure with %s", type(error).__name__)
        return _friendly_api_error(error)
