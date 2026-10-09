---
tipo: referencia
esqueleto: borrador
audiencia: administracion
apps: [gestion]
resumen: "El motor de aprovisionamiento: fases numeradas e idempotentes que escriben el estado deseado de la instalación."
---
# Aprovisionamiento

## Resumen

El motor de aprovisionamiento es el único escritor del estado deseado de la instalación: fases numeradas que se ejecutan en orden fijo, idempotentes por guardia — consultan el estado antes de escribir — y de convergencia aditiva: nunca eliminan documentos, carpetas de grupo ni cuentas. La estructura (seguridad, tareas, idioma, apps, oficina, marca, grupos, carpetas y ACL) precede a las cuentas y a los datos de prueba.

## Secciones previstas

- Filosofía y guardias de idempotencia
- Referencia por fase
- Límite entre estructura y fixtures
