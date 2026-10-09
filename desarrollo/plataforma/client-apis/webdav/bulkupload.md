---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de subida masiva: subir muchos archivos pequeños en una sola solicitud HTTP multipart, con las cabeceras de cada archivo y un script de ejemplo."
---
# Subida masiva de archivos

## Resumen

Esta página describe, para quienes desarrollan clientes, la API de subida masiva: cómo enviar muchos archivos pequeños en una sola solicitud HTTP multipart, qué cabeceras lleva cada parte, qué estructura tiene la respuesta y un script de ejemplo en Bash.

````{upstream} developer_manual/client_apis/WebDAV/bulkupload.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Introducción

Subir muchos archivos pequeños suele ser más lento de lo que se podría lograr, porque no se
usa todo el ancho de banda de la red. Nextcloud tiene una API de subida masiva con la que se pueden subir
muchos archivos pequeños juntos para optimizar el uso del ancho de banda de la red.

### Uso

La API solo está disponible para los usuarios registrados de la instancia, y usa la ruta:
`<server>/remote.php/dav/bulk`.

#### Iniciar una subida masiva

Una subida masiva consiste simplemente en usar una solicitud estructurada como HTTP multipart con el tipo MIME related.

Cada archivo se envía entonces como una parte HTTP.

Cada archivo dentro de una parte HTTP necesitará las siguientes cabeceras:

- Content-Length: \<tamaño del archivo>
- Content-Type: \<tipo MIME>
- X-File-MD5: \<suma de comprobación md5>
- X-File-Mtime: \<hora de modificación del archivo>
- X-File-Path: \<ruta de destino del archivo>

La respuesta es un documento JSON con la siguiente estructura:

```json
{
    "/small file.txt": {
        "error": false,
        "etag": "adb9aa24cbfa8e372c88431d1d99629a"
    }
}
```

Ejemplo de código para subir algunos archivos de prueba con el protocolo de subida masiva

```bash
#!/bin/bash

NB=$1
SIZE=$2

USER="admin"
PASS="admin"
SERVER="nextcloud.local"
UPLOAD_PATH="/tmp/bulk_upload_request_$(openssl rand --hex 8).txt"
BOUNDARY="boundary_$(openssl rand --hex 8)"
REMOTE_FOLDER="/test"

for ((i=1; i<="$NB"; i++))
do
        file_name=$(openssl rand --hex 8)
        file_local_path="./$file_name.txt"
        file_remote_path="$REMOTE_FOLDER/$file_name.txt"
        head -c "$SIZE" /dev/urandom > "$file_local_path"
        file_mtime=$(stat -c %Y "$file_local_path")
        file_hash=$(md5sum "$file_local_path" | awk '{ print $1 }')
        file_size=$(du -sb "$file_local_path" | awk '{ print $1 }')

        {
                echo -en "--$BOUNDARY\r\n"
                echo -en "X-File-Path: $file_remote_path\r\n"
                echo -en "X-OC-Mtime: $file_mtime\r\n"
                echo -en "X-File-Md5: $file_hash\r\n"
                echo -en "Content-Length: $file_size\r\n"
                echo -en "\r\n" >> "$UPLOAD_PATH"

                cat "$file_local_path"
                echo -en "\r\n" >> "$UPLOAD_PATH"
        } >> "$UPLOAD_PATH"
done

echo -en "--$BOUNDARY--\r\n" >> "$UPLOAD_PATH"

echo "Creating folder /test"
curl \
        -X MKCOL \
        -k \
        "https://$USER:$PASS@$SERVER/remote.php/dav/files/$USER/test" > /dev/null

echo "Uploading $NB files with total size: $(du -sh "$UPLOAD_PATH" | cut -d '   ' -f1)"
echo "Local file is: $UPLOAD_PATH"
curl \
        -X POST \
        -k \
        --progress-bar \
        --cookie "XDEBUG_PROFILE=true;path=/;" \
        -H "Content-Type: multipart/related; boundary=$BOUNDARY" \
        --data-binary "@$UPLOAD_PATH" \
        "https://$USER:$PASS@$SERVER/remote.php/dav/bulk"
```
````
