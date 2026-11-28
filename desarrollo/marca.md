---
tipo: referencia
audiencia: desarrollo
apps: [gestion-aio]
resumen: "El manual de marca de APS Conecta: la paleta por roles, la tipografía, el logotipo, los iconos, las licencias y el lema."
---
# Marca

## Resumen

Esta página es el manual de marca de APS Conecta y la única fuente de sus reglas. Los valores viven en la ficha de tokens de marca de la suite, `aps/brand/tokens.css` de gestion-aio: la tabla de la paleta se genera desde esa ficha en cada compilación, y este sitio toma de ella sus colores y sus fuentes.

APS Conecta es gratuito, de código abierto, sin fines de lucro y sin publicidad, y no maneja datos de pacientes.

Dentro de la suite, la interfaz se arma con componentes de `@nextcloud/vue`, que toman la marca de las variables del tema ({doc}`tema`). Las aplicaciones nunca usan los tokens de marca ni colores literales. Los componentes `.aps-*` del sitio web no se usan dentro de Nextcloud.

## Tabla

### Paleta

Cada rol tiene sus usos permitidos. El contraste es sobre blanco, según la fórmula de WCAG 2.

```{include} ../_generated/marca-paleta.md
```

Cada par de texto y fondo cumple el nivel AA de WCAG.

### Tipografía

- Fraunces es para títulos y cifras; Nunito Sans, para todo lo demás, controles de formulario incluidos.
- Ambas son fuentes variables bajo la licencia SIL OFL 1.1, autohospedadas y sin Google Fonts. Sus archivos nunca se reducen a un subconjunto ni se renombran: es una condición de la OFL.
- Los pesos son 400, 600, 700 y 800.
- Los títulos llevan un espaciado entre letras de `-0.015em`.

| Estilo | Tamaño | Peso |
|---|---|---|
| display 4xl | `3.75rem` | 600 |
| display 2xl | `2rem` | 600 |
| display xl | `1.375rem` | 600 |
| text lg | `1.125rem` | 400 |
| text base | `1rem` | 400 |
| label sm | `0.8125rem` | 800 |

Dentro de Nextcloud, la base sigue siendo la de Nextcloud: 15 px con un interlineado de 1,5.

### Logotipo

El logotipo es el Ofiuco, la constelación del portador de la serpiente y símbolo clásico de la medicina: una red de estrellas conectadas con la serpiente dorada, sobre una baldosa con degradado violeta, coronada por la estrella guía dorada.

- El espacio libre alrededor de la baldosa mide lo que la estrella guía.
- El tamaño mínimo es de 24 px en un favicon y de 32 px en una interfaz.
- La serpiente y la estrella nunca se recolorean, y el logotipo nunca se rota, se deforma ni lleva sombras.
- Sobre una fotografía o un color se usa el logotipo de un solo color.
- Las páginas de error muestran el Ofiuco oficial sin recuadro blanco.
- Un logotipo animado respeta la preferencia de movimiento reducido.

Los logotipos que distribuye la suite:

```{figure} ../_generated/brand/img/logo/logo.svg
:alt: El Ofiuco sobre su baldosa violeta
:width: 142px

El logotipo, `aps/theme/apsconecta/core/img/logo.svg`.
```

```{figure} ../_generated/brand/img/logo/logo-header.svg
:alt: El Ofiuco sin baldosa, sobre el violeta oscuro de la barra superior
:width: 48px
:class: aps-sobre-violeta

El logotipo de la barra superior, `aps/theme/apsconecta/core/img/logoheader.svg`.
```

```{figure} ../_generated/brand/img/favicon.svg
:alt: El favicon del Ofiuco
:width: 32px

El favicon, `aps/brand/favicon.svg`.
```

### Iconos

Las aplicaciones usan glifos de un solo color de Material Design Icons, el conjunto que usa `@nextcloud/vue`.

### Licencias

- La ficha de tokens de marca, el CSS y los logotipos llevan la licencia que fija {doc}`licencias`.
- Las fuentes, la OFL 1.1: nunca se reducen a un subconjunto ni se renombran.
- Los conjuntos de iconos, MIT o Apache-2.0, conservando su aviso.
- El tema y las aplicaciones propias, AGPL-3.0-or-later.

### Lema

El lema es «La salud que compartimos es la que mejora», como lo fija el glosario de la suite (`CONTEXT.md` de gestion-aio). La variante «La salud primaria que compartimos es la que mejora» no se usa.
