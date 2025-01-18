from pypdf import PdfReader
import pdfplumber
from PIL import Image
from io import BytesIO
from Images import Image as Image_Class

class PDF:
    def __init__(self):
        self.Image_class = Image_Class()
    def ordinal(n):
        if 11 <= n % 100 <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    def process_pdf(self,path):
        reader = PdfReader(path)
        text = ''
        for page_num, page in enumerate(reader.pages):
            text += page.extract_text()
            
            # Open the PDF with PyMuPDF
            pdf_document = fitz.open(path)
            pdf_page = pdf_document.load_page(page_num)
            
            # Extract images from the page
            image_list = pdf_page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                text += f'Details about {self.ordinal(img_index+1)} image present in the page {self.Image_class.process_image_bytes(image_bytes)} \n'
        
        return text

# Example usage
# pdf_path = r'D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder\Metal Matrix\A novel look at the metal matrix used in diamond impregnated tools for cutting stones.pdf'
# extracted_text = PDF.process_pdf(pdf_path)
# print(extracted_text)