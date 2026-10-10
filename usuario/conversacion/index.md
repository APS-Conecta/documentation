---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Talk, la mensajería y las llamadas del establecimiento: cuándo está disponible, cómo se conectan las llamadas y las conversaciones de equipo."
---
# Conversación

## Resumen

**Talk** es la aplicación de mensajería y llamadas: chat, conversaciones de grupo, llamadas de audio y video y uso compartido de pantalla. Esta sección reúne el manual de Talk de la plataforma base y, al final, lo que APS Conecta Gestión fija para el establecimiento: cuándo está disponible Talk, cómo se conectan sus llamadas y para qué se usa.

````{upstream} user_manual/talk/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud Talk ofrece audio/video y chat de texto integrados en Nextcloud. Está disponible como interfaz web, cliente de escritorio y aplicaciones móviles para Android e iOS.

Hay más información sobre Nextcloud Talk [en su sitio web](https://nextcloud.com/talk/).
Los clientes de escritorio y móviles se descargan desde [nextcloud.com/install](https://nextcloud.com/install/).

- {nc-doc}`user_manual/talk/chat_index`
- {nc-doc}`user_manual/talk/conversation_index`
- {nc-doc}`user_manual/talk/call_index`
- {nc-doc}`user_manual/talk/federation_index`
- {nc-doc}`user_manual/talk/integrations_index`
- {nc-doc}`user_manual/talk/moderator_index`
- {nc-doc}`user_manual/talk/guest`
````

## En APS Conecta Gestión

### Disponibilidad

Talk es una opción de la instalación: la administración decide al instalar la suite si el establecimiento la incluye, y el instalador la deja apagada salvo que se active. Si **Talk** no aparece entre las aplicaciones, la instalación del establecimiento no la incluye.

La grabación de llamadas es una segunda opción de la instalación. Solo existe con Talk activado y también parte apagada; {doc}`/usuario/conversacion/call-recording` describe su uso.

### Cómo se conectan las llamadas

Con Talk activado, la instalación configura su propio servidor de señalización, el backend de alto rendimiento de Talk, y su propio servidor TURN y STUN. También retira el servidor STUN externo que Talk trae por omisión, así que las llamadas no consultan servidores ajenos a la instalación para conectarse.

### Uso en el establecimiento

Talk sirve para la coordinación interna del establecimiento, por ejemplo:

- la reunión breve de cada mañana del sector;
- la coordinación del triage entre SOME, los TENS de procedimientos y los médicos de urgencia;
- las consultas urgentes de farmacovigilancia entre Farmacia y los equipos de sector.

La plataforma es una intranet operativa, no una ficha clínica: los datos de pacientes no van en los mensajes.

Para abrir la conversación de un equipo del establecimiento:

1. Abrir la aplicación **Talk**.
2. Escribir el nombre del grupo en el campo **Buscar conversaciones o usuarios**, por ejemplo «Jefaturas» o «Sector Norte».
3. Hacer clic en el grupo en la lista de resultados.
4. Escribir el nombre de la conversación.
5. Hacer clic en **Crear conversación**.

Las conversaciones abiertas a todo el personal se encuentran con **Unirse a conversaciones abiertas**, como explica {doc}`/usuario/conversacion/open-conversations`.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
