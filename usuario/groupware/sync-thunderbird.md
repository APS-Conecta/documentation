---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Sincronizar contactos y calendarios con Thunderbird mediante CardDAV y CalDAV nativos, o los contactos con el complemento CardBook."
---
# Sincronizar con Thunderbird

## Resumen

Esta página explica cómo sincronizar contactos y calendarios con Thunderbird mediante su soporte nativo de CardDAV y CalDAV y, como alternativa solo para los contactos, con el complemento CardBook. Está dirigida a usuarios de Thunderbird.

````{upstream} user_manual/groupware/sync_thunderbird.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
[Thunderbird](https://www.thunderbird.net) es un cliente de correo maduro y con muchas funciones que puede convertirse en un gestor de información personal (PIM) completo. Desde la versión 102, admite la sincronización de libretas de direcciones mediante CardDAV y el descubrimiento automático de los calendarios y las libretas de direcciones disponibles en el servidor.

### Método recomendado

Desde Thunderbird 102, los protocolos CardDAV y CalDAV son compatibles de forma nativa.

#### Contactos

1. En la vista de libretas de direcciones, hacer clic en la flecha hacia abajo junto a **Nueva libreta de direcciones** y elegir **Añadir libreta de direcciones CardDAV**.
2. En la ventana siguiente, escribir el **Nombre de usuario** y la **Ubicación** (URL del servidor).
3. La ventana siguiente pedirá el nombre de usuario y la contraseña de esta cuenta.
4. La ventana anterior se actualizará y preguntará qué libretas de direcciones se desea sincronizar.
5. Elegirlas y, a continuación, hacer clic en **Continuar**.

Si más adelante se desea añadir una nueva libreta de direcciones, se pueden repetir todos estos pasos y solo se sugerirán las libretas que aún no estén sincronizadas.

:::{note}
Si la cuenta usa autenticación de dos factores, para iniciar sesión se necesita una {nc-ref}`contraseña de aplicación dedicada <managing_devices>` en lugar de la contraseña habitual.
:::

#### Calendarios

1. Ir a la vista de calendario de Thunderbird y seleccionar el botón **Nuevo calendario...** en la parte inferior del panel lateral izquierdo.
2. Elegir **En la red**:

   La imagen muestra el diálogo de nuevo calendario de Thunderbird con la opción **En la red** seleccionada.

3. Escribir el **Nombre de usuario** y la **Ubicación** (URL del servidor) y, a continuación, hacer clic en **Buscar calendarios**.
4. Elegir los calendarios que se desea añadir y hacer clic en **Suscribirse**.

Aquí ocurre lo mismo: si más adelante se desea añadir más calendarios, basta con repetir el procedimiento.

### Alternativa: usar el complemento CardBook (solo contactos)

[CardBook](https://addons.thunderbird.net/en/thunderbird/addon/cardbook/) es una alternativa avanzada a la libreta de direcciones de Thunderbird, compatible con CardDAV.

1. Hacer clic en el icono de CardBook en la esquina superior derecha de Thunderbird:

   La imagen muestra el icono de CardBook en la barra de herramientas de Thunderbird.

2. En CardBook:

   - Ir a Libreta de direcciones > Nueva libreta de direcciones **Remota** > Siguiente
   - Seleccionar **CardDAV** y rellenar la dirección del servidor Nextcloud, el nombre de usuario y la contraseña

3. Hacer clic en «Validar», hacer clic en Siguiente y, a continuación, elegir el nombre de la libreta de direcciones y volver a hacer clic en Siguiente:

   La imagen muestra el diálogo de CardBook para introducir el nombre de la nueva libreta de direcciones.

4. Al terminar, CardBook sincroniza las libretas de direcciones. Siempre es posible lanzar una sincronización manual haciendo clic en el botón **Sincronizar** de CardBook:

   La imagen muestra la vista de libretas de direcciones de CardBook con el botón **Sincronizar**.
````
