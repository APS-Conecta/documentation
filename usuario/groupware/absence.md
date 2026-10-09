---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Configurar un mensaje de ausencia en los ajustes de Disponibilidad y cómo lo usan el estado de usuario, el calendario, Correo y Talk."
---
(nc-groupware-absence)=
# Configurar mensajes de ausencia

## Resumen

Esta página explica cómo añadir un mensaje de ausencia en la sección Ausencia de los ajustes de Disponibilidad y para qué se usan esos datos: el estado de usuario, el calendario personal, la respuesta automática de Correo y Talk. Está dirigida a usuarios que se ausentan por vacaciones, licencia médica o motivos similares.

````{upstream} user_manual/groupware/absence.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Si se va a estar ausente por vacaciones, licencia médica o algo similar, se puede añadir un mensaje de ausencia en la sección **Ausencia** de los ajustes de **Disponibilidad**.

La interfaz pide el periodo de ausencia, un mensaje corto y uno largo, y un usuario sustituto opcional. Estos datos se usan para los siguientes fines:

1. El estado de usuario cambiará al mensaje corto cuando comience la ausencia y se restablecerá cuando termine.
2. Se creará un evento con el estado *ocupado* en el calendario personal. Esto permite que otras personas vean que no se está disponible cuando usan la función de disponibilidad libre/ocupado.
3. Si se ha habilitado, la aplicación Correo aplicará una respuesta automática con el mensaje largo.
4. La aplicación Talk mostrará a otras personas el mensaje largo de ausencia cuando intenten comunicarse con la persona ausente en un chat 1:1 durante la ausencia, así como el usuario sustituto, si se ha definido.
````
