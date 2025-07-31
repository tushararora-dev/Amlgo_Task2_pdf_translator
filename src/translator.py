import re
import json
import os
import time
import requests
from typing import List, Tuple, Optional
from dotenv import load_dotenv

# ========== Setup ==========
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
MODERN_REPLACEMENTS_PATH = "src/modern_replacements.json"

# ========== Language Codes ==========
MBART_LANG_CODES = {
    'en': 'en_XX',
    'hi': 'hi_IN'
}

# ========== Abbreviation Handling ==========
ABBREVIATIONS = {
    'AI', 'ML', 'API', 'URL', 'PDF', 'HTML', 'CSS', 'JS', 'SQL', 'JSON',
    'HTTP', 'HTTPS', 'NASA', 'FBI', 'CEO', 'CTO', 'PhD', 'MBA', 'USA',
    'UK', 'UAE', 'CPU', 'GPU', 'RAM', 'OCR', 'SAVE', 'FILE'
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

def mask_special_tokens(text: str) -> Tuple[str, dict]:
    replacements = {}
    for abbr in ABBREVIATIONS:
        pattern = r'\b' + re.escape(abbr) + r'\b'
        token = f"__{abbr}__"
        if re.search(pattern, text):
            text = re.sub(pattern, token, text)
            replacements[token] = abbr
    capital_words = re.findall(r'\b[A-Z]{3}\b', text)
    for word in capital_words:
        if word not in ABBREVIATIONS:
            token = f"__{word}__"
            text = text.replace(word, token)
            replacements[token] = word
    return text, replacements

def unmask_special_tokens(text: str, replacements: dict) -> str:
    for token, original in replacements.items():
        text = text.replace(token, original)
    return text

# ========== Modern Fixes ==========
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

# ========== Pre/Postprocessing ==========
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

# ========== Translation ==========
def translate_text_via_api(text: str, source: str, target: str) -> str:
    src_lang = MBART_LANG_CODES.get(source)
    tgt_lang = MBART_LANG_CODES.get(target)
    if not src_lang or not tgt_lang:
        print(f"❌ Unsupported language pair: {source} → {target}")
        return text
    payload = {
        "inputs": text,
        "parameters": {"src_lang": src_lang, "tgt_lang": tgt_lang}
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()[0]['translation_text']
        else:
            print("Translation API error:", response.status_code, response.text)
            return text
    except Exception as e:
        print("Translation error:", e)
        return text

def translate_text(text: str, source: str, target: str) -> str:
    if not text or not text.strip() or source == target:
        return text
    masked_text, replacements = mask_special_tokens(text)
    translated = translate_text_via_api(masked_text.strip(), source, target)
    translated = unmask_special_tokens(translated, replacements)
    translated = apply_modern_fixes(translated)
    return translated

def translate_text_blocks(text_blocks: List[str], source: str, target: str, callback=None) -> List[str]:
    if not text_blocks:
        return []
    translated = []
    total = len(text_blocks)
    for i, block in enumerate(text_blocks):
        if callback:
            callback((i + 1) / total, f"Translating block {i + 1} of {total}")
        segments = preprocess_text(block)
        translated_block = ""
        for segment, do_translate in segments:
            if do_translate:
                translated_segment = translate_text(segment, source, target)
            else:
                translated_segment = segment
            translated_block += postprocess_translated_text(segment, translated_segment)
        translated.append(translated_block)
        if i < total - 1:
            time.sleep(0.1)
    return translated

# ========== Language Detection ==========
def detect_language(text: str) -> Optional[str]:
    sample = text[:500].strip()
    if not sample:
        return None
    hindi_chars = sum(1 for char in sample if '\u0900' <= char <= '\u097F')
    latin_chars = sum(1 for char in sample if char.isalpha() and char.isascii())
    if hindi_chars > latin_chars:
        return 'hi'
    elif latin_chars > 0:
        return 'en'
    return None
