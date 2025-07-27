# 📄 PDF Translator (Hindi ↔ English)

This is a Streamlit-based web application that allows you to **translate PDF documents** between **Hindi and English**. The app supports intelligent text filtering, layout preservation, and a fallback mode for generating clean translated PDFs.


Working URL: https://amlgolabs-task2-pdf-translator.streamlit.app

![alt text](UI.png)

## 🚀 Features

- 🔤 Translate PDFs from **English to Hindi** and **Hindi to English**
- 📑 Preserve **PDF structure**: formatting, font size, colors, and bullet points
- 🧠 Use **Deep Translator** (Libra, Google, Microsoft) with **no API key needed**
- 📊 Extract and display **PDF statistics**: word count, estimated language, character count
- 🔎 Skip translation for abbreviations like NASA, AI, ML
- 📚 Supports **multi-page PDFs**, highlights, and links
- 🖼️ Handles **images and colored text**
- 🧪 Tested for real-world PDFs

---

## 🛠️ Tech Stack

| Area               | Tech Used          |                                                
|--------------------|--------------------|
| **Language**       | Python 3.10        |                                                    
| **Frontend/UI**    | Streamlit          |                                                   
| **PDF Reading**    | `PyMuPDF (fitz)`   |                   
| **PDF Writing**    | `PyMuPDF`          |                                
| **Translation**    | `Deep Translator`  | 
| **Deployment**     | Streamlit Cloud    |                                             

---

## 📁 Project Structure
![alt text](Task2_Folder_Structure.png)

---

## 🔁 Pipeline Flow

1. Upload PDF
2. Extract text blocks (with formatting preserved)
3. Skip non-translatable items (e.g., NASA, AI)
4. Translate content (Hindi ↔ English)
5. Rebuild PDF with original layout + translated text
6. Download the final output

---

## 🧪 PDF Test Cases

The tool has been tested on PDFs containing:
- 🖍️ Highlighted text
- 🖼️ Images
- 🎨 Colored fonts
- 🔗 Links
- 🔡 Abbreviations (AI, ML, NASA)
- 📄 Multi-page documents
- 🔤 Mixed language (Hindi + English)

---

---

## 🔧 Improvements & TODOs

- [ ] Handle **multiple PDFs** (Batch translations)
- [ ] Use **Classes and OOP** structure
- [ ] Add **logging** and **exception handling**
- [ ] Add **database** to store PDFs and stats
- [ ] Improve UI (statistics, filtering, etc.)
- [ ] Add **DevOps** practices for CI/CD
- [ ] Build a **simple offline version** (no APIs/libraries)
- [ ] Handle **bold/large fonts** more precisely
- [ ] Use **Sessions** and **Timeouts** for concurrent users
- [ ] Add better **language detection**
- [ ] Support **OCR and Table recognition** with PaddleOCR / UniLM DiT
- [ ] Enable **multithreading** or **batch translation** to speed up processing

---

## 🧠 Advanced Functionality

✅ **No API Key Needed**  
Used `Deep Translator` which allows unlimited usage of Google, Microsoft, or Libre Translate.

✅ **Custom Translator Possible**  
Optionally, a custom translation model (Transformer-based) can be trained and used instead of prebuilt models or APIs.

---

## ⚙️ How to Run Locally

```bash
# Step 1: Create environment
conda create --name pdftrans python=3.10
conda activate pdftrans

# Step 2: Install dependencies
pip install -r requirements.txt
pip install streamlit pymupdf deep-translator

# Step 3: Launch the app
streamlit run app.py


# Explanation of code

## Overview
The PDF Translator is a Streamlit-based web application that translates PDF documents between Hindi and English. It uses intelligent text filtering to preserve technical terms and formatting while providing accurate translations using Google Translate API.

## Project Structure
```
project_root/
├── app.py                 # Main Streamlit application
└── src/
    ├── config.py         # Configuration constants
    ├── pdf_reader.py     # PDF text extraction utilities
    ├── pdf_writer.py     # PDF generation utilities
    ├── translator.py     # Translation logic
    └── postprocessing.py # Text preprocessing and filtering
