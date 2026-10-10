---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API declaradas obsoletas en esta versión, el método que reemplaza a cada una y el plazo mínimo de tres años antes de su eliminación, salvo ruptura inevitable."
---
(nc-dev-deprecated-apis)=
# Obsolescencias

## Resumen

Esta página explica cuánto se mantienen las API obsoletas antes de eliminarse y enumera las que se declaran obsoletas en esta versión, con el método que las reemplaza. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/deprecations.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Para mejorar la plataforma, se están retirando progresivamente algunas API. Las API obsoletas se mantienen al menos
tres años antes de eliminarse, salvo que la ruptura no pueda evitarse.

Se recomienda encarecidamente usar las reglas de [{vendor}`Nextcloud` Rector](https://packagist.org/packages/nextcloud/rector),
que pueden corregir automáticamente algunos cambios de API.

### Nuevas obsolescencias

- `\OCP\Util::setChannel` ahora está obsoleto y hay que usar `\OCP\ServerVersion::setChannel` en su lugar.
- `\OCP\Util::linkToAbsolute` ahora está obsoleto y hay que usar `\OCP\IUrlGenerator::getAbsoluteUrl` y `\OCP\IUrlGenerator::linkTo` en su lugar.
- `\OCP\Util::linkToRemove` ahora está obsoleto y hay que usar `\OCP\IUrlGenerator::linkToRemote` en su lugar.
- `\OCP\Util::isPublicLinkPasswordRequired` ahora está obsoleto y hay que usar `\OCP\Share\IManager::shareApiLinkEnforcePassword` en su lugar.
- `\OCP\Util::isDefaultExpireDateEnforced` ahora está obsoleto y hay que usar `\OCP\Share\IManager::shareApiLinkDefaultExpireDateEnforced` en su lugar.

#### Gestión de aplicaciones

- `\OCP\AppFramework\App::buildAppNamespace` está obsoleto en favor del método no estático `\OCP\App\IAppManager::getAppNamespace`

### Obsolescencias anteriores

En esta sección se encuentran todas las obsolescencias vigentes.

Ver también las {nc-ref}`notas de versión <previous-versions>` anteriores para consultar obsolescencias.
````
