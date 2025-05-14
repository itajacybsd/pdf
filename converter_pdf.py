import PyPDF2
import re

def pdf_to_txt(pdf_path, txt_path):
    """
    Converts the text content of a PDF file to a TXT file, handling the "P" field.

    Args:
        pdf_path (str): The path to the input PDF file.
        txt_path (str): The path to the output TXT file.
    """

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Use "" to avoid NoneType errors

        lines = text.strip().split('\n')

        processed_lines = []
        for line in lines:
            cleaned_line = line.strip()
            if cleaned_line and not cleaned_line.startswith("Folha:"):  # Ignore empty lines and "Folha:" lines
                if cleaned_line.startswith("P"):
                    processed_lines.append(cleaned_line[1:].strip() + " P")
                else:
                    processed_lines.append(cleaned_line)

        text_to_write = ""
        for line in processed_lines:
            text_to_write += line + '\n'

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_to_write)

        print(f"Successfully converted '{pdf_path}' to '{txt_path}'")

    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
pdf_file_path = r'd:\lixo\cesar\teste.pdf'
txt_file_path = r'd:\lixo\cesar\teste.txt'
pdf_to_txt(pdf_file_path, txt_file_path)