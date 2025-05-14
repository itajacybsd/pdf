import PyPDF2
import os

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
                    processed_lines.append(cleaned_line[1:].strip() + "  P")
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

def process_pdf_folder(pdf_folder, txt_folder):
    """
    Processes all PDF files in the specified folder and saves the TXT files
    in the output folder.

    Args:
        pdf_folder (str): The path to the folder containing PDF files.
        txt_folder (str): The path to the folder where TXT files will be saved.
    """
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_filepath = os.path.join(pdf_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_filepath = os.path.join(txt_folder, txt_filename)
            pdf_to_txt(pdf_filepath, txt_filepath)

# Specify the input and output folders
pdf_input_folder = r'C:\ConvertePDF\PDF'
txt_output_folder = r'C:\ConvertePDF\TXT'

# Process the PDF files
process_pdf_folder(pdf_input_folder, txt_output_folder)


# Criar as pastas para alocação dos arquivos
# C:\ConvertePDF\PDF
# C:\ConvertePDF\TXT
#