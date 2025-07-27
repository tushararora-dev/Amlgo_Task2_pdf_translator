# 📄 PDF Translator (Hindi ↔ English)

This is a Streamlit-based web application that allows you to **translate PDF documents** between **Hindi and English**. The app supports intelligent text filtering, layout preservation, and a fallback mode for generating clean translated PDFs.
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

