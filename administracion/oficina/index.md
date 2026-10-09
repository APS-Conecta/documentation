---
tipo: guia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "Operar el servidor de documentos Euro-Office de la pila: tokens, almacenamiento y salud."
---
# Oficina

## Resumen

El servidor de documentos Euro-Office es un contenedor dedicado de la pila: valida tokens JWT, responde al almacenamiento por ruta interna y se mantiene en espera bajo demanda para ahorrar recursos. La administración cubre el secreto compartido, el enrutamiento de retorno, la conversión ODF con pérdida y la verificación del backend de oficina.

## Secciones previstas

- Arquitectura del servidor de documentos
- Secreto JWT
- Enrutamiento interno
- Compatibilidad de formatos
- Espera bajo demanda
- Verificación del backend

```{toctree}
:maxdepth: 1
:glob:

*
```
