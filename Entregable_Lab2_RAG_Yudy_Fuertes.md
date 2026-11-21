# Informe de Laboratorio 2: Pipeline RAG con Open WebUI y Ollama

- **Estudiante / Equipo:** Yudy Fuertes
- **Stack Utilizado:** qwen2.5:1.5b-instruct + nomic-embed-text + Open WebUI + Docker Compose
- **Fecha:** 21/11/2026

---

## 1. Comparativa: Antes del RAG (Línea Base)
Sin acceso a la base de conocimiento, qwen2.5:1.5b-instruct no pudo responder con los datos exactos de la guía de recetas colombianas. Ante la pregunta por las calorías y proteínas de la receta número 47 (Bowl de quinua con pollo y vegetales), respondió con un rango aproximado de “450 a 550 calorías” y “35 a 45 gramos de proteína”, “dependiendo de las cantidades exactas utilizadas”, cuando el valor real de la guía es 470 kcal y 40 g de proteína (además de 50 g de carbohidratos y 12 g de grasas). También describió ingredientes genéricos (quinua, pechuga de pollo, tomate, pepino, zanahoria, aguacate o aceite de oliva) sin las cantidades de la receta (quinua 130 g, pollo 130 g, zanahoria 40 g, pepino 40 g, tomate cherry 40 g, aguacate 30 g, limón) y terminó recomendando revisar el documento donde aparece la receta. En conjunto, el modelo respondió con estimaciones plausibles pero imprecisas, en lugar de entregar el dato exacto de la guía, que es el que importa en un plan nutricional.

## 2. Comparativa: Después del RAG (Con Knowledge Base)
Tras indexar `rutinas.md` y `recetas.md` en la colección Fitness-Colombiano (embeddings con nomic-embed-text vía Ollama) y conectarla al modelo `modelo-fitness-colombiano`, las respuestas pasaron de estimaciones genéricas a datos fieles a los documentos. Para el desayuno de ganancia muscular, el modelo recomendó el Bowl de avena proteico (receta 1) con 10 min de preparación, 440 kcal, 28 g de proteínas, 62 g de carbohidratos y 9 g de grasas, valores idénticos a los de `recetas.md`. Ante la pregunta por la receta de claras, indicó que la guía incluye 100 recetas y que la Tortilla de claras con espinaca y champiñón (receta 6, pérdida de grasa) lleva 4 claras de huevo (130 g), espinaca 50 g, champiñones 60 g, tomate 50 g y aceite de oliva 5 g, con 150 kcal y 17 g de proteínas. En rutinas, para 4 días por semana recomendó la estructura tren superior / tren inferior con el orden Superior A, Inferior A, descanso, Superior B e Inferior B, y para el nivel avanzado indicó periodizar en bloques de 4 a 6 semanas con una semana de descarga que reduce el 40 % del volumen; ambos datos coinciden con `rutinas.md`. En estas respuestas Open WebUI mostró “1 Fuente”, el fragmento recuperado de la colección, lo que permite verificar de dónde sale cada dato (trazabilidad). Las respuestas se apoyaron en el contexto recuperado y no en el conocimiento general del modelo.

## 3. Evaluación de Control de Alucinaciones (Fuera de Dominio)
Ante la pregunta sobre el horario de la cafetería los sábados en Innovatech, un dato que no existe en los documentos, el modelo no inventó ningún horario, que era el riesgo principal. Respondió que no podía proporcionar esa información porque su base de conocimiento está enfocada únicamente en rutinas de entrenamiento y recetas colombianas balanceadas, y recomendó consultar directamente con la empresa. Lo mismo ocurrió con la pregunta sobre el auxilio de conectividad para teletrabajo en 2027: indicó que no tenía información sobre políticas empresariales y sugirió acudir a Talento Humano o a los comunicados internos. El comportamiento fue correcto y, a diferencia de una simple negativa, delimitó su alcance al contenido de la colección. Open WebUI mostró “1 Fuente” en la consulta de la cafetería, porque la búsqueda vectorial siempre devuelve el fragmento más cercano aunque no sea relevante. Esto muestra que el RAG reduce la alucinación pero no la elimina por sí solo; el prompt de sistema, la temperatura baja (0.2) y el tamaño del modelo influyen en que sepa decir que la información no está en el documento.

---

## 4. Evidencias Adjuntas (Capturas de Pantalla)
- [x] Captura 1: Respuesta del modelo base sin RAG, receta 47 con rango aproximado .
- [x] Captura 2: Despliegue con `docker compose up -d`, descarga de `qwen2.5:1.5b-instruct` y `nomic-embed-text`, y contenedores en Docker Desktop.
- [x] Captura 3: Respuestas fundamentadas con “1 Fuente” usando la colección Fitness-Colombiano: avena proteica, tortilla de claras, 4 días por semana y descarga en nivel avanzado.
