---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Añadir un recurso DAV groupware en KOrganizer o Kalendar para sincronizar calendarios, contactos y tareas con KDE Kontact."
---
# Sincronizar con KDE Kontact

## Resumen

Esta página explica, paso a paso, cómo añadir en KOrganizer o Kalendar un recurso DAV groupware que sincroniza calendarios, contactos y tareas con las aplicaciones de KDE Kontact y el applet de calendario de Plasma. Está dirigida a usuarios del escritorio KDE.

````{upstream} user_manual/groupware/sync_kde.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
KOrganizer, Kalendar y KAddressBook pueden sincronizar su calendario, contactos y tareas con un servidor Nextcloud.

Puede seguir los pasos a continuación para KOrganizer y Kalendar:

En KOrganizer:

1. Abra KOrganizer y, en la lista **Calendario** de la izquierda, haga clic con el botón derecho y elija `Add Calendar`.

2. En la lista que se muestra, elija `Recurso compartido DAV`.

En Kalendar:

1. Abra Kalendar y, en la barra de menú, abra Ajustes y a continuación pulse en `Fuentes de calendario` -> `Añadir Calendario`.

2. En la lista que se muestra, elija `Recurso compartido DAV`.

En KOrganizer y Kalendar:

3. Introduzca su nombre de usuario. Como contraseña, necesita generar una contraseña/token de aplicación ({nc-ref}`Más información <managing_devices>`).

4. Elija `Nextcloud` como opción de servidor Groupware.

5. Introduzca la URL de su servidor Nextcloud y, si es necesario, la ruta de instalación (todo lo que viene después de la primera /, por ejemplo `mynextcloud` en `https://example.com/mynextcloud`). Luego pulse siguiente.

6. Ya puede probar la conexión, que puede tardar un poco al ser la primera. Si no funciona, puede volver atrás y cambiar los ajustes.

7. Elija un nombre para el recurso, por ejemplo `Trabajo` o `Casa`. Por defecto, se sincroniza tanto CalDAV (calendarios) como CardDAV (contactos).

:::{note}
Puede establecer una frecuencia de actualización manual para sus recursos de calendario y contactos. De forma predeterminada, este ajuste es de 5 minutos, lo que debería bastar para la mayoría de los casos de uso. Cuando crea una cita nueva, se sincroniza con Nextcloud de inmediato. Puede que desee cambiar esto para ahorrar energía o su plan de datos móviles, de modo que pueda actualizar con un clic derecho sobre el elemento en la lista de calendarios.
:::

8. Pasado unos segundos o minutos, en función de su conexión a internet, sus calendarios y contactos aparecerán en las aplicaciones de KDE KOrganizer, Kalendar y KAdressBook, así como en la applet de calendario para Plasma.
````
