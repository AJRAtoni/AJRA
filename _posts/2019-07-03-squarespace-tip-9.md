---
layout: post
title: "Squarespace Tips 009: cómo crear anchor links"
date: 2019-07-03 10:00:00 +0300
image: /images/152.jpg
image_alt: "Página creada en Squarespace con secciones enlazadas mediante anchor links"
description: "Los anchor links permiten llevar al usuario a una sección concreta dentro de una misma página. Así puedes crearlos en Squarespace sin complicarte."
card_subtitle: "Un anchor link es un enlace interno a una sección concreta de una página."
resumen: "Un anchor link es un enlace interno a una sección concreta de una página. En Squarespace ayuda a mejorar navegación, landing pages y páginas largas."
source: AJRA-v09/_posts/2019-07-03-squarespace-tip-9.md
---

Seguimos con los **Squarespace Tips**. En esta ocasión vamos a ver qué es un anchor link y cómo crearlo en **Squarespace**.

## Qué es un anchor link

Un anchor link, o enlace de anclaje, es un enlace que lleva al usuario a un punto concreto dentro de una página.

Un enlace normal suele abrir otra página. Un anchor link sirve para moverte dentro de la misma página, por ejemplo desde un índice hasta una sección, desde un botón hasta un formulario o desde una llamada a la acción hasta una tabla de precios.

Son especialmente útiles en [landing pages](/blog/landing-page/), páginas largas de servicios y contenidos con varias secciones.

## Cómo crear un anchor link en Squarespace

### 1. Crea el enlace

Primero necesitas un enlace sobre el que el usuario pueda hacer clic. Puede ser texto, un botón o cualquier elemento que permita añadir una URL.

En un bloque de texto, selecciona el texto, haz clic en el icono de enlace y elige la opción de enlace externo.

### 2. Define un ID único

El ID es el nombre del punto al que quieres saltar. Debe empezar con `#` cuando lo usas como enlace:

```text
#anchor-link-example
```

Ese texto puede ser el que quieras, pero evita espacios. Lo más limpio es separar palabras con guiones. Ten en cuenta también que los anchor links distinguen entre mayúsculas y minúsculas.

### 3. Añade la URL completa si hace falta

Si enlazas dentro de la misma página, muchas veces bastará con `#anchor-link-example`.

Si enlazas desde otra página, usa la URL completa de destino:

```text
https://examplesite.com/pagina/#anchor-link-example
```

### 4. Coloca el ID en la sección de destino

Ahora tienes que marcar el lugar al que debe llegar el enlace.

En Squarespace puedes hacerlo con un bloque de código colocado justo antes de la sección de destino:

```html
<div id="anchor-link-example"></div>
```

También puedes asignarlo a un elemento concreto:

```html
<p id="anchor-link-example">Aquí empieza la sección.</p>
```

### 5. Guarda y prueba

Guarda los cambios, abre la página publicada y prueba el enlace. Si no funciona, revisa tres cosas: que el ID sea exactamente igual, que no tenga espacios y que el enlace no esté configurado para abrir en una ventana nueva.

Este tip encaja muy bien con otros ajustes de estructura en Squarespace, como [personalizar CSS](/blog/squarespace-tip-7/) o usar `!important` solo cuando toca en [reglas CSS concretas](/blog/squarespace-tip-8/).

Si quieres mejorar la navegación de una página larga o revisar una landing en Squarespace, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
