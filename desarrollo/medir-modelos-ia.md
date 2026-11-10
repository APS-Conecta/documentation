---
tipo: guia
audiencia: desarrollo
apps: []
resumen: "Medir los modelos candidatos de la IA local con las preguntas fijas de gestion-aio, en un equipo con o sin GPU, y entregar sus archivos de resultados."
---
# Medir los modelos de la IA local

## Objetivo

Antes de que la suite adopte un modelo para la IA local, el comando de medición de [gestion-aio](https://github.com/APS-Conecta/gestion-aio) prueba cada candidato, `gemma4:e2b` y `qwen3.5:2b`, en su digest fijado. Le hace 32 preguntas fijas en español sobre las herramientas del primer tramo: las operaciones de Estadística y las del conector MCP. Ninguna herramienta se ejecuta, tampoco las escrituras: cada respuesta se califica por la herramienta que el modelo llama, por sus argumentos y por el tiempo que tarda.

El umbral es de al menos 95 % de llamadas correctas, con un p95 de respuesta de 15 s o menos, en el equipo de 6 GB de VRAM. Cada equipo de referencia entrega un archivo de resultados por modelo.

## Requisitos

- Linux, o WSL en Windows, con Docker, Git y Python 3.10 o posterior.
- Unos 10 GB libres en disco para la imagen de Ollama y los dos modelos.
- En un equipo con GPU: una GPU NVIDIA con su controlador y el NVIDIA Container Toolkit, de modo que `nvidia-smi` responda, o una GPU AMD o Intel con `/dev/dri` presente en el equipo.

## Pasos

1. Obtener el repositorio:

   ```bash
   git clone https://github.com/APS-Conecta/gestion-aio
   cd gestion-aio
   ```

2. Iniciar Ollama en la imagen fijada. En un equipo con GPU NVIDIA:

   ```bash
   docker run -d --name ollama-medicion --gpus=all -p 127.0.0.1:11434:11434 \
     -v ollama-medicion:/root/.ollama -e OLLAMA_CONTEXT_LENGTH=16384 -e OLLAMA_NUM_PARALLEL=1 \
     ollama/ollama:0.40.16@sha256:910d0d8107b538fb0894e63163eb195de0cc7aefcbc666dc62d3b18f71124592
   ```

   En un equipo con GPU AMD o Intel, el mismo comando con `--device /dev/dri` en lugar de `--gpus=all`, como lo hace la suite. En un equipo sin GPU, el mismo comando sin `--gpus=all`.

3. Ejecutar la medición:

   ```bash
   python3 aps/benchmark/benchmark.py
   ```

   La primera vez descarga ambos modelos, unos 7 GB. Cada pregunta imprime una línea con su resultado y su tiempo. Con GPU, cada modelo tarda minutos; solo con CPU, del orden de una hora.

4. Entregar los resultados. El comando deja en la carpeta actual un archivo por modelo, `benchmark-<modelo>-<equipo>.json`. Adjuntarlos a la incidencia [APS-Conecta/gestion-aio#91](https://github.com/APS-Conecta/gestion-aio/issues/91), junto con cualquier error tal como se imprimió.

5. Retirar Ollama:

   ```bash
   docker rm -f ollama-medicion
   docker volume rm ollama-medicion
   ```

## Verificación

- La última línea de cada modelo dice su tasa de llamadas correctas, su p50 y su p95, y si pasa el umbral.
- En cada archivo, `digest` es el digest fijado del modelo y `hardware` nombra la GPU y su VRAM; sin GPU, la lista `gpus` queda vacía.
- Con GPU, `model_bytes_in_vram` es igual a `model_bytes` cuando el modelo cupo entero en la VRAM.

## Problemas frecuentes

| Mensaje o síntoma | Qué hacer |
|---|---|
| «Ollama holds digest …, not the pin …; not measured» | El registro de Ollama movió la etiqueta del modelo y ya no entrega el digest fijado. Informarlo en la incidencia: no se mide otro digest. |
| «Connection refused» | Ollama no está iniciado: repetir el paso 2. |
| `model_bytes_in_vram` en 0 con GPU | Docker no ve la GPU. Con NVIDIA: revisar el NVIDIA Container Toolkit y que el contenedor se inició con `--gpus=all`. Con AMD o Intel: revisar que el contenedor se inició con `--device /dev/dri`. |
