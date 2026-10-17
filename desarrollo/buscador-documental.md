---
tipo: referencia
esqueleto: borrador
audiencia: desarrollo
apps: [buscador-documental]
resumen: "Buscador Documental: estado del diseño y decisiones de las etapas de mediciones (S0) y de esqueleto con comprobación de permisos (S1)."
---
# Buscador Documental

## Resumen

Buscador Documental busca por palabras y por significado, incluidos escaneos y fotografías, respetando los permisos de Nextcloud. Está en diseño: PostgreSQL con pgvector guarda el estado, el texto y los vectores, y un proceso de trabajo externo hace la lectura y el reconocimiento de texto. Las etapas S0 (mediciones) y S1 (esqueleto de punta a punta) están terminadas: un PDF escaneado recorre la aplicación, el proceso de trabajo con firma HMAC y el reconocimiento de texto hasta el índice, y cada resultado se vuelve a comprobar contra los permisos de Nextcloud en el momento de la consulta; una prueba de permisos de 20 comprobaciones corre en la integración continua. La comprobación de 50 resultados no cumple los 300 ms previstos (377 ms en el percentil 95) y la ADR-0010 acepta esa excepción. Las decisiones y las mediciones están en el repositorio de la aplicación, en `buscador/`.

## Secciones previstas

- Propósito y diseño
- Decisiones de las etapas
- Contrato del proceso de trabajo
- Pruebas
- Limitaciones
