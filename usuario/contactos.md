---
tipo: guia
esqueleto: borrador
audiencia: usuario
apps: [gestion]
resumen: "El directorio del personal del establecimiento en la aplicación Contactos."
---
# Contactos

## Resumen

La aplicación Contactos mantiene el directorio del personal del establecimiento: cada cuenta activa aparece con su nombre, rol clínico y sector. El directorio se busca por rol, anexo telefónico o unidad, y desde cada tarjeta se puede iniciar una conversación en Talk o agendar una reunión.

## Secciones previstas

- Directorio del personal
- Búsqueda por rol y unidad
- Comunicación directa

````{upstream} user_manual/groupware/contacts.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La aplicación Contactos no está habilitada de forma predeterminada en Nextcloud 34 y debe instalarse por separado desde nuestra tienda de aplicaciones.

La aplicación Contactos de Nextcloud es similar a otras aplicaciones de contactos para móviles, pero con más funciones. Esta sección cubre las funciones básicas que ayudan a mantener la libreta de direcciones en la aplicación.

A continuación se explica cómo añadir contactos, editarlos o eliminarlos, subir una foto de contacto y gestionar las libretas de direcciones.

### Añadir contactos

Al acceder por primera vez a la aplicación Contactos, quedan disponibles la libreta de direcciones del sistema, que contiene todos los usuarios de la instancia que se tiene permitido ver, y una libreta de direcciones predeterminada vacía.

Para añadir contactos a la libreta de direcciones, se puede usar uno de los siguientes métodos:

- Importar contactos con un archivo de contacto virtual (VCF/vCard)
- Añadir contactos manualmente

La forma más rápida de añadir un contacto es usar un archivo de contacto virtual (VCF/vCard).

#### Importar contactos virtuales

Para importar contactos con un archivo VCF/vCard:

1. Cuando aún no hay contactos, se muestra un botón **Importar contactos**.
2. Buscar "Ajustes" en la parte inferior de la barra lateral izquierda, junto al botón del engranaje.
3. Hacer clic en el botón del engranaje. Aparecerá el botón "Importar" de la aplicación Contactos.

:::{note}
La aplicación Contactos solo admite la importación de vCards de las versiones 3.0 y 4.0.
:::

4. Hacer clic en el botón "Importar" y subir el archivo VCF/vCard.

Una vez completada la importación, el nuevo contacto aparecerá en la libreta de direcciones.

#### Añadir contactos manualmente

Si no se pueden importar contactos virtuales, la aplicación Contactos permite **añadir contactos** manualmente.

Para crear un contacto nuevo:

1. Hacer clic en el botón `+ New contact`.

   La configuración de la vista de edición se abre en el campo de vista de la aplicación.

2. Especificar la información del nuevo contacto y luego hacer clic en Guardar.
3. Se mostrará el modo de vista con los datos añadidos

#### Editar o eliminar información de contacto

La aplicación Contactos permite editar o eliminar la información de los contactos.

Para editar o eliminar información de contacto:

1. Ir al contacto concreto que se desea modificar.
2. Seleccionar la información del campo que se desea editar o eliminar.
3. Hacer las modificaciones o hacer clic en la papelera.

Los cambios o eliminaciones hechos en la información de cualquier contacto se aplican de inmediato.

No todos los contactos serán editables. La libreta de direcciones del sistema no permite modificar los datos de otras personas, solo los propios. Los datos propios también se pueden modificar en los {nc-doc}`ajustes de usuario <user_manual/userpreferences>`.

#### Foto de contacto

Para añadir una foto a los contactos nuevos, hacer clic en el botón de subida.

Una vez establecida la foto de contacto, se verá así. La imagen muestra la foto de contacto ya establecida.

Para subir una nueva, quitarla, verla a tamaño completo o descargarla, hacer clic en la foto del contacto para que aparezcan esas opciones.

Si el administrador permite las actualizaciones desde redes sociales en los ajustes de groupware de administración, los usuarios también pueden obtener fotos de contacto directamente desde redes sociales. En ese caso, el contacto debe tener guardado un nombre de usuario en la sección de redes sociales. Cada entrada de una red social compatible añade una entrada de descarga para esa red. Actualmente se admiten las siguientes redes sociales:

- Instagram
- Mastodon
- Tumblr
- Diaspora
- Xing
- Telegram
- Gravatar

Los avatares sociales solo se obtienen si están disponibles públicamente sin iniciar sesión en la red social correspondiente. En los ajustes de usuario de contactos, en la página de contactos, se pueden activar las actualizaciones automáticas desde redes sociales. Esto actualizará los avatares con los datos del perfil social una vez por semana. Las redes sociales se consultan en el orden indicado arriba.

### Gestionar varios contactos a la vez

La aplicación Contactos permite seleccionar varios contactos y realizar acciones en lote sobre ellos. Para seleccionar varios contactos, hacer clic en la foto de perfil de cada contacto por separado, o hacer clic en la foto de perfil del primer contacto y luego, manteniendo pulsada la tecla Mayús, hacer clic en otro contacto de la lista para seleccionar todos los contactos que hay entre el primero y el segundo.

Esto muestra un menú en la parte superior de la lista de contactos con varias acciones que se pueden realizar sobre los contactos seleccionados.

En el modo por lotes, el botón con el icono de cruz deselecciona todos los contactos seleccionados, mientras que el botón con el icono de papelera elimina todos los contactos seleccionados.

:::{note}
Es posible que no se puedan modificar o eliminar ciertos contactos, por ejemplo, si están en una libreta de direcciones de solo lectura. En ese caso, las acciones correspondientes estarán deshabilitadas.
:::

#### Combinar contactos duplicados

