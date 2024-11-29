from services.pdf_service import encode_pdf_to_base64, decode_base64_to_pdf
from services.db_service import insert_document, find_document

def save_report_to_db(pdf_path, metadata):
    """Codifica um PDF e salva no banco de dados."""
    base64_pdf = encode_pdf_to_base64(pdf_path)
    document = {
        "id_relatorio": metadata["id_relatorio"],
        "tipo_relatorio": metadata["tipo_relatorio"],
        "descricao": metadata["descricao"],
        "data_geracao": metadata["data_geracao"],
        "periodo": metadata["periodo"],
        "arquivo": {
            "nome": metadata["arquivo_nome"],
            "conteudo": base64_pdf
        },
        "metadados": metadata["metadados"]
    }
    return insert_document(document)

def retrieve_report_from_db(id_relatorio, output_path):
    """Busca um relatório no banco de dados e salva como PDF."""
    query = {"id_relatorio": id_relatorio}
    document = find_document(query)
    if not document:
        return None

    # Decodificar e salvar o PDF
    decode_base64_to_pdf(document["arquivo"]["conteudo"], output_path)
    return document