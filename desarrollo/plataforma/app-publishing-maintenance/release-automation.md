---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo automatizar con GitHub Actions la compilación, la firma y la subida de una versión de una app a la tienda de apps, con los cambios del Makefile."
---
# Automatización de versiones

## Resumen

Esta página explica cómo automatizar con GitHub Actions la compilación, la firma y la subida de una nueva versión de una app a la tienda de apps, incluidos los secretos que necesita el workflow y los cambios en el Makefile para la firma de código. Está dirigida a quienes publican apps.

````{upstream} developer_manual/app_publishing_maintenance/release_automation.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La automatización es algo estupendo: evita errores y facilita la vida, lo que deja más tiempo para trabajar en todas esas funciones que se querían implementar.

### GitHub Actions

Si el repositorio de la aplicación está en GitHub, como ocurre con muchas aplicaciones de Nextcloud, GitHub Actions es una excelente forma de automatizar la publicación de la app desde el repositorio git en la tienda de apps de {vendor}`Nextcloud`.

Una forma sencilla de empezar es usar <https://github.com/R0Wi/nextcloud-appstore-push-action> en el repositorio junto con algunas otras acciones. Así se puede compilar automáticamente la app y publicarla en la tienda de apps. Admite versiones preliminares y firma de código.
Para empezar, crear un nuevo archivo yaml en el directorio `.github/workflows`.

```yaml
name: Build and publish app release

on:
  release:
      types: [published]

env:
  APP_NAME: news

jobs:
  build_and_publish:
    environment: release
    runs-on: ubuntu-latest
    name: "Release: build, sign and upload the app"
    strategy:
      matrix:
        php-versions: ['7.4']
        nextcloud: ['stable21']
        database: ['sqlite']
    steps:
      - name: Checkout
        uses: actions/checkout@5a4ac9002d0be2fb38bd78e4b4dbde5606d7042f

      - name: Setup PHP
        uses: shivammathur/setup-php@afefcaf556d98dc7896cca380e181decb609ca44
        with:
          php-version: ${{ matrix.php-versions }}
          extensions: pdo_sqlite,pdo_mysql,pdo_pgsql,gd,zip
          coverage: none

      - name: Set up server non MySQL
        uses: SMillerDev/nextcloud-actions/setup-nextcloud@fae87e29aa7cdf1ea0b8033c67f60e75b10be2cd
        with:
          cron: false
          version: ${{ matrix.nextcloud }}
          database-type: ${{ matrix.database }}

      - name: Prime app build
        run: make

      - name: Configure server with app
        uses: SMillerDev/nextcloud-actions/setup-nextcloud-app@fae87e29aa7cdf1ea0b8033c67f60e75b10be2cd
        with:
          app: ${{ env.APP_NAME }}
          check-code: false

      - name: Create signed release archive
        run: |
          cd ../server/apps/${{ env.APP_NAME }} && make appstore
        env:
          app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
          app_public_crt: ${{ secrets.APP_PUBLIC_CRT }}

      - name: Upload app tarball to release
        uses: svenstaro/upload-release-action@483c1e56f95e88835747b1c7c60581215016cbf2
        id: attach_to_release
        with:
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          file: ../server/apps/${{ env.APP_NAME }}/build/artifacts/appstore/${{ env.APP_NAME }}.tar.gz
          asset_name: ${{ env.APP_NAME }}.tar.gz
          tag: ${{ github.ref }}
          overwrite: true

      - name: Upload app to Nextcloud appstore
        uses: R0Wi/nextcloud-appstore-push-action@a011fe619bcf6e77ddebc96f9908e1af4071b9c1
        with:
          app_name: ${{ env.APP_NAME }}
          appstore_token: ${{ secrets.APPSTORE_TOKEN }}
          download_url: ${{ steps.attach_to_release.outputs.browser_download_url }}
          app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
          nightly: ${{ github.event.release.prerelease }}

      - name: Delete crt and key from local storage
        run: rm -f ~/.nextcloud/certificates/*
```

Asegurarse de revisar si las acciones usadas tienen actualizaciones útiles, ya que están fijadas a un sha1 concreto para evitar cambios dañinos que pasen inadvertidos.

Para que este workflow funcione hay que proporcionar algunas variables.

