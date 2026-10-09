---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Periodos de conservación configurables (papelera, versiones, actividad, tokens, sesiones, registros, copias de seguridad) y su ajuste al RGPD."
---
# Conservación de datos

## Resumen

Esta página describe los periodos de conservación configurables de la papelera, las versiones de archivos, el registro de actividad, los tokens de «Recordarme» y las sesiones, junto con la rotación de registros y las copias de seguridad, y cómo ajustarlos a las obligaciones del RGPD. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/gdpr/data_retention.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud conserva varias categorías de datos más allá del momento en que un usuario los considera «eliminados». Esta página describe los periodos de conservación configurables y cómo ajustarlos a las obligaciones de minimización de datos según el artículo 5(1)(e) del RGPD.

Todos los ajustes siguientes se configuran en `config/config.php`. Consultar {nc-doc}`admin_manual/configuration_server/config_sample_php_parameters` para ver la referencia completa de parámetros.

### Papelera

Cuando un usuario elimina un archivo, este pasa a la papelera. La política de conservación la controla `trashbin_retention_obligation`:

```
'trashbin_retention_obligation' => 'auto',
```

Valores disponibles:

- `auto` (predeterminado): conservar los archivos eliminados al menos 30 días; eliminarlos antes si el usuario se está quedando sin cuota.
- `D1, auto`: conservar al menos D1 días; eliminar antes si la cuota es baja.
- `auto, D2`: eliminar antes si la cuota es baja; garantizar la eliminación después de D2 días en cualquier caso.
- `D1, D2`: conservar al menos D1 días; garantizar la eliminación después de D2 días.
- `disabled`: no vaciar nunca automáticamente la papelera.

A efectos del RGPD, `disabled` significa que los archivos eliminados se conservan indefinidamente: evitarlo salvo que exista un motivo concreto. Establecer un máximo firme (p. ej., `'30, 60'`) ofrece a los usuarios una garantía de eliminación predecible.

Los usuarios con los permisos adecuados pueden vaciar su propia papelera en cualquier momento desde la app Archivos, o un administrador puede ejecutar:

```
sudo -E -u www-data php occ trashbin:cleanup <uid>
```

Para hacer caducar los archivos de todos los usuarios según la política actual:

```
sudo -E -u www-data php occ trashbin:expire
```

### Versiones de archivos

La app Versiones almacena copias anteriores de los archivos modificados. La conservación la controla `versions_retention_obligation`:

```
'versions_retention_obligation' => 'auto',
```

Valores disponibles:

- `auto` (predeterminado): las versiones se depuran según un calendario integrado (se conservan más versiones de los cambios recientes y menos de los antiguos). Consultar {nc-doc}`admin_manual/configuration_files/file_versioning`.
- `D, auto`: conservar las versiones al menos D días y después aplicar el calendario automático.
- `auto, D`: aplicar el calendario automático; garantizar la eliminación después de D días.
- `D1, D2`: conservar al menos D1 días; garantizar la eliminación después de D2 días.
- `disabled`: no eliminar nunca automáticamente las versiones.

Para eliminar versiones de inmediato:

```
sudo -E -u www-data php occ versions:cleanup <uid>
sudo -E -u www-data php occ versions:expire <uid>
```

### Registro de actividad

El registro de actividad recoge los eventos de archivos y de uso compartido de cada usuario. El trabajo cron diario elimina las entradas con más antigüedad que el número de días configurado:

```
'activity_expire_days' => 365,
```

Establecer un valor menor para reducir la huella de datos personales. Establecerlo en `0` desactiva la caducidad automática (las entradas se conservan indefinidamente).

:::{note}
El registro de actividad es distinto del registro de auditoría del sistema que genera la app `admin_audit`. La conservación del registro de auditoría la controla la configuración de rotación de registros, no este ajuste.
:::

### Tokens de «Recordarme»

Cuando los usuarios seleccionan «Recordarme» al iniciar sesión, Nextcloud almacena una cookie de autenticación de larga duración. Su duración la controla:

```
'remember_login_cookie_lifetime' => 60 * 60 * 24 * 15,
```

El valor predeterminado es de 15 días. Reducir este valor obliga a los usuarios a volver a autenticarse con más frecuencia, pero limita la ventana de exposición ante tokens robados.

### Duración de la sesión

Las sesiones activas caducan cuando se cierra el navegador (cookies de sesión). El núcleo no tiene ningún ajuste de caducidad de sesión en el servidor; las sesiones se invalidan cuando el usuario cierra la sesión o cuando un administrador las revoca mediante:

```
sudo -E -u www-data php occ user:auth-tokens:delete <uid>
```

### Registros del servidor y del servidor web

Los registros de acceso del servidor web y el registro de la aplicación Nextcloud contienen direcciones IP y otros datos personales. Almacenarlos indefinidamente no se considera un uso legítimo según el RGPD. Rotar los registros con regularidad y cifrar los registros archivados para proteger los datos personales que contienen.

Una configuración mínima de `logrotate` que rota a diario y conserva los registros durante un periodo limitado:

```text
/var/log/nextcloud/*.log {
    daily
    rotate 90
    compress
    shred
    missingok
    notifempty
}
```

Ajustar el valor de `rotate` según las obligaciones legales y los requisitos de seguridad. Si la ley obliga a conservar los registros durante un periodo concreto (p. ej., para cumplir leyes nacionales de ciberseguridad), esa obligación prevalece sobre el principio de minimización, pero el periodo de conservación debe indicarse en la política de privacidad.

:::{note}
La protección contra ataques de fuerza bruta de Nextcloud almacena las direcciones IP de los inicios de sesión fallidos, pero estas se eliminan automáticamente al cabo de 24 horas o tras un inicio de sesión correcto y no requieren gestión manual.
:::

### Copias de seguridad

Cuando se atiende una solicitud de supresión eliminando una cuenta, los datos también existen en cualquier copia de seguridad que se conserve. El derecho de supresión del RGPD se extiende a las copias de seguridad, salvo que su conservación la exija la ley o sea necesaria para la defensa jurídica.

Enfoques prácticos:

- **Copias de seguridad con límite de tiempo**: establecer una política de conservación de las copias de seguridad (p. ej., 90 días) para que los datos personales acaben purgándose automáticamente de las copias, aunque no puedan eliminarse a petición.
- **Copias de seguridad aisladas**: asegurarse de que las copias de seguridad nunca puedan restaurarse en una instancia de producción activa sin un procedimiento de recuperación deliberado, para que los datos eliminados no puedan reaparecer por accidente.
- **Copias de seguridad cifradas**: cifrar los soportes de las copias de seguridad para que los datos no puedan leerse si el soporte se pierde o se transfiere.

:::{note}
Eliminar los datos de un usuario concreto de una copia de seguridad existente es técnicamente complejo (a menudo poco práctico en copias de seguridad en cinta o basadas en instantáneas) y puede obligar a replantear la estrategia de copias de seguridad si se reciben con frecuencia solicitudes de supresión a gran escala.
:::

### Tabla resumen

| Categoría de datos | Clave de configuración | Conservación predeterminada | Mínimo recomendado |
|---|---|---|---|
| Papelera | `trashbin_retention_obligation` | 30 días (auto) | Establecer un máximo firme (p. ej., `auto, 60`) |
| Versiones de archivos | `versions_retention_obligation` | calendario automático | Establecer un máximo firme (p. ej., `auto, 180`) |
| Registro de actividad | `activity_expire_days` | 365 días | 90–180 días |
| Tokens de «Recordarme» | `remember_login_cookie_lifetime` | 15 días | 7–15 días |
````
