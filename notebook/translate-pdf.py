import argparse
from fpdf import FPDF
from unidecode import unidecode
from langchain.document_loaders import PyPDFLoader
import openai
import tiktoken

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

client = openai.OpenAI()


def get_translation(page, input_language, target_language):
    prompt = f"Translate this page from {input_language} to {target_language}, output\
     only the translation, not the original text.\n\nEnglish: {page}\nPortuguese:"
 
    response = client.chat.completions.create(
         model="gpt-4-0125-preview",
         messages=[{"role": "system", "content": f"You are an expert translator from {input_language} to {target_language} papers about machine learning."},
                  {"role": "user", "content": prompt}],)
 
    return response.choices[0].message.content

def get_translations(pages, input_language, output_language):
    translations = []
    for i in range(0, len(pages), 2):
        batch = pages[i:i+1]
        combined_pages = "\n\n".join(batch)
        if len(enc.encode(combined_pages))>4096:
            batch = pages[i:i+1]
            combined_pages = "\n\n".join(batch)
            # Get translations and extend the list
            combined_translation = get_translation(combined_pages, input_language=input_language, target_language=output_language)
            translated_pages = combined_translation.split("\n\n")
            translations.extend(translated_pages)
            fourth_page = pages[i+1]
            translation = get_translation(fourth_page, input_language=input_language, target_language=output_language)
            translations.append(translation)
        else:
            # Get translations and extend the list
            combined_translation = get_translation(combined_pages, input_language=input_language, target_language=output_language)
            translated_pages = combined_translation.split("\n\n")
            translations.extend(translated_pages)
        
    return translations


def create_pdf(pages, output_file="translated.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Times", size=12)

    for page in pages:
        pdf.add_page()
        pdf.multi_cell(0, 10, unidecode(page))


    pdf.output(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate and create PDF from a PDF file")
    parser.add_argument("-i", type=str, help="Path to the input PDF file")
    parser.add_argument("-o", type=str, default="./output_translated.pdf",help="Path to the output PDF file")
    parser.add_argument("-il", type=str, default="english", help="Input language")
    parser.add_argument("-ol", type=str, default="hindi", help="Output language")
    args = parser.parse_args()

    # Load and split the PDF
    loader = PyPDFLoader(args.i)
    pdf_doc = loader.load_and_split()
    content = [page.page_content for page in pdf_doc]

    # Translate the content
    translated_content = get_translations(content,input_language=args.il, output_language=args.ol)

    # Create the PDF
    create_pdf(translated_content, output_file=args.o)