- `APP_NAME` establece el nombre de la app, directamente en el yaml

Luego hay algunos secretos; hay que manejarlos con cuidado.
Si el repositorio está dentro de la organización nextcloud, hay que usar un entorno (environment).

```yaml
jobs:
  build_and_publish:
    environment: release
    runs-on: ubuntu-latest
```

En este ejemplo se usa el entorno «release»: abrir los ajustes del repositorio y la pestaña «Environments», añadir un nuevo entorno con el nombre «release», asegurarse de activar «Required reviewers» y añadir solo a las personas de confianza, que podrán aprobar una versión.
Guardar las reglas y, al final, añadir los siguientes secretos del entorno.

- `APP_PRIVATE_KEY` la clave privada de la app
- `APP_PUBLIC_CRT` el certificado de la app; este podría ser público, pero para facilitar su uso se añade como secreto
- `APPSTORE_TOKEN` se obtiene en la tienda de apps como desarrollador registrado <https://apps.nextcloud.com/account/token>

Si la app no está en la organización de {vendor}`Nextcloud`, también se pueden añadir los secretos anteriores en la sección «Secrets», pero con cuidado: cualquiera con acceso de escritura al repositorio podrá crear versiones. Asegurarse también de eliminar la declaración del entorno.

Si no se usa firma de código para la app, se puede eliminar la siguiente sección del yaml.

```yaml
env:
app_private_key: ${{ secrets.APP_PRIVATE_KEY }}
app_public_cert: ${{ secrets.APP_PUBLIC_CERT }}
```

Asegurarse también de eliminar `environment: release`.

#### Cambios en el Makefile para la firma de código

Como el certificado y la clave privada ahora se guardan en variables de entorno, hay que convertirlos de algún modo en un archivo.
Un ejemplo que puede usarse lo proporciona la app News.

```php
#!/usr/bin/env php
<?php
/**
* Nextcloud - News
*
* This file is licensed under the Affero General Public License version 3 or
* later. See the COPYING file.
*
* @author Benjamin Brahmer <info@b-brahmer.de>
* @copyright Benjamin Brahmer 2020
*/

if ($argc < 2) {
    echo "This script expects two parameters:\n";
    echo "./file_from_env.php ENV_VAR PATH_TO_FILE\n";
    exit(1);
}

# Read environment variable
$content = getenv($argv[1]);

if (!$content){
    echo "Variable was empty\n";
    exit(1);
}

file_put_contents($argv[2], $content);

echo "Done...\n";
```

Es un script php muy sencillo que recibe una variable de entorno y una ruta de archivo, y vuelca en el archivo lo que encuentre en la variable.
Después de guardar el script en algún lugar del repositorio, se puede usar en el Makefile.

```bash
cert_dir=$(HOME)/.nextcloud/certificates
[...]
appstore:
[...]
# export the key and cert to a file
mkdir -p $(cert_dir)
php ./bin/tools/file_from_env.php "app_private_key" "$(cert_dir)/$(app_name).key"
php ./bin/tools/file_from_env.php "app_public_crt" "$(cert_dir)/$(app_name).crt"
[...]
```

Asegurarse también de que estos archivos se usen al firmar la app, en el Makefile.

```bash
@if [ -f $(cert_dir)/$(app_name).key ]; then \
  echo "Signing app files…"; \
  php ../../occ integrity:sign-app \
    --privateKey=$(cert_dir)/$(app_name).key\
    --certificate=$(cert_dir)/$(app_name).crt\
    --path=$(appstore_sign_dir)/$(app_name); \
  echo "Signing app files ... done"; \
fi
```

Y eso es básicamente todo lo que hay que hacer: se pueden usar la clave y el certificado al firmar la app.

#### El proceso

1. Crear una nueva versión (release) en GitHub, con la información que se suela incluir.
2. Decidir si debe ser una versión normal o una versión preliminar; las versiones preliminares se subirán a la tienda de apps como versión nightly.
3. Al terminar, publicar la versión y esperar unos minutos; aparecerá una solicitud para aprobar la versión, en Actions o en las notificaciones.
4. Si todo funcionó, se encontrará un `appname.tar.gz` como adjunto de la versión.
5. Comprobar la versión recién publicada en la tienda de apps; enhorabuena por la primera app publicada automáticamente.
````
