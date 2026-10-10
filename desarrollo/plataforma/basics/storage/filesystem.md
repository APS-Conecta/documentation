---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo acceder al sistema de archivos desde una app con la API de nodos: leer y escribir archivos, almacenamiento directo, backends y puntos de montaje."
---
# API del sistema de archivos de Nextcloud

## Resumen

Esta página muestra cómo una app accede al sistema de archivos mediante la API de nodos a partir de `IRootFolder`: obtener la carpeta de un usuario, escribir y leer archivos, acceder directamente al almacenamiento y a su caché, implementar un backend de almacenamiento y agregar puntos de montaje. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/basics/storage/filesystem.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Guía de alto nivel para usar la API del sistema de archivos de Nextcloud.

Como los usuarios pueden elegir su backend de almacenamiento, al sistema de archivos se debe acceder mediante las clases de sistema de archivos adecuadas. Para un sistema de archivos simplificado para datos específicos de la app, ver {nc-doc}`IAppData <developer_manual/basics/storage/appdata>`

### API de nodos

La «API de nodos» es la API principal con la que las apps acceden al sistema de archivos de Nextcloud: cada elemento del sistema de archivos se representa como un nodo File o Folder,
y cada nodo da acceso a la información del sistema de archivos y a las acciones pertinentes
para ese nodo.

#### Obtener acceso

El acceso al sistema de archivos lo proporciona `IRootFolder`, que se puede inyectar en la clase.
Desde la carpeta raíz se puede acceder a la carpeta personal de un usuario o a un archivo o carpeta por su ruta absoluta.

```php
use OCP\Files\IRootFolder;
use OCP\IUserSession;

class FileSystemAccessExample {
    private IUserSession $userSession;
    private IRootFolder $rootFolder;

    public function __construct(IUserSession $userSession, IRootFolder $rootFolder) {
        $this->userSession = $userSession;
        $this->rootFolder = $rootFolder;
    }

    /**
    * Create a new file with specified content in the home folder of the current user
    * returning the size of the resulting file.
    */
    public function getCurrentUserFolder(string $path, string $content): int {
        $user = $this->userSession->getUser();

        if ($user === null) {
            return null;
        }

        // the "user folder" corresponds to the root of the user visible files
        return $this->rootFolder->getUserFolder($user->getUID());
    }
}
```

Para más detalles sobre los métodos específicos que proporcionan los nodos de archivo y de carpeta, ver la documentación de los métodos de las interfaces `OCP\Files\File` y `OCP\Files\Folder`.

#### Escribir en un archivo

Todos los métodos devuelven un objeto Folder en el que se puede acceder a archivos y carpetas, o realizar operaciones del sistema de archivos de forma relativa a su raíz. Por ejemplo, para escribir en {file}`nextcloud/data/myfile.txt` hay que obtener la carpeta raíz y usar:

```php
use OCP\Files\IRootFolder;

class FileWritingExample {

    private IRootStorage $storage;

    public function __construct(IRootFolder $storage){
        $this->storage = $storage;
    }

    public function writeContentToFile($content) {

        $userFolder = $this->storage->getUserFolder('myUser');

        // check if file exists and write to it if possible
        try {
            try {
                $file = $userFolder->get('myfile.txt');

                // the id can be accessed by $file->getId();
                $file->putContent($content);
            } catch(\OCP\Files\NotFoundException $e) {
                $userFolder->newFile('myfile.txt', $content);
            }

        } catch(\OCP\Files\NotPermittedException $e) {
            // you have to create this exception by yourself ;)
            throw new StorageException('Cant write to file');
        }
    }
}
```

#### Leer de un archivo

También se puede acceder a archivos y carpetas por su id, llamando al método **getById** de la carpeta.

```php
use OCP\Files\IRootFolder;

class FileReadingExample {

    private IRootFolder $storage;

    public function __construct(IRootFolder $storage){
        $this->storage = $storage;
    }

    public function getFileContent($id) {

        $userFolder = $this->storage->getUserFolder('myUser');

        // check if file exists and read from it if possible
        try {
            $file = $userFolder->getById($id);
            if ($file instanceof \OCP\Files\File) {
                return $file->getContent();
            } else {
                throw new StorageException('Can not read from folder');
            }
        } catch(\OCP\Files\NotFoundException $e) {
            throw new StorageException('File does not exist');
        }
    }
}
```

#### Acceso directo al almacenamiento

Aunque en general debe evitarse en favor de las API de más alto nivel,
a veces una app necesita comunicarse directamente con la implementación de almacenamiento de su caché de metadatos.

Se puede acceder al almacenamiento subyacente de un archivo o carpeta llamando a `getStorage` en el nodo, u obteniendo primero
el punto de montaje con `getMountPoint` y obteniendo el almacenamiento a partir de él.

Una vez obtenida la instancia del almacenamiento, se puede usar la API de almacenamiento de `OCP\Files\Storage\IStorage`; sin embargo, hay que tener en cuenta que
todas las rutas que usa la API de almacenamiento son internas al almacenamiento. El `IMountPoint` que devuelve `getMountPoint` proporciona
métodos para traducir entre rutas absolutas del sistema de archivos y rutas internas del almacenamiento.

Si se necesita consultar directamente los metadatos en caché, se puede obtener el `OCP\Files\Cache\ICache` del almacenamiento llamando a `getCache`.

#### Implementar un almacenamiento

La forma recomendada de implementar un backend de almacenamiento es heredar de `OC\Files\Storage\Common`, que proporciona
implementaciones de respaldo para varios métodos y reduce el trabajo necesario para implementar la API de almacenamiento completa.
Sin embargo, hay que tener en cuenta que varias de estas implementaciones de respaldo probablemente sean considerablemente menos eficientes que una
implementación del método optimizada para las capacidades del backend de almacenamiento.

#### Agregar puntos de montaje al sistema de archivos

La forma recomendada de agregar puntos de montaje propios al sistema de archivos desde una app es implementar `OCP\Files\Config\IMountProvider`
y registrar el proveedor mediante `OCP\Files\Config\IMountProviderCollection::registerProvider`.

Una vez registrado, el proveedor se llama cada vez que se configura el sistema de archivos para un usuario, y el proveedor de puntos de montaje
puede devolver una lista de puntos de montaje que agregar para ese usuario.
````
