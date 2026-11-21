import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI



BASE_URL = os.getenv("OPENWEBUI_BASE_URL", "http://localhost:3000/api")
API_KEY = os.getenv("OPENWEBUI_API_KEY", "")
TARGET_MODEL = os.getenv("MODEL_ID", "modelo-fitness-colombiano")


def ejecutar_consulta_rag(mensaje: str, temperatura: float = 0.2) -> None:
    """Envía un prompt al modelo personalizado con Knowledge Base en Open WebUI."""
    if not API_KEY:
        print("[ERROR] Variable OPENWEBUI_API_KEY no definida en el archivo .env.")
        return

    cliente = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    print(f"Conectando al endpoint: {BASE_URL}")
    print(f"Modelo activo: {TARGET_MODEL}\n")

    try:
        completado = cliente.chat.completions.create(
            model=TARGET_MODEL,
            messages=[{"role": "user", "content": mensaje}],
            temperature=temperatura,
        )
        print("=== RESPUESTA DEL ASISTENTE RAG ===")
        print(completado.choices[0].message.content)
    except Exception as error:
        print(f"[FALLO DE CONEXIÓN]: {error}")


if __name__ == "__main__":
    consulta_prueba = (
        "Hola, preséntate brevemente y dime qué tipo de asistencia puedes brindarme."
    )
    ejecutar_consulta_rag(consulta_prueba)
