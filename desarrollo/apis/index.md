---
tipo: explicacion
audiencia: desarrollo
apps: [Databases, territorio]
resumen: "Mapa de las APIs que usa la suite: fuentes geoespaciales oficiales, servicios con acceso restringido y las interfaces de Nextcloud."
---
# APIs

Esta sección reúne las APIs externas e internas que usa la suite, con el detalle que una persona necesita para conectarse: dirección, protocolo, capas, campos y límites conocidos. Se centra en las fuentes geoespaciales del mapa de territorio.

La fuente de verdad del estado de cada servicio es el catálogo `APIs/catalog.yaml` del repositorio Databases ({doc}`/desarrollo/databases`). Las páginas de esta sección explican cómo se usa cada fuente y no repiten el estado de los sondeos: para saber si un servicio responde hoy, se consulta el catálogo y su último informe de sondeo.

```{toctree}
:maxdepth: 1

Geoportal de Chile <geoportal-cl>
Salud, educación y bomberos <salud-educacion-bomberos>
Límites administrativos <limites-administrativos>
FONASA y ciclovías <fonasa-y-ciclovias>
Nextcloud y REST interno <nextcloud-y-rest-interno>
```
