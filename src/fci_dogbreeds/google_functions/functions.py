"""Google API Functions"""

import json
import logging
from typing import List, Optional
from google import genai
from google.genai import types, errors
from pydantic import BaseModel
from fci_dogbreeds.config import DATA_PROMPTS, PROMPT_LANGUAGES, GOOGLE_API_KEY

logger = logging.getLogger(__name__)


# 1. Define the desired JSON structure with Pydantic
class BreedGroup(BaseModel):
    """ BaseModel for breedgroup """
    fci_group: int
    group_name: str
    breeds: List[str]


class LanguageDataset(BaseModel):
    """ BaseModel for language dataset """
    groups: List[BreedGroup]


def _get_client() -> genai.Client:
    """Lazily initialize and return the Gemini client."""
    # 2. Initialize the Gemini Client (lazy initialization)
    _client: Optional[genai.Client] = None
    if _client is None:
        # Ensure the GEMINI_API_KEY environment variable is set on your system,
        # or provide it directly here: client = genai.Client(api_key="YOUR_API_KEY")
        api_key = GOOGLE_API_KEY
        if not api_key:
            raise ValueError(
                "No API key was provided. Please set the GOOGLE_API_KEY environment variable "
                "or ensure it's configured properly. Learn how to create an API key at "
                "https://ai.google.dev/gemini-api/docs/api-key"
            )
        _client = genai.Client(api_key=api_key)
    return _client

def get_data_from_gemini(language: str) -> dict:
    """Sends a prompt to Gemini and enforces structured JSON output."""
    logger.info("Fetching FCI data for language: %s...", PROMPT_LANGUAGES[language])

    prompt = DATA_PROMPTS.get(language,"EN")

    # Use gemini-3.6-flash with Chat API as recommended by Google
    client = _get_client()
    try:
        # Create a chat session with the model and send message using the recommended Chat API
        chat = client.chats.create(model="gemini-3.6-flash")
        response = chat.send_message(
            message=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LanguageDataset,  # Forces Gemini to follow the Pydantic structure
                temperature=0.1,  # Low temperature for consistent and accurate data
            ),
        )
        return json.loads(str(response.text))

    except errors.ClientError as e:
        if e.code == 429:
            logger.warning("Rate limit hit (429). Retry with exponential backoff.")
            raise e
        logger.error("Invalid API request or Authentication problem: %s", e)
        raise e

    except errors.ServerError as e:
        logger.warning("Google Gemini servers are temporarily struggling: %s", e)
        raise e

    except json.JSONDecodeError as json_err:
        logger.error("Gemini schema returned invalid JSON strings: %s", json_err)
        raise json_err

    except Exception as unexpected_err:
        logger.error("Unanticipated bug outside Gemini pipeline: %s", unexpected_err)
        raise unexpected_err
