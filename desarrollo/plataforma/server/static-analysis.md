---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Análisis estático del código PHP del servidor con psalm y las extensiones de PHP que deben estar instaladas y habilitadas para ejecutarlo."
---
# Análisis estático

## Resumen

Esta página indica qué herramienta se usa para el análisis estático del código PHP del repositorio del servidor, psalm, y qué extensiones de PHP deben estar instaladas y habilitadas para que funcione. Está dirigida a quienes desarrollan el servidor.

````{upstream} developer_manual/server/static-analysis.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Análisis estático de PHP

En el repositorio del servidor se usa psalm para el análisis estático del código PHP.

(nc-dev-psalm-php-extensions)=
#### Extensiones de PHP necesarias

Para que psalm funcione, las siguientes extensiones de PHP deben estar instaladas y habilitadas:

- apcu
- curl
- ftp
- gd
- iconv
- imagick
- json
- ldap
- libxml
- mbstring
- openssl
- pdo
- simplexml
- sysvsem
- xmlreader
- zip

Algunas son para funciones opcionales, pero aun así son necesarias para validar el código.
````
