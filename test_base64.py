import base64

# Abra o arquivo PDF em modo binário
with open("C:/Users/Sergio/Downloads/relatorio_teste.pdf", "rb") as pdf_file:
    # Codifique o conteúdo em base64
    encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

print(encoded_pdf)