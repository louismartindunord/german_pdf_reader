import fitz
import pytesseract
from pdf2image import convert_from_path


pdf_path = "mon_fichier_scanné.pdf"
output_pdf_path = "pdf_reconnu_avec_texte.pdf"

images = convert_from_path(pdf_path, dpi=300)

# Créer un nouveau PDF vide
doc = fitz.open()

for i, image in enumerate(images):
    text = pytesseract.image_to_pdf_or_hocr(
        image, extension="pdf", lang="deu"
    )  # remplace 'deu' par 'fra' pour le français
    ocr_page = fitz.open("pdf", text)

    doc.insert_pdf(ocr_page)

doc.save(output_pdf_path)
doc.close()

print(f"document save in : {output_pdf_path}")
