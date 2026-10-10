---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "Las cuatro áreas de carpetas de equipo del establecimiento, quién lee y quién gestiona cada una, y la regla de una sola copia viva."
---
# Archivos

## Resumen

La aplicación **Archivos** guarda los documentos del establecimiento. Esta sección reúne el manual de Archivos de la plataforma base: el acceso, la gestión, la colaboración y la seguridad. Al final, la sección «En APS Conecta Gestión» describe cómo la suite organiza los documentos de un centro de salud: cuatro áreas de carpetas de equipo, sus permisos y las convenciones de trabajo.

````{upstream} user_manual/files/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

- {nc-doc}`user_manual/files/accessing`
- {nc-doc}`user_manual/files/managing`
- {nc-doc}`user_manual/files/collaboration`
- {nc-doc}`user_manual/files/security`
````

## En APS Conecta Gestión

### Las cuatro áreas

Los documentos del establecimiento viven en carpetas de equipo, no en la carpeta personal de cada cuenta. La suite crea esas carpetas en cuatro áreas:

- **Transversal**: el conocimiento que comparte todo el personal. Trae cinco subcarpetas: **Protocolos**, **Flujogramas**, **Documentación**, **Registro de redes** y **Actas de reuniones**.
- **Programas**: una carpeta por programa de salud, con el nombre que le da el establecimiento.
- **Unidades**: una carpeta por unidad funcional. La suite parte de seis (SOME, Farmacia, Dental, OIRS, Estadística-REM y Dirección) y cada establecimiento ajusta la lista.
- **Sectores**: una carpeta por sector territorial, con el nombre propio de cada sector.

La carpeta **Transversal** contiene además el archivo **LÉEME — Convenciones.md**, con las reglas de organización de esta página escritas para el personal.

Para abrir un documento del área:

1. Abrir la aplicación **Archivos**.
2. Abrir la carpeta del área: **Transversal**, **Programas**, **Unidades** o **Sectores**.
3. Abrir la carpeta del programa, de la unidad o del sector.
4. Hacer clic en el documento para editarlo en el navegador, como describe {doc}`/usuario/oficina`.

### Quién lee y quién gestiona

El acceso se concede siempre a grupos, nunca a personas: cada cuenta ve las carpetas que le abren sus grupos, es decir, su rol, su categoría, sus equipos y «Todo el personal». Gestionar una carpeta es leer, escribir y eliminar en ella.

| Carpeta | Solo lectura | Gestión |
|---|---|---|
| Transversal | Todo el personal | Jefaturas |
| Programas/«programa» | — | El equipo del programa y Jefaturas |
| Unidades/«unidad» | Jefaturas | El rol dueño de la unidad |
| Unidades/Dirección | — | Jefaturas |
| Sectores/«sector» | — | El equipo del sector y Jefaturas |

Las unidades de partida tienen estos roles dueños:

| Unidad | Rol dueño |
|---|---|
| SOME | Administrativo SOME |
| Farmacia | Químico Farmacéutico (Dir. Técnico Farmacia) y TENS – Farmacia / PNAC |
| Dental | Cirujano Dentista y TONS (Técnico en Odontología) |
| OIRS | Encargado/a OIRS |
| Estadística-REM | Encargado/a de Estadística (REM) |
| Dirección | Ninguno: la gestionan las Jefaturas |

Ninguna concesión de esta matriz de partida incluye el permiso de compartir: los documentos de las carpetas de equipo no se comparten con otras cuentas ni por enlace público.

### Una sola copia viva

Estas reglas existen para que cada documento tenga una versión confiable:

- Editar el documento en su lugar, en el navegador, en vez de descargarlo, editarlo y volver a subirlo.
- No duplicar archivos con sufijos como `_final`, `_final2` o `_ESTE_SI`.
- Conservar un hito con el {doc}`historial de versiones </usuario/archivos/version-control>` o con un sufijo `vN` explícito, y borrar los borradores.
- Guardar la copia viva en la carpeta del área que le corresponde.
- Enviar el enlace al documento, no una copia del archivo.

### Nombres de archivo

Los nombres de archivo siguen el patrón `AAAA-MM-DD_area_tema_vN.ext`:

| Parte | Regla |
|---|---|
| `AAAA-MM-DD` | La fecha ISO va primero, para que los archivos se ordenen solos. |
| `area`, `tema` | En minúsculas y sin acentos. |
| `vN` | Solo cuando hace falta marcar un hito. |

Un ejemplo es `2026-07-19_protocolos_triage-urgencias_v2.docx`. El nombre no lleva espacios raros ni caracteres especiales: el título en español va en el contenido del documento.

### Archivos eliminados

Cada carpeta de equipo conserva su propia papelera, así que un archivo eliminado en ella se puede recuperar. El procedimiento está en {doc}`/usuario/archivos/deleted-file-management`.

### Límites

- Las convenciones se cumplen a mano: ningún proceso clasifica, mueve ni renombra archivos de forma automática.
- La matriz de acceso es un primer corte. La matriz validada se acuerda después con cada establecimiento.
- El archivo **LÉEME — Convenciones.md** se instala una sola vez y no se sobrescribe, porque el personal puede haberlo anotado. Una versión nueva de las convenciones no llega a un establecimiento que ya tiene el archivo.
- La plataforma es una intranet operativa, no una ficha clínica. Los registros de pacientes se llevan en la ficha clínica del establecimiento, no en estas carpetas.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
