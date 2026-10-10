---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Pasos con que AppAPI instala una ExApp: descarga de la imagen según computeDevice y los endpoints /heartbeat, /init y /enabled que la app implementa."
---
(nc-dev-app_installation_flow)=
# Flujo de instalación de la app

## Resumen

Esta página describe, paso a paso, cómo AppAPI instala una ExApp: qué imagen de Docker descarga según el valor de *computeDevice* y qué solicitudes envía a los endpoints `/heartbeat`, `/init` y `/enabled`, con las respuestas que la app debe devolver. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/InstallationFlow.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Descarga de la imagen (Docker)

AppAPI intentará primero descargar la imagen de Docker cuyo `suffix` sea igual al valor de *computeDevice*.

Los valores disponibles para `computeDevice` son: `cpu`, `cuda` o `rocm`.

El sufijo se añadirá de la siguiente manera:

```
return $imageParams['image_src'] . '/' .
    $imageParams['image_name'] . '-' . $daemonConfig['computeDevice']['id'] . ':' . $imageParams['image_tag'];
```

Para `cpu`, AppAPI intentará primero obtener la imagen de `ghcr.io/nextcloud/skeleton-cpu:latest`.
Si no se encuentra la imagen, se descargará `ghcr.io/nextcloud/skeleton:latest`.

Quien desarrolla la aplicación y quiera imágenes personalizadas para cualquiera de estos valores
puede subir al registro las imágenes extendidas, además de la imagen base.

### Heartbeat

Lo primero que hace AppAPI es desplegar la aplicación.

En el caso de Docker, esto significa:

1. descargar la imagen (pull)
2. crear el contenedor a partir de la imagen de Docker
3. si el contenedor admite *healthcheck*, AppAPI espera el estado *healthy*
4. esperar hasta que el endpoint «/heartbeat» esté disponible con una solicitud `GET`

En respuesta a la solicitud «/heartbeat», la aplicación debe devolver: `{"status": "ok"}`.

:::{note}
La solicitud al endpoint `/heartbeat` se hace sin autenticación de AppAPI.
:::

### Inicialización

:::{note}
A partir de este punto, todas las solicitudes que hace AppAPI contienen {nc-ref}`cabeceras de autenticación <auth-headers>`.
:::

Cuando la aplicación está lista, según lo determina el paso anterior,
AppAPI envía una solicitud `POST` al endpoint `/init` de la aplicación.

*Si la aplicación no necesita realizar una inicialización larga, tiene la opción de no implementar el endpoint «/init»; así,
AppAPI recibirá un error 404 o 501 en su solicitud, pero se puede considerar que la inicialización está hecha y esta sección puede omitirse.*

Si se quiere implementar el endpoint «/init», la aplicación debe:

1. En el manejador de «/init»: devolver una respuesta con datos JSON vacíos ante la llamada de AppAPI.
2. En una tarea en segundo plano: enviar una solicitud OCS a `PUT /ocs/v1.php/apps/app_api/ex-app/status` con el valor del progreso.

:::{warning}
`PUT /ocs/v1.php/apps/app_api/apps/status/$APP_ID` está obsoleto y se eliminará en el futuro.
:::

Los valores posibles de **progress** son enteros del 1 al 100;
tras recibir el valor 100, **la aplicación se considera inicializada y lista para funcionar**.

Si, en la etapa de inicialización, la aplicación sufre un error crítico que hace imposible que siga funcionando,
debe añadirse
`"error": "some error"`
a la `OCS request` que establece el progreso,
con una breve explicación de en qué etapa ocurrió el error.

Ejemplo de carga útil de una solicitud con error:

```
{"progress": 67, "error": "connection error to huggingface."}
```

### Habilitación

Tras recibir **progress: 100** (*o cuando la ExApp no implementa el endpoint «/init»*), AppAPI habilita la aplicación.

Para habilitar o deshabilitar la aplicación, se envía una solicitud PUT al endpoint `/enabled`.

:::{note}
A diferencia de usar una carga útil, esta solicitud utiliza un parámetro de consulta llamado `enabled` para indicar el estado deseado.
:::

El parámetro `enabled` acepta un valor entero:

- *1* para habilitar la aplicación
- *0* para deshabilitar la aplicación

Por ejemplo, para habilitar la aplicación, la solicitud sería:

```
PUT http://ex-app:2432/enabled?enabled=1
```

Del mismo modo, para deshabilitar la aplicación, la solicitud sería:

```
PUT http://ex-app:2432/enabled?enabled=0
```

Este enfoque garantiza que el estado de la aplicación pueda alternarse fácilmente con un simple parámetro de consulta.

:::{note}
El endpoint `/enabled` comparte tanto la **habilitación** como la **deshabilitación**,
así que la app debe determinar qué ocurre mediante el parámetro de entrada `enabled` de la solicitud.
:::

Dentro del manejador de `/enabled`, la aplicación debe registrar todas las acciones relacionadas con Nextcloud, como la interfaz y otras cosas.

La respuesta a esta solicitud debe contener:

```
{"error": ""}
```

en caso de éxito; y si se produce algún error durante la **habilitación**, debe estar presente y no estar vacío:

```
{"error": "i can't handle enabling"}
```

Estos son todos los pasos del flujo de instalación de una ExApp.
````
