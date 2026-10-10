---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Compilar el cliente de escritorio: clonar desde GitHub, compilar en macOS y Windows, construir el instalador de Windows, parámetros de cmake y sanitizadores."
---
# Compilar el cliente

## Resumen

Esta página explica cómo preparar un entorno de compilación para desarrollar y probar el cliente de escritorio: clonar su repositorio de GitHub, compilarlo en macOS y en Windows, construir el instalador de Windows por compilación cruzada, los parámetros de cmake conocidos y los sanitizadores. Está dirigida a quienes desarrollan el cliente.

````{upstream} developer_manual/desktop/building.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El objetivo de esta sección es preparar un entorno de compilación para desarrollar y probar el cliente Nextcloud Desktop. Si solo se quiere usar el cliente Nextcloud Desktop sin desarrollarlo ni probarlo, conviene descargar en su lugar la última compilación estable.

:::{note}
Estas instrucciones representan una metodología concreta, simplificada y fácil de entender, pero de ningún modo son la única forma de preparar un entorno de compilación.
:::

Los pasos indicados aquí se han probado varias veces y deberían permitir compilar el cliente o la documentación, o ambos, sin advertencias ni errores. Estas instrucciones deberían estar al día con la versión, 34, del cliente de Nextcloud con la que se distribuyen. Si se usa la versión más reciente de estas instrucciones y aparecen errores o advertencias con el código más reciente del repositorio, abrir un issue en GitHub para avisarnos y así poder documentar una solución alternativa o corregir los problemas de fondo.

### Usar GitHub

De forma predeterminada, clonar el repositorio de GitHub entrega la rama «master», que es la más reciente. Si por algún motivo se quiere compilar una versión anterior del cliente Nextcloud Desktop, se puede elegir la rama correspondiente a esa versión. Sin embargo, con las versiones anteriores del cliente, hay que tener presente que los problemas que tengan pueden haberse corregido en versiones más recientes.

:::{note}
Hacer cualquier cosa que no sea simplemente descargar el código existente requiere tener una cuenta de GitHub.
:::

Si el objetivo de clonar y compilar el cliente Nextcloud Desktop es contribuir a su desarrollo, y aún no se es «colaborador» del repositorio de GitHub de Nextcloud Desktop, habrá que crear un «fork» haciendo clic en el botón «fork» de la esquina superior derecha de cualquier página de GitHub del repositorio. Es importante hacerlo de antemano, porque la URL para clonar el repositorio es distinta para un fork que para la versión oficial principal.

Al clonar un repositorio de GitHub, hay dos opciones para autenticar la cuenta de GitHub: SSH o HTTPS. SSH requiere una configuración adicional, pero es más seguro y simplifica las cosas más adelante. Para una explicación de las diferencias entre HTTPS y SSH, así como instrucciones para configurar SSH, consultar este [artículo de ayuda de GitHub][GitHub help article] sobre el tema.

La versión más básica del comando de Git para clonar un repositorio es la siguiente:

```bash
$ git clone <repository_url>
```

Esto clona el repositorio en el directorio donde se ejecuta el comando.

Las cuatro versiones del comando `git clone` son las siguientes:

1. HTTPS desde el repositorio oficial:

   ```bash
   $ git clone https://github.com/nextcloud/desktop.git
   ```

2. SSH desde el repositorio oficial:

   ```bash
   $ git clone git@github.com:nextcloud/desktop.git
   ```

3. HTTPS desde un fork (ver arriba):

   ```bash
   % git clone https://github.com/<github_username>/desktop.git
   ```

4. SSH desde un fork (ver arriba):

   ```bash
   % git clone git@github.com:<github_username>/desktop.git
   ```

### Compilación de desarrollo en macOS

:::{note}
Aunque es posible hacer muchos de los pasos siguientes con interfaces gráficas, siempre que es posible se indican en su lugar los comandos de Terminal, para simplificar el proceso.
:::

1. Instalar Xcode desde la Mac App Store:

   <https://apps.apple.com/app/xcode/id497799835>

Luego, en Terminal:

2. Instalar las herramientas de línea de comandos de Xcode:

   ```bash
   % xcode-select –install
   ```

