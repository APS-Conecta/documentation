---
tipo: guia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo una app registra configuraciones de administración y ajustes personales: la clase ISettings con su plantilla, una sección y su registro en info.xml."
---
(nc-dev-settings-section)=
# Ajustes

## Resumen

Esta página explica cómo una app registra configuraciones de administración y ajustes personales: la clase que implementa `\OCP\Settings\ISettings` con su plantilla, una sección propia con `\OCP\Settings\IIconSection` y el registro de ambas en el info.xml de la app. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/digging_deeper/settings.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
- {nc-doc}`developer_manual/digging_deeper/declarative_settings`

Una app puede registrar tanto configuraciones de administración como ajustes personales.
Los ajustes se dividen en secciones para agrupar los ajustes similares.
Por ejemplo, en la sección **Compartir** solo hay ajustes (integrados y de apps)
relacionados con el uso compartido.

### Formulario de ajustes

Para que los ajustes aparezcan, se necesitan tres cosas:

1. Una clase que implemente `\OCP\Settings\ISettings`
2. Una plantilla
3. La clase implementadora indicada en el info.xml de la app

A continuación se muestra un ejemplo de una clase que implementa la interfaz ISettings. Se basa
en la solución de survey_client.

```php
<?php
namespace OCA\YourAppNamespace\Settings;

use OCA\YourAppNamespace\Collector;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\BackgroundJob\IJobList;
use OCP\IConfig;
use OCP\IDateTimeFormatter;
use OCP\IL10N;
use OCP\Settings\ISettings;

class AdminSettings implements ISettings {

        /** @var Collector */
        private $collector;

        /** @var IConfig */
        private $config;

        /** @var IL10N */
        private $l;

        /** @var IDateTimeFormatter */
        private $dateTimeFormatter;

        /** @var IJobList */
        private $jobList;

        /**
         * Admin constructor.
         *
         * @param Collector $collector
         * @param IConfig $config
         * @param IL10N $l
         * @param IDateTimeFormatter $dateTimeFormatter
         * @param IJobList $jobList
         */
        public function __construct(Collector $collector,
                                                                IConfig $config,
                                                                IL10N $l,
                                                                IDateTimeFormatter $dateTimeFormatter,
                                                                IJobList $jobList
        ) {
                $this->collector = $collector;
                $this->config = $config;
                $this->l = $l;
                $this->dateTimeFormatter = $dateTimeFormatter;
                $this->jobList = $jobList;
        }

        /**
         * @return TemplateResponse
         */
        public function getForm() {

                $lastSentReportTime = (int) $this->config->getAppValue('survey_client', 'last_sent', 0);
                if ($lastSentReportTime === 0) {
                        $lastSentReportDate = $this->l->t('Never');
                } else {
                        $lastSentReportDate = $this->dateTimeFormatter->formatDate($lastSentReportTime);
                }

                $lastReport = $this->config->getAppValue('survey_client', 'last_report', '');
                if ($lastReport !== '') {
                        $lastReport = json_encode(json_decode($lastReport, true), JSON_PRETTY_PRINT);
                }

                $parameters = [
                        'is_enabled' => $this->jobList->has('OCA\Survey_Client\BackgroundJobs\MonthlyReport', null),
                        'last_sent' => $lastSentReportDate,
                        'last_report' => $lastReport,
                        'categories' => $this->collector->getCategories()
                ];

                return new TemplateResponse('yourappid', 'admin', $parameters);
        }

        /**
         * The section ID, e.g. 'sharing'
         *
         * @return string
         */
        public function getSection() {
                return 'survey_client';
        }

        /**
         * Whether the form should be rather on the top or bottom of
         * the admin section. The forms are arranged in ascending order of the
         * priority values. It is required to return a value between 0 and 100.
         *
         * @return int
         */
        public function getPriority() {
                return 50;
        }

}
```

Los parámetros del constructor se resolverán y se creará una instancia
automáticamente cuando se necesite, de modo que quien desarrolla no tiene que ocuparse de ello.

`getSection` debe devolver el ID de la sección de administración deseada.
Actualmente, los valores integrados son `server`, `sharing`, `encryption`,
`logging`, `additional` y `tips-tricks`. Las apps pueden registrar secciones
propias (ver más abajo), y también registrarse en secciones de otras apps.

`getPriority` se usa para ordenar los formularios dentro de una sección. Cuanto menor sea el valor,
más arriba aparecerá, y viceversa. El resultado depende de las
prioridades de los demás ajustes.

Nextcloud buscará las plantillas en una carpeta de plantillas ubicada en el directorio raíz
de la app. Siempre debe terminar en .php; en este caso, `templates/admin.php`
sería la ruta relativa final.

