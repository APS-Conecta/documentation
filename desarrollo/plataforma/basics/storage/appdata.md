---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "La carpeta AppData: un sistema de archivos simple y privado por app, cómo inyectar IAppData y los métodos de su raíz, sus carpetas y sus archivos."
---
# AppData

## Resumen

Esta página describe la carpeta AppData, que da a cada app un sistema de archivos simple y privado, cómo obtenerla inyectando `IAppData` y qué métodos ofrecen su raíz, sus carpetas y sus archivos. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/storage/appdata.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
A menudo una app quiere almacenar datos. Sin embargo, no todos los datos que se almacenan pertenecen a los archivos de los usuarios. A menudo solo se quiere un almacenamiento muy simple para tener algunos archivos temporales. Para facilitarlo existe la carpeta AppData, que proporciona a cada app un sistema de archivos simple y privado.

Su uso es casi trivial cuando la app usa el AppFramework.

```php
<?php

namespace OCA\MyApp\Controller\MyController;

use OCP\AppFramework\Controller;
use OCP\Files\IAppData;
use OCP\IRequest;

class MyController extends Controller {
    /** @var IAppData */
    private $appData;

    public function __construct($appName,
                                IRequest $request,
                                IAppData $appData) {
        parent::__construct($appName, $request);
        $this->appData = $appData;
    }
}
```

Esto da al controlador acceso al sistema de archivos simple IAppData de la app.

### El sistema de archivos simple

*IAppData* usa el sistema de archivos simple. Es un sistema de archivos muy simplificado que permite asignarlo fácilmente, por ejemplo, a memcaches. El sistema de archivos tiene tres elementos: *root*, *folder*, *file*.

El *root* solo puede contener carpetas. Y cada carpeta solo puede contener archivos. Se limita así para mantener las cosas simples y permitir asignarlo fácilmente a otros backends. Por ejemplo, un administrador de sistemas podría elegir asignar los avatares a un almacenamiento rápido, ya que se usan a menudo.

#### Raíz

El elemento raíz solo puede contener carpetas. Hay 3 cosas que se pueden hacer con un elemento raíz:

- *getFolder*: obtiene la carpeta que se solicita
- *newFolder*: crea una carpeta nueva
- *getDirectoryListing*: lista todas las carpetas de esta raíz

#### Carpeta

Una carpeta tiene algunas opciones más.

- *getDirectoryListing*: lista todos los archivos de la carpeta
- *fileExists*: comprueba si un archivo existe
- *getFile*: obtiene un archivo
- *newFile*: crea un archivo nuevo
- *delete*: elimina una carpeta y su contenido
- *getName*: obtiene el nombre de la carpeta

#### Archivo

- *getName*: obtiene el nombre del archivo
- *getSize*: obtiene el tamaño del archivo
- *getETag*: obtiene el ETag del archivo
- *getMTime*: obtiene la hora de modificación del archivo
- *getContent*: obtiene el contenido del archivo
- *putContent*: escribe contenido en el archivo
- *delete*: elimina el archivo
- *getMimeType*: obtiene el tipo MIME del archivo
- *read*: obtiene un recurso para leer el archivo
- *write*: obtiene un recurso para escribir en el archivo
````
