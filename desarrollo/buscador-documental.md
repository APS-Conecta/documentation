---
tipo: referencia
esqueleto: borrador
audiencia: desarrollo
apps: [buscador-documental]
resumen: "Buscador Documental: estado del diseño y decisiones de la etapa de mediciones."
---
# Buscador Documental

## Resumen

Buscador Documental busca por palabras y por significado, incluidos escaneos y fotografías, respetando los permisos de Nextcloud. Está en diseño: PostgreSQL con pgvector guarda el estado, el texto y los vectores, y un proceso de trabajo externo hace la lectura y el reconocimiento de texto. Las decisiones y las mediciones de la etapa S0 están en el repositorio de la aplicación, en `buscador/`.

## Secciones previstas

- Propósito y diseño
- Decisiones de las etapas
- Contrato del proceso de trabajo
- Pruebas
- Limitaciones
