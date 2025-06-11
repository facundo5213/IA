import os
import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

def extraer_datos_cheque(ruta_pdf):
    url = f"{ENDPOINT}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2023-07-31"
    headers = {
        "Content-Type": "application/pdf",
        "Ocp-Apim-Subscription-Key": KEY
    }

    with open(ruta_pdf, "rb") as f:
        response = requests.post(url, headers=headers, data=f)

    response.raise_for_status()
    result_url = response.headers["operation-location"]

    import time
    for _ in range(10):
        time.sleep(2)
        res = requests.get(result_url, headers={"Ocp-Apim-Subscription-Key": KEY})
        result = res.json()
        if result["status"] == "succeeded":
            break

    campos = {}
    for campo in result["analyzeResult"]["documents"][0]["fields"]:
        valor = result["analyzeResult"]["documents"][0]["fields"][campo].get("content", "")
        campos[campo] = valor

    return campos
