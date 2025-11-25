from PyPDF2 import PdfReader
import docx

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        reader=PdfReader(file_path)
        text=''
        for page in reader.pages:
            text+=page.extract_text()+'\n'
        return text
    elif file_path.endswith(".docx"):
        doc=docx.Document(file_path)
        texts=[]
        for para in doc.paragraphs:
            texts.append(para.text)
        text='\n'.join(texts)
        return text
    else:
        return "Unsupported File Format"