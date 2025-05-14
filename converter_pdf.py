import PyPDF2
import os
import re

def pdf_to_txt_multicolumn(pdf_path, txt_path):
    """
    Converts the text content of a PDF file with multiple columns to a TXT file,
    attempting to separate lines from different columns.
    Handles the "P" field and ignores lines starting with "82-0...82-9".

    Args:
        pdf_path (str): The path to the input PDF file.
        txt_path (str): The path to the output TXT file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        lines = text.strip().split('\n')
        processed_lines = []
        current_block = []

        for line in lines:
            cleaned_line = line.strip()
            if cleaned_line and not cleaned_line.startswith("Folha:") and not re.match(r"^82-[0-9]", cleaned_line):
                if current_block and not check_column_break(current_block[-1], cleaned_line):
                    processed_lines.append(" ".join(current_block))
                    current_block = [cleaned_line]
                else:
                    current_block.append(cleaned_line)

        if current_block:
            processed_lines.append(" ".join(current_block))

        final_processed_lines = []
        for line in processed_lines:
            if line.startswith("P"):
                final_processed_lines.append(line[1:].strip() + "  P")
            else:
                final_processed_lines.append(line + " ")

        text_to_write = "\n".join(final_processed_lines)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_to_write)

        print(f"Successfully converted '{pdf_path}' to '{txt_path}'")

    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_column_break(prev_line, current_line, spacing_threshold=50):
    """
    Attempts to detect a column break between two consecutive lines based on spacing.
    This is a heuristic approach and might not work for all layouts.
    """
    prev_words = prev_line.split()
    current_words = current_line.split()

    if not prev_words or not current_words:
        return False

    last_word_prev_end = 0
    for match in re.finditer(re.escape(prev_words[-1]), prev_line):
        last_word_prev_end = match.end()

    first_word_current_start = -1
    for match in re.finditer(re.escape(current_words[0]), current_line):
        first_word_current_start = match.start()
        break

    if last_word_prev_end > 0 and first_word_current_start > last_word_prev_end + spacing_threshold:
        return True
    return False

def process_pdf_folder_multicolumn(pdf_folder, txt_folder):
    """
    Processes all PDF files in the specified folder and saves the TXT files
    in the output folder, attempting to handle multiple columns.

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
            pdf_to_txt_multicolumn(pdf_filepath, txt_filepath)

# Specify the input and output folders
pdf_input_folder = r'C:\ConvertePDF\PDF'
txt_output_folder = r'C:\ConvertePDF\TXT'

# Process the PDF files
process_pdf_folder_multicolumn(pdf_input_folder, txt_output_folder)