Para combinar contactos, seleccionar dos contactos y hacer clic en el botón con el icono "Combinar contactos" en la parte superior de la lista de contactos; se abrirá un diálogo que ayuda a combinar contactos duplicados. El diálogo de combinación muestra los detalles de ambos contactos lado a lado, y se puede elegir qué detalles conservar en el contacto combinado.

Las propiedades con un botón de opción (circular) solo pueden tener un valor, así que se debe seleccionar uno de los dos valores (como el nombre del contacto, que solo puede tener un valor); en cambio, las casillas de verificación (botones cuadrados) permiten conservar ambos valores si se desea (como los números de teléfono o las direcciones de correo electrónico, que pueden tener varios valores).

Si alguno de los contactos forma parte de uno o varios grupos, de forma predeterminada el contacto combinado formará parte de todos los grupos a los que pertenecían los dos contactos. Se puede desmarcar cualquier grupo durante la combinación si no se desea que el contacto combinado forme parte de él.

:::{note}
Actualmente solo se pueden combinar dos contactos a la vez y, naturalmente, solo se pueden combinar contactos que uno mismo puede modificar. Si la acción de combinar está deshabilitada, comprobar que los contactos seleccionados cumplen esas condiciones.
:::

### Organizar los contactos con grupos de contactos

Los grupos de contactos ayudan a organizar los contactos en grupos.

Para crear un grupo de contactos nuevo, hacer clic en el signo más junto a "Grupos de contactos" en la barra lateral izquierda.

:::{note}
Los grupos de contactos deben tener al menos un miembro para guardarse. Tener en cuenta que a los grupos de contactos solo se pueden añadir contactos de libretas de direcciones con permiso de escritura. Los contactos de libretas de direcciones de solo lectura, como la libreta de direcciones del sistema, no se pueden añadir.
:::

### Añadir y gestionar libretas de direcciones

Al hacer clic en el botón "Ajustes" (engranaje) en la parte inferior de la barra lateral izquierda, se accede a los ajustes de la aplicación Contactos. Este campo muestra todas las libretas de direcciones disponibles y ciertas opciones para cada una, y permite crear libretas de direcciones nuevas con solo indicar su nombre.

En los ajustes de Contactos también se pueden compartir, exportar y eliminar libretas de direcciones. Allí se encuentran las URL de CardDAV.

:::{note}
Los contactos de las libretas de direcciones deshabilitadas no se muestran en la aplicación Contactos ni en el menú de contactos.
:::

Consultar {nc-doc}`Groupware <user_manual/groupware/index>` para obtener más detalles sobre la sincronización de las libretas de direcciones con iOS, macOS, Thunderbird y otros clientes CardDAV.

### Equipos

En las organizaciones se da la colaboración informal: un evento que organizar durante unas semanas, una breve sesión de ideación entre miembros de distintas entidades, talleres, un espacio para bromear y fomentar el espíritu de equipo, o simplemente organizaciones muy orgánicas en las que la estructura formal se mantiene al mínimo.

Por todas estas razones, Nextcloud admite Equipos, una función integrada en la aplicación Contactos con la que cada usuario puede crear su propio equipo, un agregado de cuentas definido por el usuario. Luego, los equipos se pueden usar para compartir archivos y carpetas, o añadirse a conversaciones de Talk, como un grupo normal.

#### Crear un equipo

En el menú izquierdo, hacer clic en el + junto a Equipos. Asignar un nombre al equipo. Al llegar a la pantalla de configuración del equipo, se puede:

- añadir miembros al equipo
- hacer clic en el menú de tres puntos junto a un usuario para modificar su rol dentro del equipo.

#### Roles del equipo

Los equipos admiten 4 tipos de roles:

- Miembro
- Moderador
- Administrador: puede configurar las opciones del equipo (+permisos de moderador)
- Propietario

**Miembro**

Miembro es el rol con menos permisos. Un miembro solo puede acceder a los recursos compartidos con el equipo y ver a los miembros del equipo.

**Moderador**

Además de los permisos de miembro, un moderador puede invitar, confirmar invitaciones y gestionar a los miembros del equipo.

**Administrador**

Además de los permisos de moderador, un administrador puede configurar las opciones del equipo.

**Propietario**

Además de los permisos de administrador, un propietario puede transferir la propiedad del equipo a otro miembro del equipo. Solo puede haber un único propietario por equipo.

#### Añadir miembros a un equipo

Se pueden añadir como miembros de un equipo cuentas locales, grupos, direcciones de correo electrónico u otros equipos. En el caso de un grupo o un equipo, el rol se aplica a todos los miembros del grupo o equipo.

#### Opciones del equipo

Hay varias opciones, que se explican por sí solas, para configurar un equipo: gestionar las invitaciones y la membresía, la visibilidad del equipo, si se permite la membresía en otros equipos y la protección con contraseña.

**Evitar que los equipos sean miembros de otros equipos**

Cuando esta opción está habilitada, el equipo ya no puede añadirse directamente como miembro de otro equipo. Sin embargo, esta restricción solo se aplica a las nuevas adiciones directas. Las membresías existentes se mantienen, y las membresías heredadas siguen siendo posibles si este equipo pertenece a un equipo padre que se añade en otro lugar.

#### Elementos compartidos

:::{versionadded} 5.5 Nextcloud 25 o posterior
:::

Los elementos compartidos entre dos contactos se mostrarán en la aplicación de contactos. Esto incluye archivos multimedia, eventos de calendario, salas de chat y tarjetas de Deck compartidas, todo lo cual será visible en los detalles del contacto. Esta función se limita a los contactos que figuran en la libreta de direcciones del sistema. Actualmente, nuestro sistema solo admite elementos compartidos entre dos contactos.
````