3. Instalar Homebrew desde [brew.sh][brew.sh] (que simplemente mostrará lo siguiente):

   ```bash
   % /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

:::{note}
En determinadas circunstancias, puede aparecer un error del tipo `Permission denied @ apply2files` al instalar ciertos paquetes de Homebrew. Se trata de [un problema conocido][a known issue] y puede solucionarse cambiando los permisos de los archivos afectados con el siguiente comando:

```bash
% sudo chown -R $(whoami):admin /usr/local/* \
   && sudo chmod -R g+rwx /usr/local/*
```

Esta solución alternativa puede provocar otras advertencias de la shell.
:::

4. Instalar los paquetes de Homebrew:

   ```bash
   % brew install git qt qtkeychain cmake openssl glib cmocka karchive
   ```

5. Algunos paquetes de Homebrew no se enlazan automáticamente en lugares donde los scripts de compilación puedan encontrarlos, así que se puede crear un script de perfil de shell que los encuentre y los cargue dinámicamente al ejecutar una compilación:

   ```bash
   % echo 'export QT_PATH=$(brew --prefix qt6)/bin' >> ~/.nextcloud_build_variables
   % echo 'export CMAKE_PREFIX_PATH=$(brew --prefix qt6);$(brew --prefix karchive)' >> ~/.nextcloud_build_variables
   ```

   :::{note}
   El nombre `~/.nextcloud_build_variables` es solo una sugerencia por comodidad. Se puede usar otro archivo o crear un script de shell completo, pero esta forma de hacerlo es la más sencilla de explicar.
   :::

6. Clonar el repositorio de {vendor}`Nextcloud` en una ubicación conveniente, como `~/Repositories`:

   ```bash
   % mkdir ~/Repositories
   ```

   (si aún no existe), luego:

   ```bash
   % cd ~/Repositories
   ```

   :::{note}
   El repositorio clonado puede ir prácticamente en cualquier lugar donde la cuenta de usuario tenga acceso de escritura, aunque no debería ir en un directorio sincronizado con otro servicio en la nube (sobre todo, no en iCloud Drive). Se recomienda `~/Repositories` por orden y coherencia.
   :::

   ```bash
   % git clone <repository_url>
   ```

   (Ver la sección anterior sobre el uso de GitHub para una explicación de qué URL usar).

7. Crear el directorio de compilación:

   ```bash
   % cd ~/Repositories/desktop
   % mkdir build
   ```

8. Generar los archivos de compilación:

:::{note}
De forma predeterminada, Nextcloud Desktop se compila en un directorio protegido de macOS, así que hay que especificar una ubicación de compilación. Se puede hacer cada vez que se compila, o se puede añadir a las variables de compilación guardadas, así:

```bash
% echo 'export CMAKE_INSTALL_PREFIX=~/Builds' >> ~/.nextcloud_build_variables
# If you want to build a macOS app bundle for distribution
% echo 'export BUILD_OWNCLOUD_OSX_BUNDLE=ON' >> ~/.nextcloud_build_variables
```

Reemplazar `~/Builds` por otro directorio si se quiere que la compilación termine en otro lugar.
:::

```bash
% source ~/.nextcloud_build_variables
% cd ~/Repositories/desktop/build
% cmake ..
```

9. Compilar e instalar:

   ```bash
   % make install
   ```

### Compilación de desarrollo en Windows

#### Requisitos del sistema

- Windows 10 o Windows 11
- [El código del cliente de escritorio](https://github.com/nextcloud/desktop)
- Python 3
- PowerShell
- Microsoft Visual Studio 2022 y herramientas para compilar C++
- [KDE Craft](https://community.kde.org/Craft)

#### Configurar Microsoft Visual Studio

1. Hacer clic en «Modify» en Visual Studio Installer.

2. Seleccionar «Desktop development with C++»

#### Gestionar las dependencias

Las dependencias se gestionan con [KDE Craft](https://community.kde.org/Craft) porque es fácil de configurar y hace el mantenimiento mucho más fiable en todas las plataformas.

1. Configurar KDE Craft según las instrucciones de [Get Involved/development/Windows - KDE Community Wiki](https://community.kde.org/Get_Involved/development/Windows); requiere Python 3 y PowerShell.
2. Después de ejecutar:

```winbatch
C:\CraftRoot\craft\craftenv.ps1
```

3. Añadir los [blueprints del cliente de escritorio](https://github.com/nextcloud/desktop-client-blueprints), las instrucciones para gestionar las dependencias del cliente:

```winbatch
craft --add-blueprint-repository [git]https://github.com/nextcloud/desktop-client-blueprints.git
craft craft
```

4. Instalar todas las dependencias del cliente:

```winbatch
craft --install-deps nextcloud-client
```

#### Compilar

1. Asegurarse de que la variable de entorno %PATH% no tenga información que entre en conflicto con el entorno que se usará para compilar el cliente. Por ejemplo, si se instaló OpenSSL previamente y se añadió a %PATH%, el OpenSSL instalado podría ser de una versión distinta de la que se instaló mediante KDE Craft.
2. Abrir el símbolo del sistema (cmd.exe)
3. Ejecutar:

```winbatch
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
```

4. Para usar las herramientas instaladas con Visual Studio, se necesita lo siguiente en %PATH%:

   La imagen muestra las variables de entorno de Windows.

5. Como alternativa, se pueden usar las herramientas instaladas con KDE Craft añadiéndolas a %PATH%:

```winbatch
set "PATH=C:\CraftRoot\bin;C:\CraftRoot\dev-utils\bin;%PATH%"
```

:::{note}
C:\CraftRoot es la ruta que KDE Craft usa de forma predeterminada. Al configurarlo, se puede elegir otra carpeta.
:::

6. Crear la carpeta de compilación, ejecutar cmake, compilar e instalar:

```winbatch
cd <desktop-repo-path>
mkdir build
cd build
cmake .. -G Ninja -DCMAKE_INSTALL_PREFIX=. -DCMAKE_PREFIX_PATH=C:\CraftRoot -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build . --target install
```

7. Ahora se puede usar [Qt Creator](https://doc.qt.io/qtcreator) para importar la carpeta de compilación con su configuración y así poder trabajar con el código.

#### Compilación del instalador de Windows (es decir, de despliegue) (compilación cruzada)

Debido a la gran cantidad de dependencias, compilar el instalador del cliente para Windows **actualmente solo tiene soporte oficial en openSUSE**, usando el compilador cruzado MinGW. Se puede configurar cualquier versión de openSUSE con soporte actual en una máquina virtual si aún no se tiene instalada.

Para simplificar la configuración, se puede usar el Dockerfile proporcionado para construir una imagen propia.

1. Suponiendo que se está en la raíz del árbol de código fuente del cliente de Nextcloud, se puede construir una imagen a partir de este Dockerfile así:

   ```
   cd admin/win/docker
   docker build . -t nextcloud-client-win32:<version>
   ```

   Reemplazar `<version>` por la versión del cliente que se está compilando, p. ej., 34 para la versión del cliente que describe este documento. Si no se quiere usar docker, se pueden ejecutar manualmente en una shell los comandos de `RUN`, p. ej., para crear un entorno de compilación propio en una máquina virtual.

   :::{note}
   Las imágenes de docker son específicas de cada versión. Esta se refiere a la 34. ¡Las versiones más nuevas pueden tener dependencias distintas y, por tanto, requerir una versión posterior de la imagen de docker! ¡Elegir siempre la imagen de docker que corresponda a la versión del cliente de Nextcloud!
   :::

2. Desde dentro del árbol de código fuente, ejecutar la instancia de docker:

   ```
   docker run -v "$PWD:/home/user/client" nextcloud-client-win32:<version> \
      /home/user/client/admin/win/docker/build.sh client/  $(id -u)
   ```

   Esto ejecuta la compilación, crea un instalador basado en NSIS y además ejecuta las pruebas. El binario resultante estará en una subcarpeta `build-win32` recién creada.

   Si no se quiere usar docker y se ejecutaron los comandos de `RUN` anteriores en una máquina virtual, se pueden ejecutar manualmente en el árbol de código fuente los comandos con sangría de la sección inferior de `build.sh`.

% upstream numera el paso siguiente como 4 (no hay paso 3): este comentario cierra la lista para que empiece en 4, como allí.

4. Por último, conviene firmar el instalador para evitar advertencias durante la instalación. Esto requiere un certificado [Microsoft Authenticode][Microsoft Authenticode] `osslsigncode` para firmar el instalador:

   ```
   osslsigncode -pkcs12 $HOME/.codesign/packages.pfx -h sha256 \
             -pass yourpass \
             -n "ACME Client" \
             -i "http://acme.com" \
             -ts "http://timestamp.server/" \
             -in ${unsigned_file} \
             -out ${installer_file}
   ```

   Para `-in`, usar la URL del servidor de sellado de tiempo que proporciona la CA junto con el certificado Authenticode. Como alternativa, se puede usar la utilidad oficial de Microsoft `signtool` en Microsoft Windows.

   Si se tiene experiencia con docker, se puede usar la versión de `osslsigncode` incluida en la imagen de docker.

(nc-dev-generic-build-instructions)=
### Instrucciones genéricas de compilación

En comparación con versiones anteriores, compilar el cliente de sincronización de escritorio se ha vuelto más fácil. A diferencia de versiones anteriores, CSync, la biblioteca del motor de sincronización del cliente, ahora forma parte del repositorio de código fuente del cliente y no es un módulo aparte.

Para compilar la versión más actualizada del cliente:

1. Clonar las últimas versiones del cliente desde [Git][Git] de la siguiente manera:

   ```bash
   $ git clone git://github.com/nextcloud/client.git
   $ cd client
   $ git submodule update --init
   ```

2. Crear el directorio de compilación

   ```bash
   $ mkdir client-build
   $ cd client-build
   ```

3. Configurar la compilación del cliente

   ```bash
   $ cmake -DCMAKE_BUILD_TYPE="Debug" ..
   ```

   :::{note}
   Hay que usar rutas absolutas para los directorios `include` y `library`.
   :::

   :::{note}
   En macOS, hay que especificar `-DCMAKE_INSTALL_PREFIX=target`, donde `target` es una ubicación privada, es decir, paralela al directorio de compilación, especificando `../install`.
   :::

   :::{note}
   qtkeychain debe compilarse con el mismo prefijo, p. ej., `CMAKE_INSTALL_PREFIX=/Users/path/to/client/install/ .`
   :::

   :::{note}
   Ejemplo:: `cmake -DCMAKE_PREFIX_PATH=/usr/local/opt/qt6 -DCMAKE_INSTALL_PREFIX=/Users/path/to/client/install/`
   :::

4. Ejecutar `make`.

   El binario de Nextcloud aparecerá en el directorio `bin`.

5. (Opcional) Ejecutar `make install` para instalar el cliente en el directorio `/usr/local/bin`.

Los siguientes son parámetros de cmake conocidos:

- `QTKEYCHAIN_LIBRARY=/path/to/qtkeychain.dylib -DQTKEYCHAIN_INCLUDE_DIR=/path/to/qtkeychain/`: Se usa para las credenciales almacenadas. Al compilar con Qt5, la biblioteca se llama `qt5keychain.dylib.` Hay que compilar QtKeychain con la misma versión de Qt.
- `WITH_DOC=TRUE`: Crea la documentación y las páginas de manual al ejecutar `make`; además añade instrucciones de instalación, lo que permite instalar con `make install`.
- `CMAKE_PREFIX_PATH=/path/to/Qt6/6.7.0/yourarch/lib/cmake/`: Compila usando Qt6.
- `CMAKE_INSTALL_PREFIX=path`: Establece un prefijo de instalación. Es obligatorio en Mac OS

#### Sanitizador de direcciones

Se puede activar el sanitizador de direcciones para detectar corrupciones de memoria y otros errores. Están disponibles los siguientes sanitizadores:

- Sanitizador de direcciones
- Sanitizador de fugas
- Sanitizador de memoria
- Sanitizador de comportamiento indefinido
- Sanitizador de hilos

Se pueden activar uno o más sanitizadores mediante CMake. Por ejemplo, para activar el sanitizador de direcciones y el de comportamiento indefinido, ejecutar CMake así: `cmake .. -D ECM_ENABLE_SANITIZERS="address;undefined"`. Hay que tener en cuenta que no todas las combinaciones de sanitizadores funcionan juntas y que, en algunas plataformas, no están disponibles todos los tipos de sanitizadores. Por ejemplo, en Windows actualmente solo está disponible el sanitizador de direcciones. En Windows, hay que asegurarse de que el enlazador pueda encontrar las DLL de los sanitizadores en tiempo de ejecución. Si Visual Studio se instaló en la ubicación estándar, pueden encontrarse en **C:/ProgramFiles (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/Llvm/x64/lib/clang/10.0.0/lib/windows**. Asegurarse de añadir esta ubicación al path. También puede ser necesario [actualizar la versión de Visual Studio](https://docs.microsoft.com/en-us/cpp/sanitizers/asan?view=msvc-160#install-the-addresssanitizer).

:::{note}
Si se usa Visual Studio en Windows, se puede activar el sanitizador haciendo clic en **Manage Configurations**, desplazándose hasta la sección **CMake Command Arguments** e introduciendo luego `-D ECM_ENABLE_SANITIZERS="address"` en el campo de texto de debajo. Después, hacer clic en **Save and generate CMake cache to load variables**, justo encima de la tabla.
:::

[GitHub help article]: https://help.github.com/en/articles/which-remote-url-should-i-use
[brew.sh]: https://brew.sh
[a known issue]: https://stackoverflow.com/a/63241724
[CMake]: http://www.cmake.org/download
[CSync]: http://www.csync.org
[Client Download Page]: https://nextcloud.com/install/#install-clients
[Git]: http://git-scm.com
[OpenSSL Windows Build]: http://slproweb.com/products/Win32OpenSSL.html
[Qt]: http://www.qt.io/download
[Microsoft Authenticode]: https://msdn.microsoft.com/en-us/library/ie/ms537361%28v=vs.85%29.aspx
[QtKeychain]: https://github.com/frankosterfeld/qtkeychain
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
