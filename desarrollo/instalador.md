---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "El repositorio de la suite: el fork de AIO en un solo árbol, el paquete del host, el Provisionador, el manifiesto de aplicaciones y la publicación firmada."
---
# Instalador de APS Conecta Gestión

## Resumen

El repositorio [APS-Conecta/gestion](https://github.com/APS-Conecta/gestion) reúne el fork de AIO, el paquete del anfitrión, el Provisionador y el manifiesto de aplicaciones. El desarrollo avanza en un solo árbol sobre `main`.

```{note}
Los cambios del plan de actualización corresponden a la próxima versión. Consulte su estado en {doc}`/proyecto/novedades/instalador` y seleccione una versión publicada para instalar.
```

Cada versión vincula un commit, las imágenes y el paquete firmado. Las aplicaciones adicionales llegan por el canal declarado en `apps.json`: publicación firmada o instalación acotada desde la tienda.

## Tabla

| Verificación | Entrada | Resultado esperado |
|---|---|---|
| Compuerta local | `bash scripts/test.sh` | Pruebas estáticas y autopruebas completas |
| Marca y adquisición | `bash scripts/brand-gate.sh .` y `bash scripts/acquisition-gate.sh .` | Identidad, funciones admitidas y canales de instalación coherentes |
| Validadores | `bash scripts/validate.sh .` | Ortografía, Dockerfiles y definiciones válidas |
| Inventario de construcción | `python3 scripts/images.py build-matrix` | Todos los Dockerfiles de ejecución, derivados del inventario |
| Imágenes publicadas | `python3 scripts/images.py verify VERSION --sha COMMIT` | Resúmenes y etiquetas de origen correspondientes al commit fijado |
| Instalación limpia | `cleanboot.yml` | Instalación, reinicio, provisión repetida, recuperación y actualización verificadas |
| Publicación | `release.yml` | Compuertas completas, procedencia, firmas y contenido comprobados |

## Notas

### Construcción y procedencia

`images.yml` fija un commit y construye todas las imágenes de ejecución desde ese árbol. PostgreSQL se prueba antes de publicar; la comprobación confirma que las capas publicadas son las probadas. El manifiesto registra el origen y el resumen de cada imagen.

Una versión publicada conserva sus resúmenes. La opción `--force` corresponde a conjuntos todavía inéditos. El paquete se obtiene con `git archive` del commit fijado.

### Firma y credenciales

El entorno `Release` contiene `MINISIGN_SECRET_KEY`, `MINISIGN_KEY_PASSWORD` y `SPREED_REFRESH_TOKEN`. Cada paso recibe únicamente la credencial que consume. Conserve `installer.pub` en el repositorio como clave pública de verificación.

La cadena comprueba la firma y el contenido de las publicaciones de Talk. Las etiquetas de ensayo `v0.0.0-ci.N` se publican como preliminares y conservan la versión estable marcada como más reciente. El procedimiento está en [RELEASING.md](https://github.com/APS-Conecta/gestion/blob/main/aps/RELEASING.md).

### Desarrollo y verificación

Trabaje en una rama por tarea. Ejecute las verificaciones en un árbol de trabajo aislado y registre los resultados en el pull request. Los cambios de imágenes se validan con un conjunto reconstruido y una instalación limpia.

El permiso predeterminado de los workflows es de lectura. Los trabajos declaran los permisos de escritura necesarios y los checkouts usan `persist-credentials: false`.

El plan vigente está en [gestion #175](https://github.com/APS-Conecta/gestion/issues/175). La documentación acompaña cada entrega en sus manuales de uso, administración y desarrollo.
