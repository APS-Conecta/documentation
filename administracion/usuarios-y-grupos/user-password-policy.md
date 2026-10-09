---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Las reglas de la política de contraseñas: longitud mínima, historial, caducidad, bloqueo, caracteres exigidos y comprobación de contraseñas filtradas."
---
# Política de contraseñas de usuario

## Resumen

Esta página enumera las reglas de la política de contraseñas que pueden configurarse en la sección Seguridad de las Configuraciones de administración, de la longitud mínima a la comprobación contra contraseñas filtradas. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_password_policy.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Una política de contraseñas es un conjunto de reglas pensadas para mejorar la seguridad informática animando a los usuarios a emplear contraseñas robustas y a usarlas correctamente.

En la sección Seguridad de las Configuraciones de administración se puede configurar

- una longitud mínima de la contraseña. El valor predeterminado es 10 caracteres.
- un historial de contraseñas
- un periodo de caducidad de las contraseñas
- una política de bloqueo
- la prohibición de contraseñas comunes como «password» o «login».
- la obligación de usar mayúsculas y minúsculas
- la obligación de usar caracteres numéricos
- la obligación de usar caracteres especiales como ! o :
- la comprobación de la contraseña contra la lista de contraseñas filtradas de haveibeenpwnd.com (comprobación con hash mediante la API de haveibeenpwnd.com)
````
