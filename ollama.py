import requests
import json


def ollama(prompt):
    url = 'http://localhost:11434/api/generate'
    # Datos para enviar en la solicitud POST
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }

    # Convertir los datos a formato JSON
    payload = json.dumps(data)

    # Configurar los encabezados de la solicitud
    headers = {
        'Content-Type': 'application/json'
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=payload)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Imprimir la respuesta
        resp = response.json()
        #return resp['response']
        print(resp)
        print(resp['response'])
        ## Guardar el diccionario en el archivo JSON
        #with open('ollama.json', 'w') as json_file:
        #    json.dump(resp, json_file)

        #print(f"El diccionario se ha guardado exitosamente !")
    else:
        print("Error:", response.status_code)


ollama("por que el cielo es azul?")