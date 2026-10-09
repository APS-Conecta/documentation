---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Instalar Collabora Online (coolwsd) en Ubuntu 24.04 desde sus paquetes: claves de firma, repositorio, paquetes y configuración básica."
---
# Ejemplo de instalación en Ubuntu 24.04

## Resumen

Esta página muestra los comandos para instalar el servicio Collabora Online (coolwsd) en Ubuntu 24.04 desde el repositorio de paquetes de Collabora y hacer su configuración básica (SSL, terminación SSL, host WOPI y contraseña de administración) antes de configurar un proxy inverso. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/example-ubuntu.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

### Importar las claves de firma:

```bash
cd /usr/share/keyrings && sudo wget https://collaboraoffice.com/downloads/gpg/collaboraonline-release-keyring.gpg
```

### Añadir el repositorio:

```bash
sudo echo -e "Types: deb\nURIs: https://www.collaboraoffice.com/repos/CollaboraOnline/CODE-deb\nSuites: ./\nSigned-By: /usr/share/keyrings/collaboraonline-release-keyring.gpg" > /etc/apt/sources.list.d/collaboraonline.sources
```

### Instalar los paquetes

```bash
sudo apt update && sudo apt install coolwsd code-brand
```

### Configuración

Editar /etc/coolwsd/coolwsd.xml. El servicio Collabora Online (coolwsd) se ejecuta mediante systemd. Después de editar el archivo de configuración, hay que reiniciar el servicio:

```bash
sudo systemctl restart coolwsd
```

La configuración predeterminada busca un certificado SSL y una clave, que no están presentes, así que probablemente lo mejor sea desactivar SSL y, opcionalmente, activar la terminación SSL, y después configurar el proxy inverso.

:::{seealso}
Los ejemplos de configuración completos para el proxy inverso se encuentran en la documentación de Collabora Online:
<https://sdk.collaboraonline.com/docs/installation/Proxy_settings.html>
:::

```bash
sudo coolconfig set ssl.enable false
sudo coolconfig set ssl.termination true
sudo coolconfig set storage.wopi.host nextcloud.example.com
sudo coolconfig set-admin-password
sudo systemctl restart coolwsd
systemctl status coolwsd
```
````
