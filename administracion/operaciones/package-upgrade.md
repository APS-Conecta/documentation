---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El snap de Nextcloud: instalación, primer inicio de sesión y actualización o reversión con snap refresh y snap revert."
---
# Actualizar con paquetes snap

## Resumen

Esta página presenta el snap no oficial de Nextcloud: cómo instalarlo, el primer inicio de sesión y cómo actualizarlo manualmente o volver a la última versión que funcionaba. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/maintenance/package_upgrade.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Inicio rápido de la actualización

El snap de Nextcloud es un Nextcloud no oficial diseñado para ser fácil de instalar y sencillo de mantener. El snap de Nextcloud ideal es una instancia de Nextcloud de tipo «instalar y olvidar» que funciona en la mayoría de las arquitecturas y se actualiza sola sin necesidad de conocimientos de administración. Combinar Nextcloud con snapd lo convierte en una opción perfecta para entornos IoT o escalables. Snapd es una tecnología segura y robusta que el equipo del snap de Nextcloud ha adoptado.

Sin embargo, el snap impone sus propias decisiones.

- El snap de Nextcloud usa el Apache recomendado.
- El snap de Nextcloud usa el MySQL recomendado.
- El snap de Nextcloud usa el PHP recomendado.

### Instalación

**En Ubuntu**

- <https://snapcraft.io/nextcloud>
- Instalar Nextcloud `sudo snap install nextcloud`

**Todas las demás distribuciones**
[atención](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Why-Ubuntu-is-the-only-supported-distro/)

De forma predeterminada se instala la última versión estable del snap de Nextcloud, que se actualizará automáticamente a las versiones estables posteriores, pero también hay [otras versiones disponibles](https://github.com/nextcloud/nextcloud-snap/wiki/Release-strategy) y se tiene control total de las [actualizaciones automáticas](https://github.com/nextcloud-snap/nextcloud-snap/wiki/Managing-automatic-updates).

Tras la instalación, Nextcloud se iniciará automáticamente. Suponiendo que se está en la misma red que el dispositivo en el que se instaló, se llega a la instalación de Nextcloud visitando `<hostname>.local` o la dirección IP de la instancia en el navegador. Si el nombre de host es `localhost` o `localhost.localdomain`, como en un dispositivo Ubuntu Core, se usará `nextcloud.local` en su lugar.

### Primer inicio de sesión

Al visitar la instalación de Nextcloud por primera vez, se pedirá introducir un nombre de usuario y una contraseña de administrador antes de que Nextcloud se inicialice. Esto puede tardar un poco según los recursos y el dispositivo. Tras proporcionar esa información, se habrá iniciado sesión y podrán instalarse apps, crearse usuarios y subirse archivos.

### Consejos de actualización

De forma predeterminada, el snap de Nextcloud se actualiza automáticamente a las versiones estables posteriores. Sin embargo, también puede actualizarse manualmente con el comando:

`sudo snap refresh nextcloud`

Si la actualización falla, puede volverse fácilmente a la última versión que funcionaba con el comando:

`sudo snap revert nextcloud`

Hay más documentación, una [extensa wiki](https://github.com/nextcloud-snap/nextcloud-snap/wiki) y [preguntas frecuentes](https://github.com/nextcloud-snap/nextcloud-snap/wiki/FAQ's) en el [GitHub de los desarrolladores](https://github.com/nextcloud-snap/nextcloud-snap).
````
