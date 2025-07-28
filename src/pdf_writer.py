import pymupdf as fitz
from typing import List, Dict, Tuple

DEFAULT_FONT = "helv"
DEFAULT_FONT_SIZE = 12

def create_translated_pdf(original_bytes: bytes, text_blocks: List[Dict], translated_texts: List[str]) -> bytes:
    doc = fitz.open(stream=original_bytes, filetype="pdf")
    WHITE = fitz.pdfcolor["white"]
    ocg = doc.add_ocg("Translated", on=True)

    blocks_by_page = {}
    for i, block in enumerate(text_blocks):
        page_num = block['page']
        if page_num not in blocks_by_page:
            blocks_by_page[page_num] = []
        if i < len(translated_texts):
            blocks_by_page[page_num].append((block, translated_texts[i]))

    for page_num, page_blocks in blocks_by_page.items():
        page = doc[page_num]
        for block, translated_text in page_blocks:
            if translated_text.strip():
                x0, y0, x1, y1 = block['bbox']
                # Expand vertical height slightly
                y1 = y1 + 10  # increase 6 points or more
                bbox = (x0, y0, x1, y1)
                page.draw_rect(bbox, color=None, fill=WHITE, oc=ocg)
                translated_html = translated_text.replace('\n', '<br>')
                page.insert_htmlbox(
                    bbox,
                    translated_html,
                    css="* {font-family: sans-serif; font-size: 12px;}",
                    oc=ocg
                )

    doc.subset_fonts()
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def add_translated_text_to_page(page, text_blocks: List[Dict], translated_texts: List[str]):
    for i, (block, translated_text) in enumerate(zip(text_blocks, translated_texts)):
        if not translated_text.strip():
            continue
        bbox = fitz.Rect(block['bbox'])
        font_size = max(8, min(block.get('size', DEFAULT_FONT_SIZE), 24))
        font = get_font_name(block.get('flags', 0))
        color = get_text_color(block.get('color', 0))
        page.insert_text(
            (bbox.x0, bbox.y0 + font_size),
            translated_text,
            fontsize=font_size,
            fontname=font,
            color=color
        )

def add_simple_text_blocks(page, texts: List[str]):
    y_position = 50
    line_height = 16
    for text in texts:
        if not text.strip():
            continue
        lines = wrap_text(text, page.rect.width - 100)
        for line in lines:
            if y_position > page.rect.height - 50:
                break
            page.insert_text((50, y_position), line, fontsize=DEFAULT_FONT_SIZE)
            y_position += line_height

# main margin or width of text
def wrap_text(text: str, max_width: float) -> List[str]:
    words = text.split()
    lines = []
    current_line = ""
    char_width = DEFAULT_FONT_SIZE * 0.6
    max_chars = int(max_width / char_width)

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def get_font_name(flags: int) -> str:
    if flags & 16:
        return "helv-boldoblique" if flags & 2 else "helv-bold"
    elif flags & 2:
        return "helv-oblique"
    return "helv"

def get_text_color(color_int: int) -> Tuple[float, float, float]:
    if color_int == 0:
        return (0, 0, 0)
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return (r / 255, g / 255, b / 255)


# preserving the original PDF's page size
def create_simple_translated_pdf(translated_text: str, original_bytes: bytes = None) -> bytes:
    doc = fitz.open()
    if original_bytes:
        orig_doc = fitz.open(stream=original_bytes, filetype="pdf")
        if len(orig_doc) > 0:
            page_width = orig_doc[0].rect.width
            page_height = orig_doc[0].rect.height
        else:
            page_width, page_height = fitz.paper_size("a4")
        orig_doc.close()
    else:
        page_width, page_height = fitz.paper_size("a4")

    page = doc.new_page(width=page_width, height=page_height)
    margin = 50
    line_height = 16
    y_position = margin

    lines = translated_text.split('\n')
    for line in lines:
        if y_position > page_height - margin:
            page = doc.new_page(width=page_width, height=page_height)
            y_position = margin
        if line.strip():
            wrapped_lines = wrap_text(line, page_width - 2 * margin)
            for wrapped_line in wrapped_lines:
                page.insert_text((margin, y_position), wrapped_line, fontsize=DEFAULT_FONT_SIZE)
                y_position += line_height
        else:
            y_position += line_height

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes
