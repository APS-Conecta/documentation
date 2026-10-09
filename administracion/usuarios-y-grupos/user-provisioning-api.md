---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La API de aprovisionamiento: qué permite hacer con usuarios, grupos y apps, su URL base, las cabeceras obligatorias y sus conjuntos de instrucciones."
---
# API de aprovisionamiento de usuarios

## Resumen

Esta página presenta la API de aprovisionamiento, que permite a sistemas externos gestionar usuarios, grupos, cuotas y apps mediante solicitudes HTTP: su URL base, las cabeceras que exige y los enlaces a sus conjuntos de instrucciones. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_provisioning_api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La aplicación Provisioning API habilita un conjunto de API que los sistemas externos pueden usar para crear, editar, eliminar y consultar atributos de usuario, consultar, establecer y quitar grupos, establecer cuotas y consultar el almacenamiento total usado en Nextcloud. Los usuarios administradores de grupo también pueden consultar Nextcloud y realizar las mismas funciones que un administrador para los grupos que gestionan. La API también permite a un administrador consultar las aplicaciones de Nextcloud activas y la información de las aplicaciones, y activar o desactivar una app de forma remota. Pueden usarse solicitudes HTTP con una cabecera Basic Auth para realizar cualquiera de las funciones enumeradas arriba. La app Provisioning API está activada de forma predeterminada.

La URL base de todas las llamadas a la Provisioning API es `https://cloud.example.com/ocs/v1.php/cloud`.

Todas las llamadas a los endpoints OCS exigen que la cabecera `OCS-APIRequest` tenga el valor `true`.

Todas las solicitudes POST exigen la cabecera `Content-Type: application/x-www-form-urlencoded`. (Nota: algunas bibliotecas, como cURL, establecen esta cabecera automáticamente; otras exigen establecerla de forma explícita).

- {nc-doc}`admin_manual/configuration_user/instruction_set_for_users`
- {nc-doc}`admin_manual/configuration_user/instruction_set_for_groups`
- {nc-doc}`admin_manual/configuration_user/instruction_set_for_apps`
````
