---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo funciona la protección contra fuerza bruta de Nextcloud, cómo ajustarla, diagnosticar ralentizaciones, excluir IP y combinarla con fail2ban."
---
# Protección contra ataques de fuerza bruta

## Resumen

Esta página explica cómo funciona la protección integrada de Nextcloud contra ataques de fuerza bruta, cómo ajustarla con la app `bruteforcesettings`, `occ` y `config.php`, cómo diagnosticar inicios de sesión lentos y excluir direcciones IP, y en qué se diferencia de fail2ban. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_server/bruteforce_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Introducción

Nextcloud incluye protección contra los intentos de fuerza bruta.

La función de protección contra fuerza bruta está pensada para proteger los servidores Nextcloud de los intentos de adivinar contraseñas y tokens de distintas maneras. Además del ataque obvio de «probemos una gran lista de contraseñas de uso común», también dificulta ataques algo más sofisticados a través de la página de restablecimiento de contraseña o intentando encontrar tokens de contraseñas de aplicación. Se usa en todo el ecosistema de Nextcloud, también en otras apps, si tienen puntos de entrada sensibles (y eligen activar la compatibilidad con ella).

### Cómo funciona

#### Descripción general

Cuando se activa, la protección contra fuerza bruta ralentiza durante un periodo de hasta 24 horas las solicitudes que llegan desde una dirección IP a través de un punto de entrada protegido contra fuerza bruta. En circunstancias extremas puede impedir directamente el acceso desde una dirección IP problemática durante hasta 30 minutos.

Esto protege el sistema de atacantes que prueban, por ejemplo, muchas contraseñas distintas.

El filtro principal se basa en la dirección IP. Esto significa que ninguna cuenta (ni siquiera una asociada a un intento de fuerza bruta concreto) se ve afectada cuando se conecta desde una dirección IP distinta de la de los intentos de fuerza bruta. Esto ayuda a minimizar las denegaciones de servicio involuntarias contra conexiones legítimas y, a la vez, a maximizar la resistencia a los ataques desde orígenes IP problemáticos.

Las activaciones molestas se minimizan mediante valores predeterminados razonables integrados, adecuados a cada tipo de acción.

Un trabajo cron diario gestiona automáticamente el historial de intentos. Las entradas individuales caducan a las 48 horas (no obstante, los intentos pueden seguir *registrándose* indefinidamente en otros lugares mediante los mecanismos habituales de Nextcloud Server y a criterio del administrador).

Se admite excluir (incluir en la lista blanca) determinadas direcciones IP de la protección contra fuerza bruta para evitar falsos positivos, pero normalmente los falsos positivos se resuelven mejor corrigiendo sus causas de fondo (p. ej., un proxy inverso mal configurado o un cliente que se comporta mal).

:::{tip}
Si se detecta un problema en el comportamiento de autenticación de cualquiera de los clientes oficiales de Nextcloud, conviene informarlo en el repositorio correspondiente para que pueda investigarse.
:::

Mantener la protección contra fuerza bruta activa y funcionando correctamente ayuda a proteger Nextcloud Server de actores maliciosos y, a la vez, minimiza el posible impacto en el uso legítimo.

#### Ejemplo: la página de inicio de sesión

Donde más fácil es ver en acción la protección contra fuerza bruta es en la página de inicio de sesión. Si se intenta iniciar sesión por primera vez con un nombre de usuario y/o una contraseña no válidos, no se nota nada. Pero si se repite unas cuantas veces, se empieza a notar que la verificación del inicio de sesión tarda más cada vez. Es la protección contra fuerza bruta que entra en acción.

El retraso máximo es de 25 segundos, salvo que se haya alcanzado el número máximo de intentos (actualmente 10) en los últimos 30 minutos (en cuyo caso se devolverá un `429 Too Many Requests` hasta que el número de intentos en el periodo reciente baje del umbral).

Tras un inicio de sesión correcto (desde la misma dirección IP de origen), se borran los intentos de inicio de sesión no válidos anteriores y el retraso deja de aplicarse.

:::{note}
No todas las acciones se tratan necesariamente igual. Es posible que algunas actividades sean más (o menos) estrictas que otras.
:::

### Uso

#### Activación

La protección contra fuerza bruta está activada de forma predeterminada en Nextcloud. Su comportamiento puede ajustarse mediante la app `bruteforcesettings` (incluida con el servidor y activada de forma predeterminada), varios comandos `occ` y varios parámetros de `config.php`. Su eficacia depende mucho de tener un entorno bien configurado, sobre todo al integrar un proxy inverso con Nextcloud (y los parámetros asociados, como `trusted_proxies`).

#### La app de ajustes de fuerza bruta

Esta app, incluida y activada de forma predeterminada, permite (desde la interfaz web) ver el estado de una conexión y modificar ciertos parámetros de la protección contra fuerza bruta integrada en Nextcloud Server.

La interfaz que añade esta app está en *Configuraciones de administración -> Seguridad*, bajo el encabezado *Lista de permitidos de la Fuerza Bruta*.

Actualmente, un administrador puede ver el estado de la dirección IP desde la que se conecta y especificar direcciones y rangos IPv4 o IPv6 que quedan exentos de la protección contra fuerza bruta.

En el futuro podrían añadirse mejoras, en esta app y/o en combinación con Nextcloud Server, para supervisión adicional o ajustes del comportamiento relacionados con la protección contra fuerza bruta.

