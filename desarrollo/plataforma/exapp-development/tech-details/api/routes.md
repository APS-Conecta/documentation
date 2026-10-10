---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una ExApp declara en info.xml las rutas accesibles por el proxy de ExApps de AppAPI: campos de cada ruta, registro y anulación automáticos."
---
(nc-dev-ex_app_routes)=
# Rutas

## Resumen

Esta página describe cómo una ExApp declara, en la etiqueta `routes` de su `info.xml`, las rutas a las que se permite acceder a través del proxy de ExApps de AppAPI, qué indica cada campo de una ruta y cuándo se registran y se anulan automáticamente. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/routes.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Todas las ExApps deben declarar las rutas a las que se permite acceder a través del proxy de ExApps de AppAPI (`/apps/app_api/proxy/*`).

### Registrar

Durante la instalación de la ExApp, sus rutas se registran automáticamente.
Las rutas deben declararse en la etiqueta `external-app` - `routes` del archivo `info.xml`.

#### Ejemplo

```
...
<external-app>
    <routes>
        <route>
            <url>.*</url>
            <verb>GET,POST,PUT,DELETE</verb>
            <access_level>USER</access_level>
            <headers_to_exclude>[]</headers_to_exclude>
            <bruteforce_protection>[401, 500]</bruteforce_protection>
        </route>
    </routes>
</external-app>
...
```

donde los campos son:

- `url`: la ruta que se registrará en el lado de la ExApp; puede ser una expresión regular
- `verb`: el verbo HTTP que aceptará la ruta; puede ser una lista de verbos separados por comas
- `access_level`: el nombre del nivel de acceso necesario para acceder a la ruta: PUBLIC - acceso público sin autenticación, USER - se requiere la autenticación de un usuario de Nextcloud, ADMIN - se requiere un usuario administrador
- `headers_to_exclude`: una cadena codificada en JSON de un array de cadenas: las cabeceras que la ExApp quiere que se excluyan de la solicitud que se le envía
- `bruteforce_protection`: una cadena codificada en JSON de un array de números: los códigos de estado HTTP que deben activar la protección contra fuerza bruta

### Anular el registro

El registro de las rutas de la ExApp se anula automáticamente cuando se desinstala la ExApp,
y las rutas nuevas se vuelven a registrar cuando se actualiza la ExApp.
````
