from huggingface_hub import InferenceClient

def build_prompt(text: str, source_lang: str, target_lang: str) -> str:
    if source_lang in ['en', 'english'] and target_lang in ['hi', 'hindi']:
        return f"""You are a highly skilled English-to-Hindi translator.

Your task is to translate the following English sentence into accurate, grammatically correct, and natural Hindi.

🚫 STRICT RULES:
1. DO NOT translate or transliterate abbreviations or acronyms (e.g., AI, NASA, API, URL)
2. DO NOT translate or transliterate FULLY CAPITALIZED words (e.g., PDF, HTML, FILE, SAVE, ML, JSON) — keep them **exactly** as written
3. DO NOT modify formatting or punctuation
4. Maintain technical terms, brand names, and code terms **as-is**
5. Respond with ONLY the translation — no extra notes, no formatting

English: {text}

Hindi:"""

    elif source_lang in ['hi', 'hindi'] and target_lang in ['en', 'english']:
        return f"""You are a highly skilled Hindi-to-English translator.

Your task is to translate the following Hindi sentence into fluent, natural English.

🚫 STRICT RULES:
1. DO NOT translate or transliterate abbreviations or acronyms (e.g., AI, NASA, API, URL)
2. DO NOT translate or transliterate FULLY CAPITALIZED words (e.g., PDF, HTML, FILE, SAVE, ML, JSON) — keep them **exactly** as written
3. DO NOT modify formatting or punctuation
4. Maintain technical terms, brand names, and capital code words as-is
5. Respond with ONLY the translation — no extra notes, no formatting

Hindi: {text}

English:"""

    else:
        return f"[Error: Unsupported language direction: {source_lang} → {target_lang}]"


def run_llama_translation(prompt: str, token: str) -> str:
    client = InferenceClient(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        token=token
    )

    messages = [{"role": "user", "content": prompt}]
    response = client.chat_completion(
        messages=messages,
        max_tokens=2000,
        temperature=0.2
    )

    if response and response.choices:
        result = response.choices[0].message.content.strip()

        if result.lower().startswith("english:"):
            return result.split(":", 1)[-1].strip()
        if result.lower().startswith("hindi:"):
            return result.split(":", 1)[-1].strip()
        return result

    return "[Error: No translation received]"
