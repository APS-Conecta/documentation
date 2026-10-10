---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API de borrado remoto para clientes: consulta del estado de borrado, datos que el cliente debe eliminar y aviso de finalización al servidor."
---
(nc-dev-remotewipeindex)=
# Borrado remoto

## Resumen

Esta página describe, para quienes desarrollan clientes, la API de borrado remoto: cómo consultar si el dispositivo debe borrarse, qué datos debe eliminar el cliente y cómo indicar al servidor que el borrado terminó.

````{upstream} developer_manual/client_apis/RemoteWipe/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

Este documento ofrece una visión general rápida de la API de borrado remoto que deben usar los clientes para implementar la funcionalidad de borrado remoto.
Esto permitirá a los usuarios borrar, por ejemplo, un dispositivo perdido.

Debe tenerse en cuenta que el borrado solo funciona cuando los clientes usan el flujo de inicio de sesión, de modo que se establezca un token dedicado para este cliente.

### Obtención del estado de borrado

Cuando un cliente recibe una respuesta con estado 401 o 403, realiza una petición a {code}`<server>/index.php/core/wipe/check` y asigna al parámetro token el token de aplicación.

```bash
curl https://cloud.example.com/index.php/core/wipe/check -X POST -d 'token=<TOKEN>'
```

Si el cliente recibe como respuesta un código de estado 200 y un array JSON con wipe establecido en true, como:

```json
{
        "wipe":true
}
```

entonces el cliente debe proceder a borrar el dispositivo.

### Borrado del dispositivo propiamente dicho

- El cliente debe eliminar todos los datos de usuario vinculados a la cuenta. Esto incluye:
  - cachés
  - archivos sin conexión
  - la propia cuenta

### Notificación de la finalización

Una vez que el cliente ha borrado todos los datos requeridos, debe hacerse un POST a {code}`<server>/index.php/core/wipe/success` con el token.
Esto indica al servidor que el borrado se ha completado y desencadena la limpieza final en el lado del servidor.

```bash
curl https://cloud.example.com/index.php/core/wipe/success -X POST -d 'token=<TOKEN>'
```
````

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
