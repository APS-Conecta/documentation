---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion, IntraVox]
resumen: "Cuentas y grupos de la plataforma base y el modelo de APS Conecta Gestión: el grupo como única llave, cargos, carpetas de equipo y la planilla de personal."
---
# Usuarios y grupos

## Resumen

Esta sección reúne, para quienes administran el servidor, las páginas de la plataforma base sobre cuentas y acceso: la gestión de usuarios, las contraseñas, la autenticación de dos factores, LDAP, OpenID Connect, los perfiles y la API de aprovisionamiento. La sección «En APS Conecta Gestión», al final, describe el modelo de acceso que provisiona la suite y el ciclo de vida de sus cuentas.

````{upstream} admin_manual/configuration_user/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

- {nc-doc}`admin_manual/configuration_user/user_configuration`
- {nc-doc}`admin_manual/configuration_user/reset_admin_password`
- {nc-doc}`admin_manual/configuration_user/reset_user_password`
- {nc-doc}`admin_manual/configuration_user/user_password_policy`
- {nc-doc}`admin_manual/configuration_user/authentication`
- {nc-doc}`admin_manual/configuration_user/two_factor-auth`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap_cleanup`
- {nc-doc}`admin_manual/configuration_user/user_auth_ldap_api`
- {nc-doc}`admin_manual/configuration_user/user_provisioning_api`
- {nc-doc}`admin_manual/configuration_user/profile_configuration`
- {nc-doc}`admin_manual/configuration_user/user_auth_oidc`
````

## En APS Conecta Gestión

La autorización de la suite es solo por grupos. Toda concesión toma un id de grupo y nada más —el acceso a una carpeta, a una aplicación o la pertenencia de una persona—, así que lo que alcanza una cuenta se responde entero con los grupos a los que pertenece. De ahí la regla de la suite: conceder en el grupo más amplio que siga siendo correcto, para que un cargo nuevo herede las concesiones existentes sin editar ninguna.

### El registro de grupos

La fase 20 de la provisión es el registro de grupos: los crea con id en inglés y nombre mostrado en español, y las concesiones nombran siempre el id. La lista de los 22 cargos compartidos vive solo en [`20-groups.sh`](https://github.com/APS-Conecta/gestion/blob/main/provisioning/phases/20-groups.sh); los cargos propios de un centro se declaran en `SITE_ROLES`, en el archivo del sitio.

| Grupo | Id | Quién lo integra | Quién lo declara |
|---|---|---|---|
| Todo el personal | `all-staff` | Toda cuenta | La fase 20 |
| Categorías | `cat-jefaturas`, `cat-clinicos`, `cat-tecnicos`, `cat-administrativos` | Quien ocupa un cargo, según la categoría del cargo | La fase 20 |
| Cargos compartidos | 22 grupos `role-*` | Quien ocupa el cargo | La fase 20 |
| Cargos propios del centro | Grupos `role-*` adicionales | Quien ocupa el cargo | `SITE_ROLES`, en el archivo del sitio |
| Equipos | `prog-*` (programas) y `sector-*` (sectores) | Las personas del equipo | `SITE_TEAMS`, en el archivo del sitio |
| Administración | `admin` | La persona marcada en `primer_admin` | El asistente de AIO |
| Intranet | `IntraVox Users`, `IntraVox Editors`, `IntraVox Admins` | `all-staff` pasa a `IntraVox Users`; `cat-jefaturas` y `role-oirs`, a `IntraVox Editors` | IntraVox, con el mapa de la provisión |

- **Los grupos no se anidan.** Un cargo no concede nada por «pertenecer» a una categoría: la cuenta que ocupa el cargo entra también a su categoría, y el tercer campo de cada cargo declara cuál.
- **Las categorías son fijas.** Son lo que hace comparable la matriz de acceso de un centro con la de otro, así que un centro no las define. Un cargo propio empieza con `role-` y nombra una de las cuatro categorías; si no, la fase 20 se detiene.
- **La intranet.** En IntraVox, `IntraVox Users` solo lee, `IntraVox Editors` lee, escribe y crea páginas, e `IntraVox Admins` tiene acceso completo; la preparación del motor suma a este último, una vez, a la administración de la plataforma.

### Carpetas de equipo y permisos

Los documentos del centro viven en carpetas de equipo (Group Folders). Estas carpetas no se anidan, así que los nombres de montaje con barra —`Programas/…`, `Unidades/…`, `Sectores/…`— dan el aspecto de árbol: `Transversal` es una sola carpeta, y cada programa, unidad y sector es la suya.

La matriz de acceso es del centro: el archivo del sitio la declara en `SITE_ACL`, una fila `carpeta|grupo|permisos` por concesión, y la fase 40 la aplica. Hay dos niveles:

| Nivel | Campo de permisos | Máscara | Uso en la matriz de primer corte |
|---|---|---|---|
| Lectura | Vacío | 1 | `Transversal` para `all-staff`; cada unidad con cargo dueño para `cat-jefaturas` |
| Gestión | `read write delete` | 15 | El resto, incluida `Unidades/Dirección` para `cat-jefaturas` |

La gestión incluye eliminar: con solo leer y escribir, una carpeta admite agregar pero no quitar, y una subida equivocada queda para siempre; además, mover un archivo exige eliminarlo en el origen. Las carpetas de equipo guardan su propia papelera, así que lo eliminado se recupera. Toda concesión que existe en estas carpetas sin estar declarada se retira: borrar una fila de `SITE_ACL` quita el acceso.

El modelo es de refinamiento por permiso, sin reglas de denegación: una denegación anularía lo que concede otro de los grupos de una persona con varios cargos. El refinamiento por subcarpeta espera la matriz validada con un establecimiento.

### Cuentas

Las cuentas son locales de la plataforma: la provisión las crea con `occ user:add`. Las páginas de LDAP y de OpenID Connect de esta sección describen integraciones que la provisión no configura.

- **Cuentas de cargo.** La provisión crea una cuenta por puesto: `director`, `subdirector`, `jefe.farmacia`, `jefe.some`, un jefe por sector (`jefe.<sector>`) y uno por cada cargo propio de la categoría `cat-jefaturas`. Cada una entra a su cargo, a `cat-jefaturas` y a `all-staff`, y la de un jefe de sector también a su equipo de sector.
- **Personas.** La planilla de personal es un archivo UTF-8 con seis columnas separadas por punto y coma: `usuario;nombre;apellidos;correo;grupos;primer_admin`. No lleva contraseñas. La columna `grupos` nombra los sectores, programas y cargos; `all-staff` y la categoría de cada cargo se agregan solos. Exactamente una fila lleva `sí` en `primer_admin`, y esa persona entra al grupo `admin`, que no se escribe en `grupos`. Los cargos no van en la planilla: sus cuentas ya existen.
- **Credenciales.** La provisión genera cada contraseña y la sella en `/opt/aps-conecta/credentials.txt`, con permiso 0600: una fila por persona y una por cuenta de cargo. El sellado es acumulativo: un usuario sellado conserva su contraseña para siempre, y uno que sale de la planilla y vuelve encuentra su fila intacta. El archivo se conserva, porque la re-provisión semanal lo lee para crear las cuentas que falten.

La guía clínica, en [«La planilla de usuarios»](https://github.com/APS-Conecta/gestion/blob/main/docs/GUIA-CLINICA.md#5-la-planilla-de-usuarios) y [«Las credenciales»](https://github.com/APS-Conecta/gestion/blob/main/docs/GUIA-CLINICA.md#6-las-credenciales), da el formato completo y el ritual de entrega.

### Bajas y divergencia

La provisión nunca elimina una cuenta. La verificación de divergencia compara las cuentas vivas con las declaradas —la planilla, las cuentas de cargo y la administración de la instalación—, y una cuenta viva sin declarar la hace fallar: el informe nombra la orden que la eliminaría y recuerda que eliminar una cuenta elimina sus archivos. Con la verificación en rojo, la re-provisión semanal queda fallida; {doc}`/administracion/operaciones/index` describe cómo llega el aviso. Un grupo vivo sin declarar también aparece, con la advertencia de revisar que no sea el único con acceso a una carpeta antes de eliminarlo.

### Compromisos y límites

- **Las pertenencias solo crecen.** La provisión agrega a cada persona a los grupos que declara su fila y nunca quita una pertenencia: quitar un equipo de una fila deja a la persona en ese grupo. En los grupos de la intranet, la regla está registrada como decisión: quien sale conserva la lectura.
- **Las reglas de la intranet se escriben una vez.** La carpeta de IntraVox es la única con reglas de acceso: cada página de equipo recibe una denegación de base para `IntraVox Users` y permisos de lectura para su equipo y para `cat-jefaturas`, escritos al crear la página. Si una provisión se detiene entre la creación de la página y sus reglas, la siguiente no las vuelve a escribir: se recuperan a mano o borrando la carpeta de esa página y volviendo a provisionar.
- **La actividad.** El flujo de actividad puede mostrar nombres de elementos que una regla de acceso oculta: los nombres sensibles no van en subcarpetas restringidas.
- **Segundo factor y contraseñas.** Ningún proveedor de autenticación de dos factores está activado ni se exige, y queda diferido en [gestion#75](https://github.com/APS-Conecta/gestion/issues/75). De la política de contraseñas, la suite fija solo la comprobación de contraseñas filtradas, y la apaga: ningún prefijo de hash sale del servidor, a costa de que una contraseña filtrada ya no se rechace. El cambio de la contraseña inicial se pide a cada persona; el sistema no lo exige.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
