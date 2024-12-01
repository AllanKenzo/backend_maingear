import base64
import io

def encode_pdf_to_base64(pdf_path):
    """Codifica um arquivo PDF em Base64."""
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

def decode_base64_to_pdf(base64_string):
    pdf_data = base64.b64decode(base64_string)
    return io.BytesIO(pdf_data)
        
