import re
import time
from typing import List, Optional, Tuple
from deep_translator import GoogleTranslator
from .postprocessing import preprocess_text, postprocess_translated_text, ABBREVIATIONS, apply_modern_fixes



def translate_text_via_api(text: str) -> str:
    """
    Uses GoogleTranslator from deep_translator to translate text from English to Hindi.
    """
    try:
        return GoogleTranslator(source='en', target='hi').translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text


def mask_abbreviations(text: str) -> Tuple[str, dict]:
    replacements = {}
    for abbr in ABBREVIATIONS:
        pattern = r'\b' + re.escape(abbr) + r'\b'
        token = f"__{abbr}__"
        if re.search(pattern, text):
            text = re.sub(pattern, token, text)
            replacements[token] = abbr
    return text, replacements


def unmask_abbreviations(text: str, replacements: dict) -> str:
    for token, abbr in replacements.items():
        pattern = re.compile(re.escape(token), re.IGNORECASE)
        text = pattern.sub(abbr, text)
    return text


def translate_text(text: str, source: str, target: str) -> str:
    if not text or not text.strip() or source == target:
        return text

    masked_text, replacements = mask_abbreviations(text)
    translated = translate_text_via_api(masked_text.strip())
    translated = unmask_abbreviations(translated, replacements)
    translated = apply_modern_fixes(translated)  # ✅ Modern replacements
    return postprocess_translated_text(text, translated)



def translate_text_blocks(text_blocks: List[str], source: str, target: str, callback=None) -> List[str]:
    if not text_blocks:
        return []

    translated = []
    total = len(text_blocks)

    for i, block in enumerate(text_blocks):
        if callback:
            callback((i + 1) / total, f"Translating block {i + 1} of {total}")

        segments = preprocess_text(block)
        translated_segments = []

        for segment, should_translate in segments:
            if should_translate:
                translated_seg = translate_text(segment, source, target)
            else:
                translated_seg = segment
            translated_segments.append(translated_seg)

        translated_text = ''.join(translated_segments)
        translated.append(translated_text)

        if i < total - 1:
            time.sleep(0.1)

    return translated


def detect_language(text: str) -> Optional[str]:
    """
    Simple heuristic-based language detection: checks whether majority of characters are Devanagari (Hindi) or Latin.
    """
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
