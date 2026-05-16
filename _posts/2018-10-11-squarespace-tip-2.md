---
layout: post
title: "Squarespace Tips 002: cómo usar una fuente propia"
date: 2018-10-11 10:00:00 +0300
image: /images/115.jpg
image_alt: "Editor de CSS personalizado de Squarespace para cargar una fuente propia"
description: "Cómo cargar una fuente personalizada en Squarespace y aplicarla con CSS a títulos u otros elementos de la web."
resumen: "Usar una fuente propia en Squarespace es posible subiendo el archivo y declarando la tipografía con @font-face en CSS personalizado."
source: AJRA-v09/_posts/2018-10-11-squarespace-tip-2.md
---

Squarespace ofrece muchas fuentes listas para usar, pero a veces un proyecto necesita una tipografía concreta.

Puede ser una fuente de marca, una tipografía comprada o un archivo personalizado que el cliente quiere mantener para reforzar identidad visual.

En ese caso podemos cargar la fuente y aplicarla con CSS personalizado.

## Subir la fuente

Vamos a suponer que tenemos una fuente llamada `cubodekubrick` y queremos usarla en los títulos `h1` de la web.

Lo primero es subir el archivo de la fuente a Squarespace:

`Diseño > CSS personalizado > Gestionar archivos externos`

Desde ahí subimos el archivo de la fuente.

## Declarar la fuente con CSS

Después añadimos el CSS necesario en el área de CSS personalizado:

```
@font-face {
  font-family: "cubodekubrick";
  src: url("//xxxxxxxxxxxxxxxxxxxx");
}

h1 {
  font-family: "cubodekubrick";
}
```

Lo único que hay que cambiar es `xxxxxxxxxxxxxxxxxxxx`, que debe ser la URL generada por Squarespace para la fuente que acabamos de subir.

## Insertar la URL del archivo

Si no sabes cuál es la URL, puedes hacerlo así:

1. Selecciona `xxxxxxxxxxxxxxxxxxxx` dentro del código.
2. Haz clic en **Gestionar archivos externos**.
3. Selecciona la fuente que has subido.

Squarespace insertará la URL del archivo en el CSS.

Guardas los cambios y la fuente debería aplicarse a todos los títulos `h1`.

## Cuidado con rendimiento y licencias

Antes de subir una fuente, revisa dos cosas:

- Que tienes licencia para usarla en web.
- Que el archivo no pesa demasiado.

Las fuentes también afectan al rendimiento, y la velocidad web importa para experiencia y SEO. Si necesitas medirlo, puedes revisar la guía sobre [PageSpeed](/blog/pagespeed/).

Si quieres personalizar tu web en Squarespace sin romper diseño, rendimiento o SEO, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
