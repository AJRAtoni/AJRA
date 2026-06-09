---
layout: post
title: "Squarespace Tips 008: cuándo usar !important en CSS"
date: 2019-06-23 10:00:00 +0300
image: /images/blog/152-2.jpg
image_alt: "Código CSS personalizado aplicado a una página creada en Squarespace"
description: "El modificador !important puede ayudarte a sobrescribir estilos en Squarespace, pero conviene usarlo con criterio para no complicar el mantenimiento del CSS."
card_subtitle: "En Squarespace, !important sirve para dar prioridad a una regla CSS cuando choca con estilos existentes."
resumen: "En Squarespace, !important sirve para dar prioridad a una regla CSS cuando choca con estilos existentes. Úsalo como recurso puntual, no como solución para todo."
source: AJRA-v09/_posts/2019-06-23-squarespace-tip-8.md
---

En el [tip anterior sobre CSS en Squarespace](/blog/squarespace-tip-7/) vimos cómo añadir estilos personalizados a una web.

El siguiente problema suele aparecer rápido: escribes una regla, la guardas, recargas la página y no cambia nada.

En muchos casos no es que el CSS esté mal escrito. Lo que ocurre es que entra en conflicto con estilos que **Squarespace** ya trae definidos en la plantilla.

Una forma de resolverlo es usar `!important`, una instrucción que le dice al navegador que esa regla tiene prioridad sobre otras reglas que afecten al mismo elemento.

## Un ejemplo sencillo

Imagina que tienes dos reglas para los párrafos:

```css
p {
  color: red;
}

p {
  color: black;
}
```

El navegador no puede mostrar el mismo texto en rojo y negro a la vez. En este caso, por cómo funciona la cascada de CSS, acabará aplicando el color negro.

Si quieres forzar el rojo, podrías escribir:

```css
p {
  color: red !important;
}

p {
  color: black;
}
```

Con `!important`, la primera regla gana aunque después aparezca otra que intenta cambiar el color.

## Cuándo usarlo en Squarespace

En webs como **Squarespace**, donde la plantilla ya carga su propia hoja de estilos, `!important` puede ser útil para pequeños ajustes visuales: colores, tamaños, márgenes o detalles concretos que la plantilla insiste en sobrescribir.

Pero no conviene usarlo por sistema. Si todo tu CSS acaba lleno de `!important`, cada cambio posterior será más difícil de mantener. Antes de añadirlo, revisa si puedes ser más específico con el selector o si estás apuntando al elemento correcto.

Esta idea conecta con otros ajustes básicos de diseño en Squarespace, como [cambiar el favicon](/blog/squarespace-tips-6/) o [personalizar colores de forma consistente](/blog/colorzilla/): pequeños detalles, pero con impacto en la percepción final de la web.

Si quieres revisar el CSS de tu web en Squarespace y ordenar los cambios sin romper la plantilla, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
