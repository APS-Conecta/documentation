---
tipo: explicacion
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Qué son los ajustes predefinidos de conversación de Talk y cómo funcionan los de sala de voz, seminario web y presentación."
---
# Ajustes predefinidos de conversación

## Resumen

Esta página explica a las personas usuarias de Talk qué son los ajustes predefinidos de conversación que define la administración y qué hace cada uno: sala de voz, seminario web y presentación.

````{upstream} user_manual/talk/conversation_presets.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los ajustes predefinidos de conversación permiten a los administradores definir plantillas para las conversaciones nuevas, con ajustes preconfigurados como los permisos, las reglas de la sala de espera y el tipo de conversación.

### Ajustes predefinidos disponibles

Según la configuración de la instancia, es posible que aparezcan ajustes predefinidos al crear una conversación nueva. Cada uno aplica un conjunto concreto de valores predeterminados adecuado para un caso de uso particular.

### Sala de voz

Una sala de llamada permanente («Sala de voz») es un ajuste predefinido de conversación optimizado para reuniones no obligatorias y siempre disponibles. Cualquier persona que entre en la conversación se une a la llamada que hay en ella, lo que facilita empezar a comunicarse. Los mensajes de una conversación de sala de voz están configurados para caducar después de cierto tiempo, para mantenerla ligera y espontánea.

### Seminario web

Los moderadores pueden configurar un ajuste predefinido para forzar la sala de espera, de modo que los participantes esperen a un moderador antes de unirse. Cuando una conversación usa un ajuste predefinido con sala de espera forzada:

- Los participantes ven una sala de espera al unirse
- Un moderador debe admitirlos en la conversación o retirar la sala de espera
- Es útil para seminarios web, entrevistas o reuniones controladas

### Presentación

El ajuste predefinido Presentación es útil para reuniones internas en las que se espera que haya más oyentes que oradores. Los permisos de los participantes están optimizados para garantizar el mejor rendimiento y la mejor experiencia de moderación, de modo que los presentadores puedan hablar sin interrupciones.

Véase también:

- {nc-doc}`Conversaciones <user_manual/talk/conversations>`
- {nc-doc}`Seminario web y sala de espera <user_manual/talk/webinar>`
- {nc-doc}`Conversaciones abiertas <user_manual/talk/open_conversations>`
````
