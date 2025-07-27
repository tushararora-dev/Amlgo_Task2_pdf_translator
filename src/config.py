# Supported languages
LANGUAGES = {
    'hindi': 'hi',
    'english': 'en'
}

# Translation directions
TRANSLATION_DIRECTIONS = {
    'Hindi to English': ('hi', 'en'),
    'English to Hindi': ('en', 'hi')
}

# File upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['pdf']

# Error messages
ERROR_MESSAGES = {
    'file_too_large': f'File size exceeds {MAX_FILE_SIZE_MB}MB limit',
    'invalid_format': 'Please upload a valid PDF file',
    'translation_failed': 'Translation failed. Please try again.',
    'pdf_generation_failed': 'Failed to generate translated PDF',
    'empty_pdf': 'The uploaded PDF appears to be empty or contains no extractable text'
}

# Success messages
SUCCESS_MESSAGES = {
    'translation_complete': 'Translation completed successfully!',
    'pdf_ready': 'Your translated PDF is ready for download'
}
