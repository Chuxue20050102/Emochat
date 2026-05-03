import os
from typing import Optional

from openai import OpenAI

from services.ai.config import DASHSCOPE_BASE_URL

_client: Optional[OpenAI] = None


def get_api_key() -> Optional[str]:
    return os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")


def get_client() -> Optional[OpenAI]:
    global _client
    if _client is not None:
        return _client

    api_key = get_api_key()
    if not api_key:
        return None

    _client = OpenAI(api_key=api_key, base_url=DASHSCOPE_BASE_URL)
    return _client


# Backward-compatible private names used by earlier modules/tests.
_get_api_key = get_api_key
_get_client = get_client
