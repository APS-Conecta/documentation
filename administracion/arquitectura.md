---
tipo: explicacion
---
# Arquitectura

La instalación es una topología multicontenedor de cinco servicios sobre una red interna: el servidor de aplicaciones, la base de datos PostgreSQL, la caché Redis, el planificador de tareas de fondo y el servidor de documentos. Los puertos se publican ligados a la interfaz local — aislamiento loopback — y los volúmenes persistentes custodian los datos, las aplicaciones y el tema.

- Secciones previstas: topología de servicios, inventario de servicios e imágenes, red interna, aislamiento loopback, dimensionamiento
