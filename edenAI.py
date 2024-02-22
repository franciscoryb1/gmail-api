import json
import requests

def categorizarEDEN(prompt):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzJkZTIyMjUtMmU4Zi00M2RlLTgxZTQtOGVhOTMyZjFhOTAzIiwidHlwZSI6ImFwaV90b2tlbiJ9.08apr4KdYl3PUuCA-M_A40_cwPlb7PP2oB3iCrpQbMA"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": prompt,
        "chatbot_global_action": "te voy a enviar el contenido de un correo electronico y lo tenes que categorizar en una de las siguientes categorias queja/reclamo, solicitud de información, o agradecimiento/conformidad, devolviendo unicamente la categoria correspondiente",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']

def responderEDEN(prompt):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzJkZTIyMjUtMmU4Zi00M2RlLTgxZTQtOGVhOTMyZjFhOTAzIiwidHlwZSI6ImFwaV90b2tlbiJ9.08apr4KdYl3PUuCA-M_A40_cwPlb7PP2oB3iCrpQbMA"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": prompt,
        "chatbot_global_action": "te voy a enviar el contenido de un correo electronico y lo tenes que generar una respuesta acorde breve y concisa",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']

def EDEN(prompt):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzJkZTIyMjUtMmU4Zi00M2RlLTgxZTQtOGVhOTMyZjFhOTAzIiwidHlwZSI6ImFwaV90b2tlbiJ9.08apr4KdYl3PUuCA-M_A40_cwPlb7PP2oB3iCrpQbMA"}
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": prompt,
        "chatbot_global_action": "te voy a enviar el contenido de un correo electronico y lo tenes que categorizar en una de las siguientes categorias queja/reclamo, consultas/solicitud de información, o agradecimiento/conformidad, devolviendo UNICAMENTE la categoria correspondiente. Luego tenes que generar una respuesta acorde breve y concisa. SEPARAR LAS RESPUESTAS POR ESTA LINEA DE CARACTERES ';;;;'",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']
