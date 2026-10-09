---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Parámetros de config.php para fijar o forzar el idioma y la configuración regional predeterminados de Nextcloud."
---
# Idioma y configuración regional

## Resumen

Esta página describe, para quienes administran el servidor, los parámetros de `config.php` que fijan el idioma y la configuración regional predeterminados de Nextcloud o que los fuerzan para todos los usuarios.

````{upstream} admin_manual/configuration_server/language_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Idioma predeterminado

En condiciones normales, Nextcloud detecta automáticamente el idioma de la interfaz web. Si esto no funciona correctamente o se quiere garantizar que Nextcloud arranque siempre con un idioma determinado, puede establecerse el parámetro **default_language** en {file}`config/config.php`.

:::{note}
El parámetro `default_language` solo se aplica cuando el navegador no envía ninguna preferencia de idioma y el usuario no ha establecido la suya. Acepta códigos ISO 639-1 como `en` (inglés), `fr` (francés), `de` (alemán informal) o `de_DE` (alemán formal).
:::

```
"default_language" => "en",
```

### Forzar el idioma

Si se fuerza un idioma concreto, los usuarios ya no podrán cambiar su idioma en los ajustes personales. Puede establecerse el parámetro **force_language** en {file}`config/config.php`.

```
"force_language" => "en",
```

Si los usuarios no deben poder cambiar su idioma, pero tienen idiomas distintos, este valor puede establecerse en `true` en lugar de un código de idioma.

:::{note}
Consultar los [códigos de idioma de Transifex](https://explore.transifex.com/languages/) para ver la lista de códigos de idioma válidos.
:::

### Configuración regional predeterminada

La configuración regional define cómo se muestran las fechas y otros formatos. Nextcloud debería elegir automáticamente una configuración regional adecuada según el idioma actual. Los usuarios pueden modificar su configuración regional en su panel de ajustes. Si eso no funciona correctamente o se quiere garantizar que Nextcloud arranque siempre con una configuración regional determinada, puede establecerse el parámetro **default_locale** en {file}`config/config.php`.

:::{note}
El parámetro default_locale solo se usa cuando el usuario no ha configurado sus propias preferencias de configuración regional.
:::

```
"default_locale" => "en_US",
```

### Forzar la configuración regional

Si se fuerza una configuración regional concreta, los usuarios ya no podrán cambiar su configuración regional en los ajustes personales. Puede establecerse el parámetro **force_locale** en {file}`config/config.php`.

```
"force_locale" => "en_US",
```

:::{note}
Consultar [la lista de configuraciones regionales que admite MomentJS](https://github.com/moment/moment/tree/2.18.1/locale) para ver la lista de configuraciones regionales válidas.
:::
````