```

---

## File-by-File Analysis

### 1. config.py
**Purpose**: Central configuration file containing all constants, settings, and messages.

#### Constants:
- **LANGUAGES**: Mapping of language names to ISO codes
  - `'hindi': 'hi'`
  - `'english': 'en'`

- **TRANSLATION_DIRECTIONS**: Available translation pairs
  - `'Hindi to English': ('hi', 'en')`
  - `'English to Hindi': ('en', 'hi')`

- **File Settings**:
  - `MAX_FILE_SIZE_MB = 10`: Maximum upload size
  - `ALLOWED_EXTENSIONS = ['pdf']`: Supported file types

- **Error & Success Messages**: Centralized user feedback messages

---

### 2. pdf_reader.py
**Purpose**: Handles PDF validation, text extraction, and metadata retrieval using PyMuPDF.

#### Functions:

##### `validate_pdf(file_bytes: bytes) -> bool`
- **Purpose**: Validates if uploaded bytes form a valid PDF
- **Process**: Opens PDF stream and checks for errors
- **Returns**: Boolean indicating validity
- **Logging**: Prints validation status

##### `extract_text_blocks(file_bytes: bytes)`
- **Purpose**: Extracts structured text blocks with positioning data
- **Process**: 
  - Iterates through each page
  - Extracts text blocks with bounding boxes
  - Preserves layout information
- **Returns**: List of dictionaries containing:
  - `page`: Page number
  - `text`: Extracted text content
  - `bbox`: Bounding box coordinates
  - `block_type`: Type of block (text/image)
  - `block_no`: Block sequence number

##### `extract_simple_text(file_bytes: bytes) -> str`
- **Purpose**: Simple text extraction without layout preservation
- **Process**: Concatenates all page text with double newlines
- **Returns**: Plain text string
- **Use Case**: Fallback when layout preservation fails

##### `get_pdf_info(file_bytes: bytes)`
- **Purpose**: Retrieves PDF metadata and document properties
- **Returns**: Dictionary with:
  - `page_count`: Number of pages
  - `metadata`: Document metadata (title, author, etc.)
  - `is_encrypted`: Encryption status
  - `size_bytes`: File size
  - `page_width/height`: Page dimensions

##### `extract_images_info(file_bytes: bytes)`
- **Purpose**: Catalogs all images in the PDF
- **Process**: Scans each page for embedded images
- **Returns**: List of image metadata including position and dimensions

##### `has_extractable_text(file_bytes: bytes) -> bool`
- **Purpose**: Checks if PDF contains extractable text (not just images)
- **Use Case**: Prevents processing of image-only PDFs

---

### 3. pdf_writer.py
**Purpose**: Creates translated PDF documents with layout preservation.

#### Functions:

##### `create_translated_pdf(original_bytes: bytes, text_blocks: List[Dict], translated_texts: List[str]) -> bytes`
- **Purpose**: Main function for creating layout-preserved translated PDFs
- **Process**:
  1. Opens original PDF document
  2. Groups text blocks by page
  3. Creates overlay layer for translations
  4. Replaces original text with translations in same positions
  5. Uses HTML boxes for better text rendering
- **Features**:
  - Preserves original layout
  - Uses OCG (Optional Content Groups) for layering
  - Maintains font styling where possible

##### `add_translated_text_to_page(page, text_blocks: List[Dict], translated_texts: List[str])`
- **Purpose**: Adds translated text to a specific page
- **Process**: Places text at original block positions with preserved formatting

##### `create_simple_translated_pdf(translated_text: str, original_bytes: bytes = None) -> bytes`
- **Purpose**: Fallback function for simple text-based PDFs
- **Process**:
  - Creates new PDF with original dimensions
  - Flows translated text across pages
  - Uses consistent formatting
- **Use Case**: When layout preservation fails

##### `wrap_text(text: str, max_width: float) -> List[str]`
- **Purpose**: Text wrapping utility for proper line breaks
- **Algorithm**: Word-based wrapping with character width estimation

##### Helper Functions:
- `get_font_name(flags: int)`: Maps font flags to font names
- `get_text_color(color_int: int)`: Converts color integers to RGB tuples
- `add_simple_text_blocks()`: Adds text blocks to pages with automatic flow

---

### 4. postprocessing.py
**Purpose**: Intelligent text filtering and preprocessing before translation.

#### Key Features:

##### Smart Text Filtering
- **Abbreviations**: Maintains common technical terms (AI, ML, API, etc.)
- **URLs and Emails**: Preserves web addresses and email formats
- **Version Numbers**: Keeps software versions unchanged
- **File Names**: Preserves file extensions and technical names

##### Functions:

##### `should_skip_translation(text: str) -> bool`
- **Purpose**: Determines if text segment should be translated
- **Checks**:
  - Length validation (skip very short strings)
  - Abbreviation matching against predefined set
  - Pattern matching for numbers, symbols, URLs
  - Technical filename patterns
  - Version number formats
- **Returns**: Boolean indicating whether to skip translation

##### `preprocess_text(text: str) -> List[Tuple[str, bool]]`
- **Purpose**: Segments text into translatable and non-translatable parts
- **Process**:
  1. Tokenizes text into words and spaces
  2. Evaluates each token for translation necessity
  3. Groups consecutive tokens with same translation flag
- **Returns**: List of (text_segment, should_translate) tuples

##### `postprocess_translated_text(original: str, translated: str) -> str`
- **Purpose**: Preserves original whitespace formatting in translations
- **Process**: Maintains leading and trailing spaces from original text

---

### 5. translator.py
**Purpose**: Core translation functionality with caching and error handling.

#### Functions:

##### `get_translator(source: str, target: str) -> GoogleTranslator`
- **Purpose**: Manages translator instances with caching
- **Benefit**: Avoids recreating translator objects, improving performance
- **Implementation**: Dictionary-based caching by language pair

##### `translate_text_segment(text: str, source: str, target: str, max_retries: int = 3) -> str`
- **Purpose**: Translates individual text segments with retry logic
- **Features**:
  - Automatic retry on failure (up to 3 attempts)
  - Delay between retries to handle rate limiting
  - Fallback to original text on persistent failure
- **Post-processing**: Applies whitespace preservation

##### `translate_text(text: str, source: str, target: str) -> str`
- **Purpose**: Main text translation function with intelligent filtering
- **Process**:
  1. Validates input and language parameters
  2. Preprocesses text to identify translation segments
  3. Translates only necessary segments
  4. Reassembles text maintaining original structure
- **Optimization**: Skips translation for same source-target languages

##### `translate_text_blocks(text_blocks: List[str], source: str, target: str, callback=None) -> List[str]`
- **Purpose**: Batch translation with progress tracking
- **Features**:
  - Progress callback for UI updates
  - Rate limiting between requests
  - Handles empty or invalid blocks gracefully

##### `detect_language(text: str) -> Optional[str]`
- **Purpose**: Automatic language detection for uploaded documents
- **Algorithm**:
  - Analyzes character distribution in text sample
  - Counts Hindi Unicode characters vs Latin characters
  - Returns language code based on predominant script
- **Use Case**: Auto-detection for better user experience

---

### 6. app.py
**Purpose**: Main Streamlit application orchestrating the entire translation workflow.

#### UI Components:

##### `render_sidebar()`
- **Features**:
  - Application information and capabilities
  - Interactive text filtering demo
  - Real-time translation testing
- **Educational Value**: Shows users how intelligent filtering works

##### `render_header()`
- **Purpose**: Application title and description
- **Branding**: Clear identification of functionality

##### `render_file_upload()`
- **Validation Process**:
  1. File size checking against configured limits
  2. PDF format validation
  3. Text extractability verification
  4. Metadata display (pages, size, dimensions)
- **User Feedback**: Clear error messages for invalid files
- **Returns**: Validated file object or None

##### `render_translation_direction()`
- **Purpose**: Language pair selection interface
- **Features**:
  - Dropdown selection from configured directions
  - Visual confirmation of source and target languages
- **Returns**: Source and target language codes

##### `run_translation(uploaded_file, source_lang, target_lang)`
- **Purpose**: Main translation workflow execution
- **Process**:
  1. **Text Extraction**: Extracts structured text blocks
  2. **Progress Tracking**: Real-time progress updates
  3. **Translation**: Batch processing with callbacks
  4. **PDF Generation**: Creates translated document
  5. **Fallback Handling**: Simple layout if complex fails
  6. **Session Management**: Stores results for download
- **Error Handling**: Graceful degradation for various failure modes

##### `render_download_section()`
- **Features**:
  - Download button for translated PDF
  - Automatic filename generation with "_translated" suffix
  - Session state management
  - Reset functionality for new translations

##### `main()`
- **Purpose**: Application orchestration
- **Flow Control**: Manages UI component rendering and state
- **Configuration**: Sets page layout and metadata

---

## Technical Architecture

### Key Design Patterns:
1. **Separation of Concerns**: Each module handles specific functionality
2. **Error Handling**: Comprehensive validation and fallback mechanisms
3. **Progress Feedback**: Real-time user feedback during long operations
4. **Caching**: Translator instance caching for performance
5. **State Management**: Streamlit session state for workflow continuity

### Dependencies:
- **PyMuPDF (fitz)**: PDF manipulation and text extraction
- **deep-translator**: Google Translate API access
- **Streamlit**: Web application framework
- **Regular Expressions**: Text pattern matching and validation

### Performance Optimizations:
- Translator instance caching
- Intelligent text filtering to reduce API calls
- Progress callbacks for user experience
- Batch processing with rate limiting
- Fallback rendering strategies

### Error Handling Strategy:
- File validation at upload
- PDF format verification
- Text extractability checking
- Translation retry logic
- Graceful degradation to simple layouts
- Comprehensive user feedback

---

## Usage Workflow

1. **Upload**: User uploads PDF file (max 10MB)
2. **Validation**: System validates file format and extractability
3. **Direction**: User selects translation direction (Hindi↔English)
4. **Processing**: System extracts text, applies intelligent filtering, and translates
5. **Generation**: Creates new PDF preserving original layout
6. **Download**: User downloads translated document

## Future Enhancement Opportunities

1. **Multi-language Support**: Extended language pairs
2. **OCR Integration**: Support for image-based PDFs
3. **Batch Processing**: Multiple file uploads
4. **Custom Dictionaries**: User-defined term preservation
5. **Advanced Layout**: Better font matching and styling
6. **Cloud Storage**: Integration with cloud storage services

---

*This documentation covers the complete PDF Translator application architecture, providing detailed insights into each component's functionality and design rationale.*