import json
import re
import sys


def safe_print(msg: str) -> None:
    try:
        print(msg)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        print(msg.encode(encoding, errors="replace").decode(encoding))


def llm_json_parse(text: str) -> dict:
    content = (text or "").strip()
    if not content:
        return {}

    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?", "", content).strip()
        content = re.sub(r"```$", "", content).strip()

    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        content = match.group(0)

    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        return {}
    return {}