```php
<?php
/** @var $l \OCP\IL10N */
/** @var $_ array */

script('myappid', 'admin');         // adds a JavaScript file
style('survey_client', 'admin');    // adds a CSS file
?>

<div id="survey_client" class="section">
        <h2><?php p($l->t('Your app')); ?></h2>

        <p>
                <?php p($l->t('Only administrators are allowed to click the red button')); ?>
        </p>

        <button><?php p($l->t('Click red button')); ?></button>

        <p>
                <input id="your_app_magic" name="your_app_magic"
                           type="checkbox" class="checkbox" value="1" <?php if ($_['is_enabled']): ?> checked="checked"<?php endif; ?> />
                <label for="your_app_magic"><?php p($l->t('Do some magic')); ?></label>
        </p>

        <h3><?php p($l->t('Things to define')); ?></h3>
        <?php
        foreach ($_['categories'] as $category => $data) {
                ?>
                <p>
                        <input id="your_app_<?php p($category); ?>" name="your_app_<?php p($category); ?>"
                                   type="checkbox" class="checkbox your_app_category" value="1" <?php if ($data['enabled']): ?> checked="checked"<?php endif; ?> />
                        <label for="your_app_<?php p($category); ?>"><?php print_unescaped($data['displayName']); ?></label>
                </p>
                <?php
        }
        ?>

        <?php if (!empty($_['last_report'])): ?>

        <h3><?php p($l->t('Last report')); ?></h3>

        <p><textarea title="<?php p($l->t('Last report')); ?>" class="last_report" readonly="readonly"><?php p($_['last_report']);?></textarea></p>

        <em class="last_sent"><?php p($l->t('Sent on: %s', [$_['last_sent']])); ?></em>

        <?php endif; ?>

</div>
```

Después, la clase implementadora debe agregarse al info.xml. Los ajustes se
registrarán al instalar y al actualizar. Cuando se agregan ajustes a una app existente,
instalada y habilitada, hay que asegurarse de que se incremente la versión
para que Nextcloud pueda registrar la clase. Solo es posible registrar
una clase que implemente ISettings.

Para ver un ejemplo más complejo que usa plantillas incrustadas, consultar la
implementación de la app **user_ldap**.

### Sección

También es posible que una app registre su propia sección. Esto solo debe hacerse
si no hay ninguna sección correspondiente adecuada y el formulario de ajustes de la app
ocupa mucho espacio en pantalla. En caso contrario, registrarse en "additional".

Básicamente, funciona igual que con el formulario de ajustes. Solo hay dos
diferencias. En primer lugar, la interfaz que debe implementarse es `\OCP\Settings\IIconSection`.

Un ejemplo de implementación de la interfaz IIconSection:

```php
<?php
namespace OCA\YourAppNamespace\Settings;

use OCP\IL10N;
use OCP\IURLGenerator;
use OCP\Settings\IIconSection;

class AdminSection implements IIconSection {

        /** @var IL10N */
        private $l;

        /** @var IURLGenerator */
        private $urlGenerator;

        public function __construct(IL10N $l, IURLGenerator $urlGenerator) {
                $this->l = $l;
                $this->urlGenerator = $urlGenerator;
        }

        /**
         * Returns the ID of the section. It is supposed to be a lowercase string
         *
         * @returns string
         */
        public function getID() {
                return 'yourappid'; //or a generic id if feasible
        }

        /**
         * Returns the translated name as it should be displayed, e.g. 'LDAP / AD
         * integration'. Use the L10N service to translate it.
         *
         * @return string
         */
        public function getName() {
                return $this->l->t('Translatable Section Name');
        }

        /**
         * Whether the form should be rather on the top or bottom of
         * the settings navigation. The sections are arranged in ascending order of
         * the priority values. It is required to return a value between 0 and 99.
         *
         * @return int
         */
        public function getPriority() {
                return 80;
        }

        /**
         * The relative path to an icon describing the section
         *
         * @return string
         */
        public function getIcon() {
                return $this->urlGenerator->imagePath('yourapp', 'icon.svg');
        }

}
```

Además, la sección debe registrarse en el info.xml de la app.

### Registrar ajustes y secciones

Como ya se mencionó, tanto los ajustes como las secciones deben registrarse en el info.xml de la app.
Esto es bastante sencillo, como se ve en el fragmento de código siguiente:

```xml
...
<settings>
    <admin>OCA\YourAppNamespace\Settings\Admin</admin>
    <admin-section>OCA\YourAppNamespace\Settings\AdminSection</admin-section>
    <personal>OCA\YourAppNamespace\Settings\Personal</personal>
    <personal-section>OCA\YourAppNamespace\Settings\PersonalSection</personal-section>
</settings>
...
```
````
