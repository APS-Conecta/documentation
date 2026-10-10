---
tipo: referencia
audiencia: proyecto
apps: [gestion]
resumen: "Cambios de gestion visibles para usuarios y administradores, agrupados por versión."
---
# Novedades de gestion

## Resumen

Esta página registra los cambios de gestion que ve una persona usuaria o administradora, agrupados por versión. 📚 Scribe la actualiza cada día a partir de los cambios fusionados en el repositorio; los cambios internos no figuran. Los cambios aún no publicados aparecen como «Próxima versión». El historial anterior a la última versión publicada antes del 9 de octubre de 2026 está en el registro de cambios del repositorio, en inglés.

## Tabla

| Versión | Fecha | Cambio |
|---|---|---|
| Próxima versión |  | «Elegir el centro» abre sobre el mapa en el punto oficial del establecimiento, que se confirma o se mueve antes de «Confirmar centro»; «Punto oficial» lo restablece. |
| Próxima versión |  | La suite sirve el mapa en su propia ruta `/tiles/`, sin un contenedor de mapas aparte. |
| Próxima versión |  | La suite se instala por IP sobre HTTPS, y al terminar nombra el certificado que importa cada equipo del personal, con su huella SHA-256. |
| Próxima versión |  | El respaldo diario corre a las 04:00 hora de Santiago, la comprobación de contraseñas filtradas queda desactivada y Talk se instala solo cuando la suite lo tiene activado. |
| Próxima versión |  | El paso «Iniciar la suite» indica si Talk cabe en el servidor y, con «Preparar el asistente», deja prellenado el asistente de la suite. |
| Próxima versión |  | La pantalla «Revisar y ejecutar» presenta el plan en términos del centro, incluida la ubicación, y sigue la ejecución en vivo hasta el resultado. |
| Próxima versión |  | La pantalla «Cargar equipos y personas» reúne sectores, programas y la planilla del personal, y ofrece «Descargar plantilla» con una planilla preparada para el centro. |
| Próxima versión |  | La pantalla «Elegir el centro» busca el establecimiento en todo el registro DEIS, con filtros por región, comuna y tipo de centro. |
| Próxima versión |  | La instalación continúa en el navegador mediante un enlace HTTPS único que entrega `sudo aps-conecta abrir`. |
| Próxima versión |  | `aps-conecta estado` muestra, sin sudo, el último resultado de la re-provisión con el arreglo de cada punto, y cada administrador recibe una notificación cuando la re-provisión semanal no termina bien. |
| Próxima versión |  | `sudo aps-conecta temporizadores` instala la re-provisión semanal (domingos a las 03:00) y el mapa mensual (día 4 a las 05:00), ambos en hora de Santiago. |
| Próxima versión |  | `sudo aps-conecta install --sitio S --planilla P` realiza la misma instalación sin preguntas ni navegador. |
| Próxima versión |  | Cada cuenta de cargo recibe su propia contraseña inicial, sellada en `credentials.txt`. |
| Próxima versión |  | En un servidor Ubuntu o Debian recién instalado, `sudo aps-conecta install` prepara Docker y descarga y verifica la suite. |
| Próxima versión |  | `sudo aps-conecta install` abre con una bienvenida y recorre nueve pasos numerados. |
| Próxima versión |  | Estadística forma parte de las aplicaciones de la suite. |
| Próxima versión |  | La carpeta de contenidos de la intranet se llama «Intranet» en Archivos. |
