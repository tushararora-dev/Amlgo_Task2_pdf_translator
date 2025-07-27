import re
from typing import List, Tuple

# Common abbreviations and patterns to skip
ABBREVIATIONS = {'AI', 'ML', 'API', 'URL', 'PDF', 'HTML', 'CSS', 'JS', 'SQL', 'JSON', 'HTTP', 'HTTPS',
                 'NASA', 'FBI', 'CEO', 'CTO', 'PhD', 'MBA', 'USA', 'UK', 'UAE', 'CPU', 'GPU'}

def should_skip_translation(text: str) -> bool:
    text = text.strip()
    if len(text) < 2:
        return True

    # Remove trailing punctuation for abbreviation check
    clean = re.sub(r'[^\w]', '', text).upper()
    if clean in ABBREVIATIONS:
        return True

    if re.fullmatch(r'^[\d\W_]+$', text):  # numbers, symbols, punctuation
        return True
    if re.search(r'(http|www\.|@|\.com|\.pdf|\.png)', text.lower()):
        return True
    if re.fullmatch(r'[A-Z0-9_\-\.]+', text):  # like FILE_NAME_123.PDF
        return True
    if re.fullmatch(r'v?\d+(\.\d+)*([a-zA-Z]+\d*)?', text):  # versions like 1.0.2a
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

