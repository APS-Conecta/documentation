---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Apps que ayudan a cumplir el RGPD: aviso legal de la app Tema, Drop Account y Data Request, y cómo atender las solicitudes que llegan."
---
# Apps útiles

## Resumen

Esta página explica cómo configurar el aviso legal y la política de privacidad con la app Tema, cómo instalar las apps Drop Account y Data Request, y cómo atender las solicitudes de exportación y de eliminación que llegan por correo electrónico. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/gdpr/helpful_apps.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
En la tienda de apps de {vendor}`Nextcloud` hay varias apps disponibles que ayudan a cumplir obligaciones concretas del RGPD.

### Aviso legal (app Tema)

El **derecho a la información** (artículos 13 y 14 del RGPD) exige poner la política de privacidad al alcance de los usuarios. La app Tema integrada incluye una función de **aviso legal** que permite añadir enlaces al aviso legal y a la política de privacidad en la pantalla de inicio de sesión de Nextcloud y en el pie de página.

Para configurarla:

1. Ir a **Configuraciones de administración → Tema**.
2. Rellenar los campos **URL del aviso legal** y **URL de la política de privacidad**.
3. Guardar. Los enlaces aparecen en la página de inicio de sesión y en el pie de página de la interfaz web.

Así se garantiza que todos los usuarios, incluidos quienes acceden mediante enlaces de recursos compartidos públicos, puedan encontrar la política de privacidad sin necesidad de iniciar sesión.

### App Drop Account

La [app Drop Account](https://apps.nextcloud.com/apps/drop_account) permite a los usuarios eliminar su propia cuenta de Nextcloud directamente desde Ajustes personales, sin necesidad de contactar con un administrador.

Instalarla desde la página Apps o mediante occ:

```
sudo -E -u www-data php occ app:install drop_account
```

Una vez instalada, los usuarios ven un botón **Eliminar cuenta** en **Ajustes personales → Información personal**. Deben confirmar su contraseña antes de que se lleve a cabo la eliminación.

:::{warning}
La eliminación de la cuenta mediante esta app también elimina todos los archivos del usuario. Asegurarse de que los usuarios lo sepan antes de continuar. Considerar añadir una nota en la política de privacidad que explique qué se elimina y qué no (consultar {nc-doc}`admin_manual/gdpr/subject_rights` para ver la lista completa de lo que `user:delete` limpia y lo que no, incluidas las tablas de comentarios, que requieren una limpieza manual).
:::

### App Data Request

La [app Data Request](https://apps.nextcloud.com/apps/data_request) ofrece a los usuarios una forma de autoservicio para ejercer sus derechos del RGPD directamente desde sus Ajustes personales, sin necesidad de contactar con un administrador por correo electrónico o por un canal externo.

Una vez instalada, aparecen dos botones en la página **Ajustes personales → Información personal** de cada usuario:

- **Solicitar la exportación de datos**: envía un correo electrónico a todos los administradores para avisarles de que el usuario solicita una copia de sus datos.
- **Solicitar la eliminación de la cuenta**: envía un correo electrónico a todos los administradores para avisarles de que el usuario quiere que se elimine su cuenta.

Ambas acciones requieren que el usuario confirme su contraseña y están limitadas a una solicitud por acción y por hora.

La app es solo un puente de notificación. No realiza la exportación ni la eliminación automáticamente: los administradores deben atender cada solicitud manualmente siguiendo los pasos descritos en {nc-doc}`admin_manual/gdpr/subject_rights`.

:::{note}
Los administradores reciben la notificación en la dirección de correo electrónico configurada en su cuenta. Asegurarse de que todas las cuentas de administrador tengan establecida una dirección de correo electrónico válida; de lo contrario, las notificaciones se descartarán sin aviso.
:::

Instalarla desde la página Apps o mediante occ:

```
sudo -E -u www-data php occ app:install data_request
```

No se requiere ninguna configuración adicional después de la instalación.

**Gestión de las solicitudes entrantes**

Cuando llega un correo de solicitud:

*Para una solicitud de exportación de datos:*

1. Exportar los archivos del usuario mediante WebDAV, o pedir al usuario que use el botón **Descargar sus datos** de sus Ajustes personales.
2. Exportar los contactos y los calendarios desde las apps Contactos y Calendario, o usar `occ dav:export-calendar`.
3. Entregar al usuario los datos exportados de forma segura.

*Para una solicitud de eliminación de la cuenta:*

1. Opcionalmente, transferir la propiedad de los archivos antes de la eliminación:

   ```
   sudo -E -u www-data php occ files:transfer-ownership <uid> <new-owner>
   ```

2. Eliminar la cuenta:

   ```
   sudo -E -u www-data php occ user:delete <uid>
   ```

Consultar {nc-doc}`admin_manual/gdpr/subject_rights` para ver todos los detalles de lo que elimina cada operación y de los datos que pueden quedar después de la eliminación.
````
