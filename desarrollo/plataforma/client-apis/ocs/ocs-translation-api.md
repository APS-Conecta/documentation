---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de traducción: obtener los idiomas y opciones de traducción disponibles y traducir una cadena, con campos, códigos de estado y límites."
---
(nc-dev-ocs-translation-api)=
# API OCS de traducción

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de traducción: los endpoints para obtener las opciones de traducción disponibles y traducir una cadena de un idioma a otro, con sus campos y códigos de estado.

````{upstream} developer_manual/client_apis/OCS/ocs-translation-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

:::{versionadded} 26
:::

La API OCS de traducción permite traducir cadenas de un idioma a otro.

La URL base de todas las llamadas a la API de traducción es: `<nextcloud_base_url>/ocs/v2.php/translation/`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Obtener las opciones de traducción disponibles

:::{versionadded} 26
:::

- Método: `GET`
- Endpoint: `/languages`
- Respuesta:
  - Código de estado:
    - `200 OK`
  - Datos:

| campo | tipo | Descripción |
|---|---|---|
| `languageDetection` | bool | Si se puede omitir el idioma de origen, porque un proveedor de traducción admite detectarlo a partir de la entrada |
| `languages` | array | Una lista de tuplas de idioma; ver la definición más abajo |

#### Estructura de una tupla de idioma

| campo | tipo | Descripción |
|---|---|---|
| `from` | string | Código ISO del idioma de origen |
| `fromLabel` | string | Nombre del idioma de origen que se debe mostrar al usuario |
| `to` | string | Código ISO del idioma de destino |
| `toLabel` | string | Nombre del idioma de destino que se debe mostrar al usuario |

### Traducir una cadena

:::{versionadded} 26
:::

:::{note}
El endpoint tiene un límite de frecuencia de solicitudes, ya que puede consumir bastantes recursos. Los usuarios pueden hacer 25 solicitudes en 2 minutos; los invitados, solo 10
:::

- Método: `POST`
- Endpoint: `/translate`
- Datos:

| campo | tipo | Descripción |
|---|---|---|
| `text` | string | El texto que se va a traducir |
| `fromLanguage` | string/null | El código ISO del idioma de origen; cuando se indica null y un proveedor de traducción permite detectar el idioma de origen, se intentará adivinarlo a partir de la entrada `text` |
| `toLanguage` | string | El código ISO del idioma de destino |

- Respuesta:
  - Código de estado:
    - `200 OK`
    - `400 Bad Request` - Cuando ningún proveedor admite el idioma de destino
    - `400 Bad Request` - Cuando ningún proveedor admite el idioma de origen
    - `400 Bad Request` - Cuando no se indica el idioma de origen, pero ningún proveedor admite la detección del idioma
    - `412 Precondition Failed` - Cuando no hay ningún proveedor de traducción instalado
    - `429 Too Many Requests` - Cuando se superó el límite de frecuencia de solicitudes
  - Datos:
    - `text` - Solo se proporciona en caso de `200 OK`, la cadena traducida
    - `message` - Solo se proporciona cuando no es `200 OK`, un mensaje de error en el idioma del usuario, listo para mostrarse
    - `from` - El idioma de origen que se proporcionó o que se detectó a partir de la entrada (también puede ser null o faltar, cuando ocurre un error al detectar el idioma)
````
