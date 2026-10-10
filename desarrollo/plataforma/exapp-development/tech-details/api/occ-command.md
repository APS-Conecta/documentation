---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de AppAPI para que una ExApp registre y anule comandos OCC que disparan acciones en la ExApp: parámetros, modos de Symfony y un ejemplo."
---
(nc-dev-occ_command)=
# Comando OCC

## Resumen

Esta página describe la API con la que una ExApp registra comandos de la CLI de OCC que disparan una acción en el lado de la ExApp: los parámetros de registro, un ejemplo y la anulación del registro. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/occ_command.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta API permite registrar comandos de la CLI de OCC.
El principio es similar al del comando occ habitual de las apps PHP, que funcionan dentro del contexto de la instancia de Nextcloud,
pero, para las ExApps, es un disparador a través de la interfaz OCC de Nextcloud para realizar alguna acción en el lado de la ExApp.

:::{note}
No se admite pasar archivos directamente como argumento de entrada al comando occ.
:::

### Registrar

Endpoint OCS: `POST /apps/app_api/api/v1/occ_command`

#### Parámetros

```json
{
    "name": "appid:unique:command:name",
    "description": "Description of the command",
    "hidden": "1/0",
    "arguments": [
        {
            "name": "argument_name",
            "mode": "required/optional/array",
            "description": "Description of the argument",
            "default": "default_value"
        }
    ],
    "options": [
        {
            "name": "option_name",
            "shortcut": "s",
            "mode": "required/optional/none/array/negatable",
            "description": "Description of the option",
            "default": "default_value"
        }
    ],
    "usages": [
        "occ appid:unique:command:name argument_name --option_name",
        "occ appid:unique:command:name argument_name -s"
    ],
    "execute_handler": "handler_route"
}
```

Para más detalles sobre los modos de los argumentos y las opciones del comando,
ver la documentación original de los parámetros de entrada de la consola de Symfony, que en realidad se construyen a partir de los datos proporcionados:
<https://symfony.com/doc/current/console/input.html#using-command-arguments>

#### Ejemplo

Supóngase un comando *ping* que recibe un argumento *test_arg* y tiene una opción *test-option*:

```json
{
    "name": "my_app_id:ping",
    "description": "Test ping command",
    "hidden": 0,
    "arguments": [
        {
            "name": "test_arg",
            "mode": "required",
            "description": "Test argument",
            "default": 123
        }
    ],
    "options": [
        {
            "name": "test-option",
            "shortcut": "t",
            "mode": "none",
            "description": "Test option",
        }
    ],
    "usages": [
        "occ my_app_id:ping 12345",
        "occ my_app_id:ping 12345 --test-option",
        "occ my_app_id:ping 12345 -t"
    ],
    "execute_handler": "handler_route"
}
```

### Anular el registro

Endpoint OCS: `DELETE /apps/app_api/api/v1/occ_command`

#### Parámetros

Para anular el registro de un comando de la CLI de OCC, basta con indicar el *name* del comando:

```json
{
    "name": "occ_command_name"
}
```
````
