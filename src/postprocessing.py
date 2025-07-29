import re
import json
from typing import List, Tuple

# Path to modern replacements JSON
MODERN_REPLACEMENTS_PATH = "src\modern_replacements.json"

# Abbreviations to preserve during translation
ABBREVIATIONS = {
    'AI', 'ML', 'API', 'URL', 'PDF', 'HTML', 'CSS', 'JS', 'SQL', 'JSON',
    'HTTP', 'HTTPS', 'NASA', 'FBI', 'CEO', 'CTO', 'PhD', 'MBA', 'USA',
    'UK', 'UAE', 'CPU', 'GPU','RAM'
}

def should_skip_translation(text: str) -> bool:
    text = text.strip()
    if len(text) < 2 and text.lower() != 'a':
        return True

    clean = re.sub(r'[^\w]', '', text).upper()
    if clean in ABBREVIATIONS:
        return True

    if re.fullmatch(r'^[\d\W_]+$', text):
        return True
    if re.search(r'(http|www\.|@|\.com|\.pdf|\.png)', text.lower()):
        return True
    if re.fullmatch(r'[A-Z0-9_\-\.]+', text):
        return True
    if re.fullmatch(r'v?\d+(\.\d+)*([a-zA-Z]+\d*)?', text):
        return True
    return False


def preprocess_text(text: str) -> List[Tuple[str, bool]]:
    words = re.findall(r'\S+|\s+', text)
    segments = []
    current = ""
    current_flag = None

    for token in words:
        if token.isspace():
            current += token
            continue

        flag = not should_skip_translation(token)

        if current_flag is None or flag == current_flag:
            current += token
        else:
            if current.strip():
                segments.append((current, current_flag))
            current = token
        current_flag = flag

    if current.strip():
        segments.append((current, current_flag))
    return segments


def postprocess_translated_text(original: str, translated: str) -> str:
    leading_spaces = len(original) - len(original.lstrip())
    trailing_spaces = len(original) - len(original.rstrip())
    return ' ' * leading_spaces + translated.strip() + ' ' * trailing_spaces


# Load modern replacements from external JSON
def load_modern_replacements() -> dict:
    try:
        with open(MODERN_REPLACEMENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Could not load modern_replacements.json:", e)
        return {}

modern_replacements = load_modern_replacements()

def apply_modern_fixes(text: str) -> str:
    for wrong, right in modern_replacements.items():
        text = text.replace(wrong, right)
    return text
