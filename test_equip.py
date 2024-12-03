from services.pdf_service import encode_pdf_to_base64

pdf_path = "C:/Users/Sergio/Desktop/allan/PII/backend/backend_maingear/temp/relatorio_1.pdf"
try:
    encoded_pdf = encode_pdf_to_base64(pdf_path)
    print(f"Encoded PDF: {encoded_pdf}")
except Exception as e:
    print(f"Erro ao codificar o PDF: {e}")