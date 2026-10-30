---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "El repositorio de la suite: el fork de AIO en un solo árbol, el paquete del host, el Provisionador, el manifiesto de aplicaciones y la publicación firmada."
---
(instalador)=
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

(el-paquete-es-el-arbol-de-la-etiqueta)=
### Construcción y procedencia

`images.yml` fija un commit y construye todas las imágenes de ejecución desde ese árbol. PostgreSQL se prueba antes de publicar; la comprobación confirma que las capas publicadas son las probadas. El manifiesto registra el origen y el resumen de cada imagen.

Una versión publicada conserva sus resúmenes. La opción `--force` corresponde a conjuntos todavía inéditos. El paquete se obtiene con `git archive` del commit fijado.

### Firma y credenciales

El entorno `Release` contiene `MINISIGN_SECRET_KEY`, `MINISIGN_KEY_PASSWORD` y `SPREED_REFRESH_TOKEN`. Cada paso recibe únicamente la credencial que consume. Conserve `installer.pub` en el repositorio como clave pública de verificación.

La cadena comprueba la firma y el contenido de las publicaciones de Talk. Las etiquetas de ensayo `v0.0.0-ci.N` se publican como preliminares y conservan la versión estable marcada como más reciente. El procedimiento está en [RELEASING.md](https://github.com/APS-Conecta/gestion/blob/main/aps/RELEASING.md).

### Desarrollo y verificación

Trabaje en una rama por tarea. Ejecute las verificaciones en un árbol de trabajo aislado y registre los resultados en el pull request. Los cambios de imágenes se validan con un conjunto reconstruido y una instalación limpia.

`Containers/network-prefix.sh` calcula el prefijo IPv4 desde la dirección del servicio y su interfaz. Las imágenes de Nextcloud y Apache incluyen el mismo archivo y usan el contexto de construcción del repositorio. La compuerta local verifica prefijos e información ausente o ambigua; Clean boot comprueba una red `/20`, un cliente de la LAN con cabecera simulada y un proxy interno con una dirección reenviada válida.

Los trabajos de comprobación declaran permisos de lectura. El workflow reutilizable de imágenes admite `packages: write` para publicar y reduce los trabajos de comprobación a lectura. Los checkouts usan `persist-credentials: false`.

El plan vigente está en [gestion #175](https://github.com/APS-Conecta/gestion/issues/175). La documentación acompaña cada entrega en sus manuales de uso, administración y desarrollo.

El flujo de inicio termina con un resultado explícito dentro de su respuesta HTML. La consola valida ese resultado y comparte el mismo inicio con la actualización. Los avances de capas y bytes se distinguen de las señales periódicas de conexión; los estados repetidos y los reinicios cíclicos conservan el límite de 20 minutos de inactividad, medido con reloj monotónico.

Las autopruebas del anfitrión simulan errores con HTTP 200, una descarga de 70 minutos con avances, una descarga detenida y la recuperación de sesión. Una respuesta de autenticación permite un reingreso; una interrupción ambigua exige revisar el estado antes de repetir el inicio.

### El arranque de una línea

El activo de instalación de cada versión lleva la suma del paquete y la clave pública. Desempaca la suite en `/opt/aps-conecta/instalador` y conserva el paquete en `/opt/aps-conecta/paquete` para verificarlo sin red. El procedimiento está en {doc}`/administracion/aio`.

Antes de instalar la carpeta del paquete, ejecuta la comprobación de instalación existente del módulo del anfitrión incluido en el paquete verificado. Las comprobaciones de arquitectura, FUSE, Docker, disco y puertos se comparten entre la revisión previa, la preparación y el inicio desde el navegador. Las autopruebas del anfitrión y del arranque cubren los rechazos con comandos simulados; Clean boot instala el paquete antes de crear los contenedores.

### Proxy de salida

El anfitrión valida y carga un perfil de variables fijo, con permisos privados y lectura literal. El arranque firmado delega su guardado al módulo del paquete verificado. Docker utiliza un archivo de entorno mediante una configuración de systemd; el comando de arranque contiene su ruta. La aplicación correcta se registra después del reinicio del servicio y una falla conserva el intento pendiente.

El asistente transmite el entorno normalizado al contenedor de la plataforma. Su configuración de proxy existente aplica las exclusiones y marca la dirección como sensible en los listados ordinarios. Las llamadas al socket Docker permanecen directas. Las autopruebas del anfitrión cubren persistencia, propagación, exclusiones y recuperación; Clean boot verifica solicitudes autenticadas al registro y GitHub mediante un proxy local.

### La corrección de red con consentimiento

La tarjeta «La red del servidor» ofrece «Sí, corregir» cuando el servidor necesita DNS dividido para alcanzar su dominio. La corrección requiere consentimiento explícito y reinicia Docker una vez.

`dnsmasq` utiliza `bind-dynamic` con escucha en loopback y la dirección LAN. El escritor JSON existente combina el DNS de Docker con los servidores obtenidos de `resolvectl dns` y `resolv.conf`; conserva las otras opciones y excluye direcciones locales que producen bucles y direcciones IPv6 que requieren la interfaz del anfitrión. Las autopruebas cubren ambas fuentes y la repetición sin cambios.

La preparación separa la instalación de herramientas requeridas y del verificador opcional. Su ausencia mantiene la firma pendiente e informa cómo habilitar universe en Ubuntu.

### Pisos de recursos y datos comunales

La revisión previa informa recursos mínimos y recomendados. La instalación silenciosa importa los datos comunales; la repetición conserva los datos existentes.

### Instalaciones previas

El instalador sirve instalaciones limpias. El procedimiento de actualización y los límites de instalaciones anteriores están en {doc}`/administracion/aio`.

(deuda-tecnica-y-limites)=
### Límites

Las integraciones pendientes y la versión que las incorpora se registran en {doc}`/proyecto/novedades/instalador`.