:::{warning}
Desactivar la app `bruteforcesettings` **no** desactiva la protección contra fuerza bruta. La protección está integrada en el núcleo de Nextcloud Server y siempre está activa. Desactivar la app solo elimina la posibilidad de gestionar los ajustes de fuerza bruta desde la interfaz web.
:::

:::{danger}
Para desactivar la protección contra fuerza bruta habría que ajustar el parámetro `auth.bruteforce.protection.enabled` en el `config.php` de Nextcloud, algo **totalmente desaconsejado en servidores de producción**, sobre todo si el servidor es accesible a través de una dirección IP pública. Permite a un atacante recorrer todos los usuarios y sus contraseñas, y después las verificaciones de dos factores, hasta obtener finalmente acceso de administrador.
:::

#### Comandos `occ`

Hay varios comandos `occ` relacionados con la fuerza bruta bajo `occ security`.

#### Protección contra fuerza bruta y balanceadores de carga o proxies inversos

Si el servidor está detrás de un proxy inverso o un balanceador de carga, es importante asegurarse de que esté bien configurado. En especial, las variables **trusted_proxies** y **forwarded_for_headers** de *config.php* deben establecerse correctamente. De lo contrario, puede ocurrir que Nextcloud empiece a limitar todo el tráfico que llega del proxy inverso o del balanceador de carga. Hay más información en {nc-doc}`Proxy inverso <admin_manual/configuration_server/reverse_proxy_configuration>`.

### Solución de problemas

#### Descripción general

En la mayoría de las instalaciones Nextcloud funciona sin problemas desde el primer momento. Si iniciar sesión o conectarse suele ser muy lento para varios usuarios, el primer paso es revisar los registros de Nextcloud Server para ver qué direcciones IP se detectan (para ello hay que ajustar temporalmente `loglevel` a `1`).

Buscar entradas que empiecen por cualquiera de los siguientes textos:

- *Bruteforce attempt from* [...]
- *IP address throttled* [...]
- *IP address blocked* [...]

Si todos los clientes parecen proceder de la misma dirección IP y esa dirección IP resulta ser la del proxy, hay que revisar la configuración de `trusted_proxies`.

Si la dirección IP es un endpoint común, como una oficina con varios usuarios, puede ser una opción incluirla en la lista blanca, con el inconveniente de que los usuarios tienen que ser de confianza.

Para hacer pruebas, puede convenir incluir la propia dirección IP en la lista blanca para ver si el problema desaparece. Si desaparece (y suponiendo que la configuración del proxy sea correcta), puede que haya en la red un cliente o dispositivo que se comporta mal y genera intentos de inicio de sesión no válidos desde esa dirección IP.

El comando *occ security:bruteforce:attempts* permite consultar el estado en tiempo real de una dirección IP determinada.

:::{note}
La tabla *bruteforce_attempts* de la base de datos estará vacía si se usa una caché de memoria distribuida, ya que el backend de base de datos deja de usarse salvo que sea la única opción disponible.
:::

#### Excluir direcciones IP de la protección contra fuerza bruta

:::{note}
La mayoría de las activaciones molestas de la protección contra fuerza bruta se resuelven configurando correctamente los proxies inversos. En otros casos, las direcciones IP concretas que deban incluirse en la lista blanca pueden configurarse en esta app (manteniendo activada la protección contra fuerza bruta). Esto puede ser útil para hacer pruebas o cuando muchas personas (o dispositivos) se conectan desde una única dirección IP conocida.
:::

Es posible excluir direcciones IP de la protección contra fuerza bruta.

- Asegurarse de que la app `bruteforcesettings` esté activada (lo está de forma predeterminada)
- Iniciar sesión como administrador e ir a **Configuraciones de administración -> Seguridad**

:::{danger}
Cualquier dirección IP excluida puede realizar intentos de autenticación sin ninguna limitación. Lo mejor es excluir el menor número posible de direcciones IP, o incluso ninguna.
:::

### Protección contra fuerza bruta frente a fail2ban

La protección contra fuerza bruta integrada en Nextcloud y fail2ban son herramientas complementarias que actúan en capas distintas de la pila. En servidores de producción se recomienda usar ambas a la vez.

La **protección contra fuerza bruta de Nextcloud** está integrada en el propio Nextcloud Server (la app `bruteforcesettings` aporta la interfaz de administración y los ajustes de exclusión, pero la protección funciona de todos modos). Actúa en la **capa de aplicación**: detecta patrones sospechosos de inicio de sesión y añade retrasos progresivamente mayores a las solicitudes de la dirección IP infractora. Tiene todo el contexto sobre los puntos de acceso y las credenciales propios de Nextcloud, y se activa automáticamente sin ninguna configuración del sistema operativo.

**fail2ban** actúa en la **capa del sistema operativo y de red**. Vigila los archivos de registro en busca de entradas de inicios de sesión fallidos y ordena al cortafuegos del sistema (p. ej., `iptables` o `nftables`) que bloquee directamente la IP infractora. Las solicitudes bloqueadas se descartan antes de llegar al servidor web, a PHP o a la base de datos, lo que ahorra por completo recursos del servidor.

Los dos enfoques no son mutuamente excluyentes:

- La protección contra fuerza bruta de Nextcloud gestiona de forma transparente la limitación en la capa de aplicación, también para los clientes de la API y las apps móviles, sin necesidad de configurar el sistema.
- fail2ban reduce la carga del servidor bloqueando a los infractores reincidentes en la capa de red antes de que sus solicitudes consuman recursos de la aplicación.

Las instrucciones para configurar fail2ban con Nextcloud están en {nc-ref}`Configurar fail2ban <setup_fail2ban>`.
````
