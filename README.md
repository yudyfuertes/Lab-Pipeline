# Pipeline RAG Documental con Open WebUI y Ollama

Implementación de un sistema de Generación Aumentada por Recuperación (**RAG**) desplegado con Docker, usando **Ollama** como motor de inferencia local y de embeddings, y **Open WebUI** para gestionar la Knowledge Base y exponer una API compatible con OpenAI.

El asistente (`modelo-fitness-colombiano`) responde con base en dos documentos: `rutinas.md` (rutinas de entrenamiento por nivel) y `recetas.md` (100 recetas colombianas balanceadas).

---

## Arquitectura del entorno

| Servicio | Imagen Docker | Puerto local | Función |
| :--- | :--- | :---: | :--- |
| **Ollama** | `ollama/ollama:latest` | `11434` | Ejecuta el LLM (`qwen2.5:1.5b-instruct`) y genera embeddings (`nomic-embed-text`). |
| **Open WebUI** | `ghcr.io/open-webui/open-webui:v0.5.20` | `3000` | Interfaz web, indexación vectorial en la Knowledge Base y API REST. |

## Estructura del proyecto

```
.
├── docker-compose.yml
├── cliente_rag_api.py
├── requirements.txt
├── .env.example
├── .gitignore
├── rutinas.md
├── recetas.md
└── README.md
```

---

## Guía de despliegue

### 1. Levantar los servicios
```bash
docker compose up -d
docker ps
```
Verifica que `ollama-rag-service` y `open-webui-pipeline` estén en estado `Up`.

### 2. Descargar los modelos en Ollama
```bash
docker exec -it ollama-rag-service ollama pull qwen2.5:1.5b-instruct
docker exec -it ollama-rag-service ollama pull nomic-embed-text
```

### 3. Configurar Open WebUI
1. Abre http://localhost:3000 y crea el usuario administrador local.
2. **Embeddings:** `Admin Panel → Settings → Documents` → motor de embeddings **Ollama**, modelo `nomic-embed-text`.
3. **Knowledge Base:** `Workspace → Knowledge → +` → crea una colección y sube `rutinas.md` y `recetas.md`. Visibilidad **Public**.
4. **Modelo personalizado:** `Workspace → Models → +`
   - ID / nombre: `modelo-fitness-colombiano`
   - Modelo base: `qwen2.5:1.5b-instruct`
   - Knowledge: la colección creada en el paso anterior
   - Visibilidad: **Public**
5. **API Key:** `Settings → Account → API Keys` → genera una clave.

### 4. Configurar el cliente Python
```bash
copy .env.example .env      
```
Edita `.env` y pega tu API key en `OPENWEBUI_API_KEY`. **Nunca subas `.env` a Git** (ya está en `.gitignore`).

```bash
python -m venv .venv
.venv\Scripts\activate     
pip install -r requirements.txt
python cliente_rag_api.py
```

Si todo está bien, verás `=== RESPUESTA DEL ASISTENTE RAG ===` seguido de la respuesta del modelo.

---

## Solución de problemas

**El script dice que falta `OPENWEBUI_API_KEY`:** el `.env` debe estar en la misma carpeta que `cliente_rag_api.py`.

**Error 404 / modelo no encontrado:** el `MODEL_ID` del `.env` debe ser idéntico al ID del modelo creado en Open WebUI, y tanto el modelo como la Knowledge Base deben tener visibilidad **Public**.

**El RAG no recupera contexto:** confirma que los archivos aparecen como indexados en la Knowledge Base y que el motor de embeddings es Ollama con `nomic-embed-text`.

**Open WebUI en bucle de reinicio (`Restarting`):**
```bash
docker rm -f open-webui-pipeline
docker rmi ghcr.io/open-webui/open-webui:main
docker compose pull open-webui-app
docker compose up -d
docker logs -f open-webui-pipeline
```
Espera a que `docker ps` muestre `Up` y en los logs aparezca el arranque de Uvicorn.

**Alternativa sin la imagen Docker de Open WebUI:**
```bash
docker rm -f open-webui-pipeline
python -m venv .venv-webui
.venv-webui\Scripts\activate      
pip install open-webui
set OLLAMA_BASE_URL=http://localhost:11434   
open-webui serve --port 3000
```

---

## Seguridad
- Las API keys van solo en `.env`; nunca en el código ni en `.env.example`.
- Si una clave se expuso en Git, revócala en Open WebUI y genera otra.
