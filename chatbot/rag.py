import re
import httpx
from django.conf import settings


def generar_respuesta_llamacpp(prompt: str, pregunta: str, n_predict: int = 384, temperatura: float = 0.8):
    url = f"{settings.LLAMACPP_API}v1/chat/completions"
    payload = {
        "model": "ACADEMOS xd",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": n_predict,
        "temperature": temperatura,
        "stream": False,
        "stop": ["Usuario:", "Pregunta:"],
    }
    with httpx.Client(timeout=900) as client:
        print("haciendo peticion a: ", url)
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content']

def limpiar_respuesta(respuesta: str):
    texto = re.sub(r"```+", "", respuesta)
    # Quita espacios al inicio y fin de línea
    texto = texto.strip()

    if texto.startswith("=== RESPUESTA ===\n"):
        texto = texto.replace("=== RESPUESTA ===\n", "")
    if texto.startswith("===\nRespuesta ===\n"):
        texto = texto.replace("===\nRespuesta ===\n", "")
    if texto.startswith("=== RESPUESTA\n"):
        texto = texto.replace("=== RESPUESTA\n", "")
    if texto.startswith("===\nRespuesta\nHistorial relevante:\n"):
        texto = texto.replace("===\nRespuesta\nHistorial relevante:\n", "")
    if texto.startswith("Asistente: "):
        texto = texto.replace("Asistente: ", "").strip()
    if texto.startswith("Asistente:\n"):
        texto = texto.replace("Asistente:\n", "").strip()

    return texto.replace("===\nRespuesta\nHistorial relevante:\n", "")
