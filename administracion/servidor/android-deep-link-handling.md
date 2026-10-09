---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Enlaces profundos en Android: por qué desde Android 12 cada host debe publicar su propio assetlinks.json y por qué Nextcloud no puede hacerlo por todos."
---
# Gestión de enlaces profundos en Android

## Resumen

Esta página explica cómo funcionan los enlaces profundos en Android, qué archivo `assetlinks.json` exige Android 12 y versiones posteriores para asociar la app con el dominio, y por qué Nextcloud no puede configurarlo para todos los hosts. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/android_deep_link_handling.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los enlaces profundos en Android permiten que una aplicación se abra directamente desde una URL, lo que facilita a los usuarios llegar a un contenido concreto dentro de la app. A partir de Android 12, gestionar los enlaces profundos requiere una configuración adicional mediante un archivo `assetlinks.json`, para garantizar que la app y el dominio del host estén correctamente asociados.

### Android 11 y versiones anteriores

En Android 11 y versiones anteriores, los enlaces profundos son sencillos y no requieren más configuración que los ajustes habituales del manifiesto.

### Android 12 y versiones posteriores

En Android 12 y versiones posteriores se requiere un paso de configuración adicional para verificar la relación entre la app y el dominio del host mediante el archivo `assetlinks.json`.

#### Crear assetlinks.json

Crear un archivo llamado `assetlinks.json` y alojarlo en el directorio .well-known del sitio web (p. ej., https://www.cloud.example.com/.well-known/assetlinks.json).

Ejemplo de `assetlinks.json`:

```
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.cloud.example.nextcloud",
      "sha256_cert_fingerprints": [
        "FB:00:95:22:F6:5E:25:80:22:61:B6:7B:10:A4:5F:D7:0E:61:00:31:97:6F:40:B2:8A:64:9E:15:2D:ED:03:73"
      ]
    }
  }
]
```

##### Limitación de la configuración de Nextcloud

Debido al requisito adicional de alojar un archivo `assetlinks.json` en Android 12 y versiones posteriores, Nextcloud no puede configurar el cliente de Android para todos los distintos hosts. Esto se debe a que cada host necesita su propio archivo `assetlinks.json` para establecer una relación verificada con la app, y Nextcloud no puede gestionar este archivo para cada posible dominio de host.
````
