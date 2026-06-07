---
layout: post
title: "Código CSS para aplicar modo oscuro en una web"
date: 2020-02-18 10:00:00 +0300
image: /images/190.jpg
image_alt: "Ejemplo de una web adaptada a modo claro y modo oscuro"
description: "Con prefers-color-scheme puedes adaptar los colores de una web al modo claro u oscuro configurado en el dispositivo del usuario."
card_subtitle: "El modo oscuro en web no consiste en invertir colores: hay que usar CSS."
resumen: "El modo oscuro en web no consiste en invertir colores: hay que usar CSS, cuidar contraste y adaptar componentes para que la experiencia sea cómoda."
source: AJRA-v09/_posts/2020-02-28-modo-oscuro.md
---

El modo oscuro dejó de ser una rareza y pasó a estar integrado en sistemas operativos, apps y webs.

En una página web se puede detectar la preferencia del usuario con la media query `prefers-color-scheme`.

## Qué hace prefers-color-scheme

`prefers-color-scheme` permite saber si el usuario tiene configurado modo claro u oscuro en su dispositivo.

Las opciones habituales son:

- `no-preference`
- `light`
- `dark`

<figure>
<img src="/images/190-1.jpg" alt="Ejemplo visual de modo oscuro aplicado a una interfaz web" />
</figure>

## Ejemplo básico

Este sería un ejemplo mínimo:

```css
body {
  background: #ffffff;
  color: #111111;
}

@media (prefers-color-scheme: dark) {
  body {
    background: #111111;
    color: #f5f5f5;
  }
}
```

Con ese código, la web mantiene colores claros por defecto y cambia a fondo oscuro cuando el dispositivo indica que el usuario prefiere modo oscuro.

## No basta con invertir colores

Un buen modo oscuro necesita revisar:

- Contraste del texto.
- Estados de botones.
- Bordes y fondos de tarjetas.
- Formularios.
- Imágenes con fondo transparente.
- Logotipos.
- Sombras.

Si no se hace con cuidado, el modo oscuro puede empeorar la legibilidad.

También hay que vigilar rendimiento y CSS innecesario, igual que haríamos al revisar [PageSpeed](/blog/pagespeed/) o ajustes visuales en herramientas como [Elementor 2.8](/blog/elementor-28/).

El modo oscuro llegó también a apps populares como [WhatsApp](/blog/whatsapp-oscuro/) y clientes de correo como [Spark](/blog/spark-update-2019/), así que la web no podía quedarse atrás.

Si quieres implementar modo oscuro en tu web sin romper legibilidad, marca o rendimiento, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
