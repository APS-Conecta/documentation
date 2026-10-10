---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de AppAPI para registrar y anular ajustes declarativos de ExApps, desde Nextcloud 29, con un ejemplo de esquema de ajustes en Python."
---
(nc-dev-exapp_declarative_settings_section)=
# Ajustes declarativos

## Resumen

Esta página describe cómo AppAPI muestra los ajustes de una ExApp a partir de un esquema declarativo: los endpoints OCS para registrarlos y anular su registro, y un ejemplo de esquema de ajustes en Python con varios tipos de campo. Está dirigida a quienes desarrollan ExApps.

````{upstream} developer_manual/exapp_development/tech_details/api/settings.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
A partir de Nextcloud **29**, AppAPI ofrece la posibilidad de mostrar los ajustes de las ExApps.
Cuando un administrador o un usuario cambia algunos ajustes de una ExApp,
estos se almacenan en la base de datos y pueden obtenerse mediante la API {nc-doc}`developer_manual/exapp_development/tech_details/api/preferences` o {nc-doc}`developer_manual/exapp_development/tech_details/api/appconfig`.

:::{note}
Estos ajustes solo se muestran para las ExApps habilitadas.
:::

:::{warning}
El `section_id` del **esquema** ya debe estar registrado por alguna aplicación PHP.

**AppAPI** ofrece dos secciones que se pueden usar para ello: `ai_integration_team` y `declarative_settings`.
:::

### Registrar ajustes

Endpoint OCS: `POST /apps/app_api/api/v1/ui/settings`

#### Parámetros

Lista completa de parámetros (incluidos los opcionales):

```json
{
    "formScheme": "settings scheme"
}
```

### Anular el registro de la entrada de menú

Endpoint OCS: `DELETE /apps/app_api/api/v1/ui/settings`

#### Parámetros

```json
{
    "formId": "formId from scheme"
}
```

Ejemplo de esquema de ajustes en Python:

```python
{
    "id": "settings_example",
    "priority": 10,
    "section_type": "admin",
    "section_id": "ai_integration_team",
    "title": "AppAPI declarative settings",
    "description": "These fields are rendered dynamically from declarative schema",
    "fields": [
        {
            "id": "field1",
            "title": "Multi-selection",
            "description": "Select some option setting",
            "type": 'multi-select',
            "options": ["foo", "bar", "baz"],
            "placeholder": "Select some multiple options",
            "default": ["foo", "bar"],
        },
        {
            "id": "some_real_setting",
            'title': 'Choose init status check background job interval',
            'description': 'How often AppAPI should check for initialization status',
            'type': 'radio',
            'placeholder': 'Choose init status check background job interval',
            'default': '40m',
            'options': [
                {
                    'name': 'Each 40 minutes',
                    'value': '40m',
                },
                {
                    'name': 'Each 60 minutes',
                    'value': '60m',
                },
                {
                    'name': 'Each 120 minutes',
                    'value': '120m',
                },
                {
                    'name': 'Each day',
                    'value': f"{60 * 24}m",
                },
            ],
        },
        {
            'id': 'test_ex_app_field_1',
            'title': 'Default text field',
            'description': 'Set some simple text setting',
            'type': 'text',
            'placeholder': 'Enter text setting',
            'default': 'foo',
        },
        {
            'id': 'test_ex_app_field_1_1',
            'title': 'Email field',
            'description': 'Set email config',
            'type': 'email',
            'placeholder': 'Enter email',
            'default': '',
        },
        {
            'id': 'test_ex_app_field_1_2',
            'title': 'Tel field',
            'description': 'Set tel config',
            'type': 'tel',
            'placeholder': 'Enter your tel',
            'default': '',
        },
        {
            'id': 'test_ex_app_field_1_3',
            'title': 'Url (website) field',
            'description': 'Set url config',
            'type': url',
            'placeholder': 'Enter url',
            'default': '',
        },
        {
            'id': 'test_ex_app_field_1_4',
            'title': 'Number field',
            'description': 'Set number config',
            'type': 'number',
            'placeholder': 'Enter number value',
            'default': 0,
        },
        {
            'id': 'test_ex_app_field_2',
            'title': 'Password',
            'description': 'Set some secure value setting',
            'type': password',
            'placeholder': 'Set secure value',
            'default': '',
        },
        {
            'id': 'test_ex_app_field_3',
            'title': 'Selection',
            'description': 'Select some option setting',
            'type': 'select',
            'options': ['foo', 'bar', 'baz'],
            'placeholder': 'Select some option setting',
            'default': 'foo',
        },
        {
            'id': 'test_ex_app_field_4',
            'title': 'Toggle something',
            'description': 'Select checkbox option setting',
            'type': 'checkbox',
            'label': 'Verify something if enabled',
            'default': False,
        },
        {
            'id': 'test_ex_app_field_5',
            'title': 'Multiple checkbox toggles, describing one setting, checked options are saved as a JSON object {foo: true, bar: false}',
            'description': 'Select checkbox option setting',
            'type': 'multi-checkbox',
            'default': {'foo': True, 'bar': True},
            'options': [
                {
                    'name':'Foo',
                    'value': 'foo',
                },
                {
                    'name': 'Bar',
                    'value': 'bar',
                },
                {
                    'name': 'Baz',
                    'value': 'baz',
                },
                {
                    'name': 'Qux',
                    'value': 'qux',
                },
            ],
        },
        {
            'id': 'test_ex_app_field_6',
            'title': 'Radio toggles, describing one setting like single select',
            'description': 'Select radio option setting',
            'type': 'radio',
            'label': 'Select single toggle',
            'default': 'foo',
            'options': [
                {
                    'name': 'First radio',
                    'value': 'foo'
                },
                {
                    'name': 'Second radio',
                    'value': 'bar'
                },
                {
                    'name': 'Second radio',
                    'value': 'baz'
                },
            ],
        },
    ]
}
```
````
