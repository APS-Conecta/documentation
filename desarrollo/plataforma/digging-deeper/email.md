---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo enviar correo electrónico desde una app con el componente de correo y la interfaz IMailer, y cómo añadir adjuntos en línea a un mensaje."
---
(nc-dev-email)=
# Correo electrónico

## Resumen

Esta página explica cómo enviar correo electrónico desde una app con el componente de correo, que se obtiene inyectando la interfaz `IMailer`, y cómo añadir adjuntos en línea a un mensaje. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/email.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud tiene un componente de correo para enviar correo electrónico desde una cuenta definida por la administración.

### Uso básico

El componente de correo se oculta tras la interfaz `\OCP\Mail\IMailer`, que puede {nc-ref}`inyectarse <dependency-injection>`:

**Archivo {file}`lib/Service/MailService.php`**:

```php
<?php

use OCP\Mail\IMailer;

class MailService {
    private IMailer $mailer;

    public function __construct(IMailer $mailer) {
        $this->mailer = $mailer;
    }

    public function notify(string $email): void {
        $message = $this->mailer->createMessage();
        $message->setSubject("Hello from Nextcloud");
        $message->setPlainBody("This is some text");
        $message->setHtmlBody(
            "<!doctype html><html><body>This is some <b>text</b></body></html>"
        );
        $message->setTo([$email]);
        $this->mailer->send($message);
    }
}
```

### Adjuntos en línea

Los adjuntos en línea pueden añadirse a un mensaje con `IMessage::attachInline`:

```php
/** @var IMessage $message */
$message->attachInline(
    "this is a test", // Body
    "test.txt",       // Name
    "text/plain"      // Content type
);
$this->mailer->send($message);
```
````
