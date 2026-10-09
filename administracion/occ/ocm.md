---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Comandos occ de OCM: listar las claves de firma del JWKS, sus tres ranuras y la rotación en tres pasos (preparar, activar, retirar)."
---
# Comandos de OCM

## Resumen

Esta página es la referencia de los comandos `occ` que gestionan las claves de firma de la federación Open Cloud Mesh (OCM): las tres ranuras de claves, cómo listarlas y cómo rotarlas en tres pasos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/occ_ocm.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los comandos `ocm` gestionan las claves de firma que Nextcloud usa para la federación Open Cloud Mesh (OCM). Las solicitudes OCM salientes se firman con firmas de mensajes HTTP ([RFC 9421](https://www.rfc-editor.org/rfc/rfc9421)), y las claves públicas correspondientes se publican como un [conjunto de claves web JSON (JWKS)](https://www.rfc-editor.org/rfc/rfc7517) para que los pares federados puedan verificarlas.

Estos comandos forman parte del núcleo del servidor y están siempre disponibles. Se usan para inspeccionar y rotar las claves de firma del JWKS; no hacen falta para el funcionamiento normal, ya que se genera una clave automáticamente en la primera solicitud OCM.

:::{note}
Para más información sobre la federación y OCM, consultar {nc-doc}`admin_manual/configuration_files/federated_cloud_sharing_configuration`.
:::

```
ocm
 ocm:keys:list       list JWKS-published signing keys
 ocm:keys:stage      generate a new JWKS key and advertise it via JWKS without using it for signing yet
 ocm:keys:activate   promote the staged JWKS key to active; the previous active key moves to retiring
 ocm:keys:retire     delete the retiring JWKS key; signatures that referenced its kid can no longer be verified
```

### Ranuras de claves

Las claves de firma se guardan en tres ranuras, y todas se publican en el endpoint del JWKS mientras están ocupadas:

- **active**: la clave que se usa actualmente para firmar las solicitudes OCM salientes.
- **pending**: una clave recién preparada que se anuncia en el JWKS pero que aún no se usa para firmar. Así los pares federados tienen tiempo de obtenerla antes de que pase a estar activa.
- **retiring**: la clave activa anterior, que se mantiene publicada para que las firmas creadas con ella puedan seguir verificándose hasta que se elimine.

### Listado de claves

#### ocm:keys:list

Mostrar las claves de firma actuales del JWKS y la ranura que ocupa cada una:

```
sudo -E -u www-data php occ ocm:keys:list
+------+----------+--------------------------------+
| Pool | Slot     | Key ID                         |
+------+----------+--------------------------------+
| 1    | active   | ecdsa-p256-sha256-...          |
| 2    | pending  | ecdsa-p256-sha256-...          |
+------+----------+--------------------------------+
```

Si aún no existen claves, el comando informa de que se generará una en la primera solicitud OCM. Usar `--output=json` o `--output=json_pretty` para obtener una salida legible por máquina.

### Rotación de claves

La rotación de claves es un proceso de tres pasos: preparar una clave nueva, activarla y luego retirar la anterior. Hay que dejar pasar tiempo entre los pasos para que los pares federados puedan actualizar su copia en caché del JWKS (la caché dura una hora).

#### ocm:keys:stage

Generar una clave nueva en la ranura **pending**. Se anuncia en el JWKS, pero aún no se usa para firmar:

```
sudo -E -u www-data php occ ocm:keys:stage
  Staged new JWKS key: ecdsa-p256-sha256-...
  Wait for federated peers to refresh their JWKS cache before activating.
```

Primero se necesita una clave activa; si no existe ninguna, se genera una automáticamente. El comando falla si ya existe una clave pendiente: hay que activarla o retirarla antes de preparar otra.

#### ocm:keys:activate

Promover la clave preparada (pendiente) a **active**. La clave activa anterior pasa a la ranura **retiring**, donde sigue publicada en el JWKS para que las firmas en curso puedan seguir verificándose:

```
sudo -E -u www-data php occ ocm:keys:activate
  Staged key promoted to active.
  Run occ ocm:keys:retire once any in-flight signatures using the previous key have been verified.
```

El comando falla si no hay ninguna clave pendiente que activar o si la ranura de retiro sigue ocupada: hay que retirar antes la clave anterior.

#### ocm:keys:retire

Eliminar la clave **retiring**. Una vez eliminada, las firmas que hacían referencia a su ID de clave ya no pueden verificarse, así que solo hay que ejecutarlo cuando se tenga la seguridad de que ningún par la necesita todavía (por ejemplo, después de que haya pasado al menos un periodo de vida de la caché del JWKS desde la activación):

```
sudo -E -u www-data php occ ocm:keys:retire
  Retiring key deleted.
```

El comando falla si no hay ninguna clave en retiro que eliminar.
````
