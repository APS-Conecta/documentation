---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Ejemplos en Java con la biblioteca android-library: credenciales, carpetas, archivos, descargas, subidas, movimientos y recursos compartidos."
---
# Ejemplos

## Resumen

Esta página reúne, para quienes desarrollan apps de Android, ejemplos de código Java de la biblioteca de Android de {vendor}`Nextcloud`: inicializar el cliente, establecer las credenciales, operar con archivos y carpetas y gestionar los recursos compartidos por enlace, junto con algunos consejos.

````{upstream} developer_manual/client_apis/android_library/examples.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

### Inicializar la biblioteca

Empezar a usar la biblioteca: es necesario inicializar el objeto mClient, que se encargará de mantener la comunicación con el servidor.

#### Ejemplo de código

```java
public class MainActivity extends Activity
                          implements  OnRemoteOperationListener,
                                      OnDatatransferProgressListener {
private OwnCloudClient mClient;
private Handler mHandler = new Handler();

...

public void onCreate(Bundle savedInstanceState) {

...

// Parse URI to the base URL of the Nextcloud server
Uri serverUri = Uri.parse(getString(R.string.server_base_url));

// Create client object to perform remote operations
mClient = OwnCloudClientFactory.createOwnCloudClient(
            serverUri,
            this,
            // Activity or Service context
            true);
```

### Establecer las credenciales

La autenticación en la app es posible mediante 3 métodos distintos:

- Autenticación básica, nombre de usuario y contraseña
- Token de acceso Bearer (oAuth2)
- Cookie (inicio de sesión único basado en SAML)

#### Ejemplo de código

```java
package com.owncloud.android.lib.common;

public class OwnCloudClient extends HttpClient {
  ...
  // Set basic credentials
  client.setCredentials(
      NextcloudCredentialsFactory.newBasicCredentials(username, password)
  );
  // Set bearer access token
  client.setCredentials(
      NextcloudCredentialsFactory.newBearerCredentials(accessToken)
  );
  // Set SAML2 session token
  client.setCredentials(
      NextcloudCredentialsFactory.newSamlSsoCredentials(cookie)
  );
}
```

### Crear una carpeta

Crear una carpeta nueva en el servidor de la nube; la información que hay que enviar es la ruta de la carpeta nueva.

#### Ejemplo de código

```java
private void startFolderCreation(String newFolderPath) {
  CreateRemoteFolderOperation createOperation = new CreateRemoteFolderOperation(newFolderPath, false);
  createOperation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof CreateRemoteFolderOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
  // …
}
```

### Leer una carpeta

Obtener el contenido de una carpeta existente en el servidor de la nube; la información que hay que enviar es la ruta de la carpeta; en el ejemplo mostrado se ha pedido el contenido de la carpeta raíz. Como respuesta de este método se recibirá un array con todos los archivos y carpetas almacenados en la carpeta seleccionada.

#### Ejemplo de código

```java
private void startReadRootFolder() {
  ReadRemoteFolderOperation refreshOperation = new ReadRemoteFolderOperation(FileUtils.PATH_SEPARATOR);
  // root folder
  refreshOperation.execute(mClient, this, mHandler);
}


@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof ReadRemoteFolderOperation) {
    if (result.isSuccess()) {
      List< RemoteFile > files = result.getData();
      // do your stuff here
    }
  }
  // …
}
```

### Leer un archivo

Obtener información relativa a un archivo o una carpeta determinados; la información obtenida es: `filePath`, `filename`, `isDirectory`, `size` y `date`.

#### Ejemplo de código

```java
private void startReadFileProperties(String filePath) {
  ReadRemoteFileOperation readOperation = new ReadRemoteFileOperation(filePath);
  readOperation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof ReadRemoteFileOperation) {
    if (result.isSuccess()) {
      RemoteFile file = result.getData()[0];
      // do your stuff here
    }
  }
  // …
}
```

### Eliminar un archivo o una carpeta

Eliminar un archivo o una carpeta en el servidor de la nube. La información necesaria es la ruta de la carpeta/archivo que se va a eliminar.

#### Ejemplo de código

```java
private void startRemoveFile(String filePath) {
  RemoveRemoteFileOperation removeOperation = new RemoveRemoteFileOperation(remotePath);
  removeOperation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof RemoveRemoteFileOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
  // …
}
```

### Descargar un archivo

Descargar un archivo existente en el servidor de la nube. La información necesaria es la ruta del archivo en el servidor y targetDirectory, la ruta donde se almacenará el archivo en el dispositivo.

#### Ejemplo de código

```java
private void startDownload(String filePath, File targetDirectory) {
  DownloadRemoteFileOperation downloadOperation = new DownloadRemoteFileOperation(filePath, targetDirectory.getAbsolutePath());
  downloadOperation.addDatatransferProgressListener(this);
  downloadOperation.execute( mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof DownloadRemoteFileOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
}

@Override
public void onTransferProgress(long progressRate, long totalTransferredSoFar, long totalToTransfer, String fileName) {
mHandler.post( new Runnable() {
  @Override
  public void run() {
    // do your UI updates about progress here
  }
});
}
```

### Subir un archivo

Subir un archivo nuevo al servidor de la nube. La información necesaria es fileToUpload, la ruta donde está almacenado el archivo en el dispositivo; remotePath, la ruta donde se almacenará el archivo en el servidor; y mimeType.

#### Ejemplo de código

```java
private void startUpload(File fileToUpload, String remotePath, String mimeType) {
  UploadRemoteFileOperation uploadOperation = new UploadRemoteFileOperation(fileToUpload.getAbsolutePath(), remotePath, mimeType);
  uploadOperation.addDatatransferProgressListener(this);
  uploadOperation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof UploadRemoteFileOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
}

@Override
public void onTransferProgress(long progressRate, long totalTransferredSoFar, long totalToTransfer, String fileName) {
  mHandler.post(new Runnable() {
    @Override
    public void run() {
      // do your UI updates about progress here
    }
  });
}
```

