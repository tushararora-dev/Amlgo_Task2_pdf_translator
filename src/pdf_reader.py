import pymupdf as fitz

def validate_pdf(file_bytes: bytes) -> bool:
    print("Validating PDF...")
    fitz.open(stream=file_bytes, filetype="pdf").close()
    print("PDF is valid.")
    return True

def extract_text_blocks(file_bytes: bytes):
    print("Extracting text blocks from PDF...")
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    blocks_info = []
    for page_num, page in enumerate(doc):
        print(f"Processing page {page_num + 1}/{len(doc)}")
        for block in page.get_text("blocks", flags=fitz.TEXT_DEHYPHENATE):
            if len(block) >= 5 and block[4].strip():
                blocks_info.append({
                    'page': page_num,
                    'text': block[4],
                    'bbox': block[:4],
                    'block_type': block[5] if len(block) > 5 else 0,
                    'block_no': block[6] if len(block) > 6 else 0
                })
    doc.close()
    print(f"Total text blocks extracted: {len(blocks_info)}")
    return blocks_info

def extract_simple_text(file_bytes: bytes) -> str:
    print("Extracting simple text from PDF...")
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n\n".join(page.get_text() for page in doc)
    doc.close()
    print(f"Total characters extracted: {len(text)}")
    return text.strip()

def get_pdf_info(file_bytes: bytes):
    print("Getting PDF metadata and info...")
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    rect = doc[0].rect if doc else None
    info = {
        'page_count': len(doc),
        'metadata': doc.metadata,
        'is_encrypted': doc.is_encrypted,
        'size_bytes': len(file_bytes),
        'page_width': rect.width if rect else None,
        'page_height': rect.height if rect else None,
    }
    doc.close()
    print(f"PDF Info: {info}")
    return info

def extract_images_info(file_bytes: bytes):
    print("Extracting image info from PDF...")
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []
    for page_num, page in enumerate(doc):
        image_list = page.get_images()
        print(f"Page {page_num + 1}: Found {len(image_list)} images")
        for idx, img in enumerate(image_list):
            images.append({
                'page': page_num,
                'index': idx,
                'xref': img[0],
                'bbox': page.get_image_bbox(img),
                'width': img[2],
                'height': img[3]
            })
    doc.close()
    print(f"Total images extracted: {len(images)}")
    return images

def has_extractable_text(file_bytes: bytes) -> bool:
    print("Checking if PDF has extractable text...")
    result = bool(extract_simple_text(file_bytes).strip())
    print(f"Text extractable: {result}")
    return result
