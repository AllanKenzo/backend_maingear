import base64

def encode_pdf_to_base64(pdf_path):
    """Codifica um arquivo PDF em Base64."""
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

def decode_base64_to_pdf(base64_content, output_path):
    """Decodifica uma string Base64 para um arquivo PDF."""
    with open(output_path, "wb") as pdf_file:
        pdf_file.write(base64.b64decode(base64_content))