### Mover un archivo o una carpeta

Mover un archivo o una carpeta existentes a otra ubicación en el servidor Nextcloud. Los parámetros necesarios son la ruta del archivo o la carpeta que se va a mover y la nueva ruta deseada para él. La carpeta superior de la nueva ruta debe existir en el servidor.

Cuando el parámetro 'overwrite' vale 'true', el archivo o la carpeta se mueve aunque la nueva ruta ya esté ocupada por otro archivo o carpeta. Este será reemplazado por el primero.

#### Ejemplo de código

```java
private void startFileMove(String filePath, String newFilePath, boolean overwrite) {
  MoveRemoteFileOperation moveOperation = new MoveRemoteFileOperation(filePath, newFilePath, overwrite);
  moveOperation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof MoveRemoteFileOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
  // …
}
```

### Leer los elementos compartidos por enlace

Obtener información sobre qué archivos y carpetas se comparten por enlace (el objeto mClient contiene la información sobre la URL del servidor y la cuenta).

#### Ejemplo de código

```java
private void startAllSharesRetrieval() {
  GetRemoteSharesOperation getSharesOp = new GetRemoteSharesOperation();
  getSharesOp.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof GetRemoteSharesOperation) {
    if (result.isSuccess()) {
      ArrayList< OCShare > shares = new ArrayList< OCShare >();
      for (Object obj: result.getData()) {
        shares.add((OCShare) obj);
      }
      // do your stuff here
    }
  }
}
```

### Obtener los recursos compartidos de un archivo o una carpeta

Obtener información sobre qué archivos y carpetas se comparten por enlace en una carpeta determinada. La información necesaria es filePath, la ruta del archivo/carpeta en el servidor; la variable booleana getReshares procede de la API de Compartición y, por el momento, no se usa dentro de la biblioteca de Android de {vendor}`Nextcloud`.

#### Ejemplo de código

```java
private void startSharesRetrievalForFileOrFolder(String filePath, boolean getReshares) {
  GeteRemoteSharesForFileOperation operation = new GetRemoteSharesForFileOperation(filePath, getReshares, false);
  operation.execute(mClient, this, mHandler);
}

private void startSharesRetrievalForFilesInFolder(String folderPath, boolean getReshares) {
  GetRemoteSharesForFileOperation operation = new GetRemoteSharesForFileOperation(folderPath, getReshares, true);
  operation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof GetRemoteSharesForFileOperation) {
    if (result.isSuccess()) {
      ArrayList< OCShare > shares = new ArrayList< OCShare >();
      for (Object obj: result.getData()) {
        shares.add((OCShare) obj);
      }
      // do your stuff here
   }
}
}
```

### Compartir por enlace un archivo o una carpeta

Compartir por enlace un archivo o una carpeta del propio servidor de la nube.

La información necesaria es filePath, la ruta del elemento que se quiere compartir, y Password; este procede de la API de Compartición y, por el momento, no se usa dentro de la biblioteca de Android de {vendor}`Nextcloud`.

#### Ejemplo de código

```java
private void startCreationOfPublicShareForFile(String filePath, String password) {
  CreateRemoteShareOperation operation = new CreateRemoteShareOperation(filePath, ShareType.PUBLIC_LINK, "", false, password, 1);
  operation.execute(mClient, this, mHandler);
}

private void startCreationOfGroupShareForFile(String filePath, String groupId) {
  CreateRemoteShareOperation operation = new CreateRemoteShareOperation(filePath, ShareType.GROUP, groupId, false , "", 31);
  operation.execute(mClient, this, mHandler);
}

private void startCreationOfUserShareForFile(String filePath, String userId) {
  CreateRemoteShareOperation operation = new CreateRemoteShareOperation(filePath, ShareType.USER, userId, false, "", 31);
  operation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof CreateRemoteShareOperation) {
    if (result.isSuccess()) {
      OCShare share = (OCShare) result.getData().get(0);
      // do your stuff here
    }
  }
}
```

### Eliminar un recurso compartido

Dejar de compartir por enlace un archivo o una carpeta del propio servidor de la nube.

La información necesaria es el objeto OCShare que se quiere dejar de compartir por enlace.

#### Ejemplo de código

```java
private void startShareRemoval(OCShare share) {
  RemoveRemoteShareOperation operation = new RemoveRemoteShareOperation((int) share.getIdRemoteShared());
  operation.execute(mClient, this, mHandler);
}

@Override
public void onRemoteOperationFinish(RemoteOperation operation, RemoteOperationResult result) {
  if (operation instanceof RemoveRemoteShareOperation) {
    if (result.isSuccess()) {
      // do your stuff here
    }
  }
}
```

### Consejos

- Las credenciales deben establecerse antes de llamar a cualquier método
- Las rutas no deben estar en codificación URL
- Ruta correcta: `https://example.com/nextcloud/remote.php/dav/PopMusic`
- Ruta incorrecta: `https://example.com/nextcloud/remote.php/dav/Pop%20Music/`
- Hay algunos caracteres prohibidos en los nombres de carpetas y archivos en el servidor, y lo mismo en la biblioteca de Android de {vendor}`Nextcloud`: "\\","/","<",">",":",""","|","?","*"
- Las acciones de subida y descarga se pueden cancelar gracias a los objetos uploadOperation.cancel(), downloadOperation.cancel()
- Pruebas unitarias: antes de lanzar las pruebas unitarias hay que introducir la información de la propia cuenta (URL del servidor, usuario y contraseña) en TestActivity.java
````
