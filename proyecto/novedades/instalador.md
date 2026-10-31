---
tipo: referencia
audiencia: proyecto
apps: [gestion, files-upload-guard]
resumen: "Cambios de instalador visibles para usuarios y administradores, agrupados por versión."
---
# Novedades de instalador

## Resumen

Esta página registra los cambios de instalador que ve una persona usuaria o administradora, agrupados por versión. 📚 Scribe la actualiza cada día a partir de los cambios fusionados en el repositorio; los cambios internos no figuran. Los cambios aún no publicados aparecen como «Próxima versión».

## Tabla

| Versión | Fecha | Cambio |
|---|---|---|
| Próxima versión |  | La instalación reconoce manifiestos Docker y OCI al consultar las imágenes publicadas de la suite. |
| Próxima versión |  | AppAPI verifica su servicio HaRP predeterminado y su comunicación HTTPS con la suite por IP. La revalidación incluye ambas conexiones después de reiniciar o repetir el aprovisionamiento. |
| Próxima versión |  | El antivirus analiza las cargas antes de guardarlas y aplica un límite común al archivo completo. Una sustitución rechazada conserva el archivo anterior; los errores indican revisar el resultado, el contenido o el servicio antes de repetir la carga. |
| Próxima versión |  | Nextcloud y el servidor web validan las direcciones reenviadas mediante la subred interna real. Los registros y la protección de acceso conservan la dirección del cliente de la LAN. |
| Próxima versión |  | La instalación informa el resultado final del asistente, continúa mientras existan avances y recupera una sesión vencida una vez. Una interrupción de conexión indica revisar el estado antes de iniciar otra vez. |
| Próxima versión |  | La preparación conserva los servidores DNS del anfitrión y admite una interfaz LAN tardía. Las herramientas requeridas se instalan por separado del verificador de firma opcional. |
| Próxima versión |  | Una línea de consola instala la suite: descarga el paquete de la versión, verifica su suma sha256 y su firma, y deja lista la orden `sudo aps-conecta install`. |
| Próxima versión |  | La instalación silenciosa termina importando los datos comunales del centro; importar de nuevo no crea nada («0 creados»). |
| Próxima versión |  | El paso 7 del asistente ofrece, con consentimiento explícito («Sí, corregir»), arreglar la red del servidor cuando el dominio no responde desde el propio servidor. |
| Próxima versión |  | La revisión previa informa dos niveles de recursos —mínimo y recomendado— para memoria y disco. |
| Próxima versión |  | La revisión previa instala lo que falte —Docker, signify, gdal—, verifica el paquete guardado sin red y nombra lo que corrigió. |
| Próxima versión |  | La suite usa Euro-Office como único editor y mantiene sus aplicaciones habilitadas durante una demora del servicio. La configuración se completa en el siguiente inicio. |
| Próxima versión |  | El conjunto fijo incluye Talk, búsqueda, vistas previas, antivirus y AppAPI mediante HaRP. Farmacia, Estadística y Tótem conservan su selección. |
| Próxima versión |  | La instalación configura la búsqueda dentro de documentos, incorpora sus tres aplicaciones y prepara los ajustes de memoria del servidor. La aceptación busca el contenido de un archivo cargado por una cuenta sin privilegios. |
| Próxima versión |  | Cada construcción produce el conjunto completo de imágenes desde un commit y verifica su procedencia y resúmenes. |
| Próxima versión |  | La publicación ejecuta las compuertas completas, verifica el contenido firmado y protege las credenciales en el entorno `Release`. |
| Próxima versión |  | Las actualizaciones siguen el procedimiento de la suite y el establecimiento aporta su dominio o IP. |
| Próxima versión |  | El banco de pruebas y la aceptación del ciclo de vida usan la instalación HTTPS por IP, con el certificado y el comando del instalador. La revisión de puertos considera TCP y UDP y admite el puerto 80 ocupado. |
| Próxima versión |  | La revisión previa exige x86-64, FUSE y Docker Engine compatible, mide el disco de datos real y detecta contenedores sin su carpeta de instalación. Las indicaciones del cortafuegos usan las subredes reales de la suite. |
| Próxima versión |  | La instalación conserva el proxy institucional para las descargas, Docker, el asistente y la plataforma. El perfil mantiene sus credenciales privadas y excluye la comunicación interna. |
| Próxima versión |  | El aprovisionamiento aplica el nombre del establecimiento en el tema en uso y lo conserva al reiniciar. |

## Notas

El [plan de gestion #175](https://github.com/APS-Conecta/gestion/issues/175) registra la implementación y sus verificaciones. La configuración de Talk durante el aprovisionamiento y el perfil de grabación continúan en etapas posteriores.

Estas entradas describen la próxima versión. Para instalar, seleccione una versión estable en [Publicaciones de la suite](https://github.com/APS-Conecta/gestion/releases).
