import os
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
import tempfile


def get_all_documents_already_transformed():
    output_dir = "transformed_documents"
    return os.listdir(output_dir)


def convert_all_file_from_folder():
    input_dir = "documents_to_transform"
    output_dir = "transformed_documents"
    os.makedirs(output_dir, exist_ok=True)

    already_transformed = get_all_documents_already_transformed()

    if not os.path.isdir(input_dir):
        print("There is an issue: the directory does not exist")
        return

    all_documents = os.listdir(input_dir)

    for document in all_documents:
        if document in already_transformed:
            print(f"Le document {document} a déjà été transformé.")

        else:
            document_path = os.path.join(input_dir, document)
            print(f"Processing {document_path}...")

            # Convert each page to image
            images = convert_from_path(document_path, dpi=300)

            # Create temp OCRed PDFs
            temp_pdf_files = []
            for i, image in enumerate(images):
                print(f"prise en charge de la page {i}")
                pdf_bytes = pytesseract.image_to_pdf_or_hocr(
                    image, extension="pdf", lang="deu"
                )
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_file.write(pdf_bytes)
                temp_file.close()
                temp_pdf_files.append(temp_file.name)

            # Merge all OCRed PDF pages
            merger = PdfMerger()
            for temp_pdf in temp_pdf_files:
                merger.append(temp_pdf)

            output_path = os.path.join(
                output_dir, f"{os.path.splitext(document)[0]}_ocr.pdf"
            )
            merger.write(output_path)
            merger.close()

            # Clean temp files
            for temp_pdf in temp_pdf_files:
                os.remove(temp_pdf)

            write_document_transformed(document)
            print(f"Document saved at: {output_path}")
