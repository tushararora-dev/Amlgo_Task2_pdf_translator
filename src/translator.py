from deep_translator import GoogleTranslator
from typing import List, Optional
import time
from .postprocessing import preprocess_text, postprocess_translated_text
from .config import LANGUAGES

translator_cache = {}

def get_translator(source: str, target: str) -> GoogleTranslator:
    key = f"{source}_{target}"
    if key not in translator_cache:
        translator_cache[key] = GoogleTranslator(source=source, target=target)
    return translator_cache[key]

def translate_text_segment(text: str, source: str, target: str, max_retries: int = 3) -> str:
    if not text.strip():
        return text
    translator = get_translator(source, target)
    for _ in range(max_retries):
        translated = translator.translate(text.strip())
        if translated:
            return postprocess_translated_text(text, translated)
        time.sleep(1)
    return text

def translate_text(text: str, source: str, target: str) -> str:
    if not text or not text.strip() or source == target:
        return text
    # Skip intelligent segmentation, translate full text
    translated = translate_text_segment(text, source, target)
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
        translated_segments = []

        for segment, should_translate in segments:
            if should_translate:
                translated_seg = translate_text_segment(segment, source, target)
            else:
                translated_seg = segment  # Leave it as-is
            translated_segments.append(translated_seg)

        # Join the segments together
        translated_text = ''.join(translated_segments)
        translated.append(translated_text)

        if i < total - 1:
            time.sleep(0.1)

    return translated

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
