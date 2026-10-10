---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Qué hacer al cambiar código PHP de backend: actualizar el cargador automático y anotar las API públicas con @since y @deprecated."
---
# Código de backend

## Resumen

Esta página explica qué hacer antes de confirmar cambios en el código PHP de backend del servidor: regenerar los archivos del cargador automático cuando se crean archivos nuevos y documentar la compatibilidad de las API públicas con `@since` y `@deprecated`. Está dirigida a quienes desarrollan el servidor.

````{upstream} developer_manual/server/code-back-end.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Al cambiar código PHP de backend, en general no hace falta ningún paso adicional antes de confirmar los cambios.

Sin embargo, si se crearon archivos nuevos, hay que ejecutar el siguiente comando para actualizar los archivos del cargador automático:

```console
build/autoloaderchecker.sh
```

Después, incluir también en los commits los cambios de los archivos del cargador automático.

### Documentación de compatibilidad

- Las API nuevas (interfaces, constantes, métodos, clases, traits, enums) que se agregan al espacio de nombres público `OCP` deben anotarse con un atributo `@since X.Y.Z` con la versión en la que se agregaron.
- Cuando se hace un backport, la versión debe ajustarse al X.Y.Z de la versión estable en la que se hizo el backport, solo en esa rama estable.
  La rama master debe seguir indicando la versión mayor más reciente que incluye la API.
- Una vez publicada una API, salvo que esté marcada como experimental, debe declararse obsoleta de forma similar con `@deprecated X.Y.Z` durante 3 años (9 versiones de Nextcloud) antes de que pueda eliminarse.
  Las obsolescencias deben documentarse claramente en {nc-ref}`critical-changes` para la próxima versión mayor.
````
