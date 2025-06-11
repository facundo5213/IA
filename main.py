import os
import sys
import json
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Carga variables de entorno
load_dotenv()
ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
KEY      = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
MODEL_ID = os.getenv("AZURE_CUSTOM_MODEL_ID")

if not all([ENDPOINT, KEY, MODEL_ID]):
    print("❌ Completá tu .env con ENDPOINT, KEY y MODEL_ID")
    sys.exit(1)

client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(KEY))

def extraer_cuit(ruta_pdf: str) -> str:
    """Envía el PDF a Azure, espera el resultado y devuelve el campo 'cuit'."""
    # Lanza la petición de análisis
    with open(ruta_pdf, "rb") as f:
        poller = client.begin_analyze_document(MODEL_ID, document=f)
    result = poller.result()

    # Documentos analizados (debería ser uno)
    if not result.documents:
        raise RuntimeError("No se detectó ningún documento en el PDF.")
    doc = result.documents[0]

    # Extrae el campo 'cuit'
    campo = doc.fields.get("cuit")
    if not campo or not campo.value:
        raise RuntimeError("El campo 'cuit' no fue detectado.")
    return campo.value

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_pdf_de_cheque>")
        sys.exit(1)

    ruta = sys.argv[1]
    try:
        cuit = extraer_cuit(ruta)
        # Devolver como JSON
        salida = {"cuit": cuit}
        print(json.dumps(salida, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
