---
tipo: explicacion
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "Cómo encajan las APIs externas con las interfaces de la plataforma y los contratos OCS de las aplicaciones propias, con enlaces a la documentación."
---
# Plataforma y REST interno

## Contexto

Las aplicaciones propias de la suite corren dentro de la plataforma y reciben sus datos por tres capas: las APIs de la plataforma (OCS y WebDAV), los contratos REST de cada aplicación y, cuando hace falta, una fuente externa de las que describe esta sección. Esta página solo explica cómo encajan; el detalle ya está documentado en otro lugar y aquí no se copia.

## Diseño

| Capa | Qué es | Dónde está documentada |
| --- | --- | --- |
| APIs de la plataforma | OCS para acciones y WebDAV para archivos | {doc}`/desarrollo/plataforma/client-apis/index`, {doc}`/desarrollo/plataforma/client-apis/ocs/ocs-api-overview` y {doc}`/desarrollo/plataforma/client-apis/files` |
| Contratos de las aplicaciones | Rutas OCS y REST de cada aplicación propia, con su especificación OpenAPI | {doc}`/desarrollo/territorio`, {doc}`/desarrollo/farmacia`, {doc}`/desarrollo/estadistica` y {doc}`/desarrollo/epidemiologia` |
| Fuentes externas | Servicios oficiales que una aplicación consulta o importa | Las demás páginas de esta sección y el catálogo de {doc}`/desarrollo/databases` |

Las aplicaciones que consultan servicios externos desde el servidor usan el cliente HTTP de la plataforma (`IClientService`), con un `User-Agent` propio de la forma `APS-Conecta-<App>/1.0 (+<repositorio>)` y un paquete de CA propio cuando el servidor sirve una cadena TLS incompleta. Nunca se desactiva la verificación. Epidemiología y estadística son los ejemplos vigentes; ver {doc}`/desarrollo/epidemiologia` y {doc}`/desarrollo/estadistica`.

Los errores que ve la persona usuaria siguen la forma común de `aps-common` ({doc}`/desarrollo/aps-common`): una frase en español en `{message}`, con 422 para un rechazo y 404 para algo que no existe.

## Compromisos y límites

Cómo cada aplicación registra sus fuentes, con qué frecuencia las actualiza y dónde guarda las copias de las capas queda fuera de esta sección. Se decide aplicación por aplicación, y el mapa de territorio todavía no lo ha definido.
