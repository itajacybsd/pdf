# Data: 15/05/2025
# Autor: Itajacy Furtado
#
# Este script converte arquivos PDF em arquivos TXT,
# utilizando a biblioteca PyPDF2 para extrair texto dos PDFs.

import PyPDF2
import os
import re

def pdf_to_txt_multicolumn(pdf_path, txt_path):
    """
    Converte o conteúdo de texto de um arquivo PDF com várias colunas em um arquivo TXT,
    tentando separar linhas de colunas diferentes.
    Remove qualquer linha que inicie com "Folha:".
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
            # Remove completamente a linha se começar com "Folha:"
            if cleaned_line.startswith("Folha:"):
                continue

            # Remove o trecho da linha que começa com "Folha:" (caso esteja no meio)
            cleaned_line = re.sub(r'Folha:.*', '', cleaned_line).strip()

            if cleaned_line:
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
                final_processed_lines.append(line[1:].strip() + " P")
            else:
                final_processed_lines.append(line + " ")

        text_to_write = "\n".join(final_processed_lines)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_to_write)

        print(f"Convertido com Sucesso '{pdf_path}' para '{txt_path}'")

    except FileNotFoundError:
        print(f"Erro: arquivo PDF '{pdf_path}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def check_column_break(prev_line, current_line, spacing_threshold=50):
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
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_filepath = os.path.join(pdf_folder, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_filepath = os.path.join(txt_folder, txt_filename)
            pdf_to_txt_multicolumn(pdf_filepath, txt_filepath)

# Especifica os caminhos para as pastas de entrada e saída
pdf_input_folder = r'C:\ConvertePDF\PDF'
txt_output_folder = r'C:\ConvertePDF\TXT'

# Processa os arquivos PDF na pasta de entrada
process_pdf_folder_multicolumn(pdf_input_folder, txt_output_folder)
