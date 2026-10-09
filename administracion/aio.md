---
tipo: explicacion
esqueleto: borrador
audiencia: administracion
apps: [AIO]
resumen: "El instalador all-in-one adaptado por APS Conecta: una cola de parches sobre el instalador oficial."
---
# AIO

## Resumen

La suite se distribuye como un fork del instalador all-in-one de Nextcloud, adaptado por APS Conecta: una cola de parches numerados transforma el instalador upstream en la instalación del establecimiento. Los parches fijan las decisiones de la suite — la elección del servidor de oficina, las aplicaciones de partida — y el repositorio del fork documenta cada cambio.

### En APS Conecta Gestión

La instalación de la suite difiere de la de {vendor}`Nextcloud` que describen las páginas de instalación. Los [parches](https://github.com/APS-Conecta/AIO/tree/main/patches) dejan el asistente en español de Chile y con el nombre del producto, dejan Euro-Office como única suite de oficina, apagan la tienda de aplicaciones, los contenedores comunitarios y la autoactualización, y agregan los valores por defecto de APS, la página posterior al arranque, el certificado del instalador y la ruta de teselas del mapa. Tras el asistente, las fases de provisión de gestion configuran el establecimiento completo: carpetas, roles, permisos, oficina, tema, intranet y aplicaciones del sector. El recorrido completo está en el [manual del instalador](https://github.com/APS-Conecta/gestion/blob/main/docs/INSTALLER.md).

## Secciones previstas

- El fork del instalador
- La cola de parches
- El asistente de instalación
- Configuración del asistente
