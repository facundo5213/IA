import requests
import os
from dotenv import load_dotenv

load_dotenv()

def verificar_cheque_bcra(numero_cheque, codigo_entidad):
    url = os.getenv("BCRA_API_URL")
    params = {
        "cod_entidad": codigo_entidad,
        "numero": numero_cheque
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        return data
    return {"denunciado": "Error al consultar"}
