---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Delegar el acceso a páginas de configuración de administración en grupos que no son admin, y los riesgos de escalada de privilegios que conlleva."
---
# Privilegios de administración (delegación)

## Resumen

Esta página explica cómo conceder a grupos que no pertenecen a `admin` acceso a páginas y secciones concretas de las configuraciones de administración, cómo revocarlo y qué riesgo de escalada de privilegios implica delegar la gestión de usuarios. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/admin_delegation_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

Nextcloud incluye una funcionalidad que permite a los administradores delegar autoridad en otras personas sin concederles privilegios de administración completos (y sin hacerlas miembros del grupo `admin`).

Esta funcionalidad de delegación de privilegios de administración la admiten muchas apps, incluidas con el servidor y del ecosistema, que tienen sus propias áreas de configuración en *Configuraciones de administración*.

:::{note}
Quien desarrolle una app y quiera que los administradores puedan usar esta funcionalidad con ella debe activar la compatibilidad con la delegación de sus ajustes (los detalles están en el Manual para desarrolladores).
:::

:::{tip}
La delegación de la gestión de usuarios es posible, pero también pueden usarse los {nc-doc}`administradores de grupo <admin_manual/configuration_user/user_configuration>`.
:::

:::{warning}
La delegación de la gestión de usuarios permite a los usuarios delegados añadirse a sí mismos a grupos que reciben la delegación de otros ajustes. Esto puede usarse para escalar privilegios.
:::

### Uso

De forma predeterminada, solo los miembros del grupo `admin` pueden acceder a *Configuraciones de administración*. Pueden crearse grupos de usuarios adicionales (o usarse grupos existentes) y después conceder a esos grupos acceso a ajustes concretos.

Con la sesión iniciada en una cuenta que sea miembro del grupo `admin`, ir a *Configuraciones de administración* -> *Privilegios de administración*. Se mostrará la lista de páginas y secciones de configuración que admiten la delegación, incluidas las de cualquier app instalada.

Al hacer clic en el cuadro combinado se puede elegir qué grupos pueden acceder a los ajustes seleccionados. El acceso puede revocarse en cualquier momento quitando el grupo de la selección (o, si solo se quiere revocar el acceso de una cuenta individual, quitando esa cuenta del grupo configurado).

:::{tip}
No todas las páginas o secciones de configuración admiten la delegación. Esto se debe a que delegar el acceso a esa página de configuración concreta permitiría escalar privilegios (es decir, eludir la autoridad de administración limitada) o a que la delegación aún no se ha implementado para esa página de configuración o app concreta.
:::
````
