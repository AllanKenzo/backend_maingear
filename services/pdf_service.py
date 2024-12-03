import base64

def encode_pdf_to_base64(pdf_path):
    """Codifica um arquivo PDF em Base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode("utf-8")
            return encoded_string
    except Exception as e:
        print(f"Erro ao codificar o PDF: {e}")
        raise

def decode_base64_to_pdf(base64_string):
    """Decodes a base64 string to binary PDF data."""
    try:
        pdf_data = base64.b64decode(base64_string)
        return pdf_data
    except Exception as e:
        print(f"Erro ao decodificar o PDF: {e}")
        raise
        
