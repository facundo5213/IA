def construir_json_respuesta(datos_cheque, resultado_bcra):
    return {
        "numero_cheque": datos_cheque.get("numero"),
        "cuit": datos_cheque.get("cuit"),
        "beneficiario": datos_cheque.get("beneficiario"),
        "monto": datos_cheque.get("monto"),
        "fecha": datos_cheque.get("fecha"),
        "entidad_bancaria": datos_cheque.get("entidad_bancaria"),
        "denunciado_bcra": resultado_bcra.get("denunciado", False),
        "estado": "rechazado" if resultado_bcra.get("denunciado") else "válido para procesar"
    }
