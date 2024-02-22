from langchain_community.llms import Ollama

llm = Ollama(model="mistral")


prompt = """
Te voy a pasar el siguiente correo electrónico para que lo contestes de forma cordial y profesional teniendo en cuenta las siguientes reglas:"

- Si el correo habla de la devolución del cobro o pago de la membresia, contestar que tiene que seguir las instrucciones de esta página: https://instrucciones.com
- Si el correo habla de tener una entrevita con matias y le ofrecen pagar honorarios y viajes, contestar diciedo que tiene que escribir a este correo: a@gmail.com
"""

correo = """
    # Aquí comienza el correo:
    Hola Ale: 
    Te escribo porque nuevamente me volvieron a debitar la membresia del curso Recordis. 
    Les pido que me devuelvan el dinero
"""

datos = prompt + correo

r = llm.invoke(datos)

print(r)