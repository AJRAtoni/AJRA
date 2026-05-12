---
layout: post
title: SQUARESPACE TIPS 008 — La importancia del !Important
date: 2019-06-23 10:00:00 +0300
image: /images/152-2.jpg
source: AJRA-v09/_posts/2019-06-23-squarespace-tip-8.md
---

En el Tip anterior os explicábamos que es el código CSS y cómo usarlo en **Squarespace**.

Muchos lo habéis probado y a algunos no os ha funcionado correctamente.

Esto puede suceder cuando utilizas algún código CSS que entre en conflicto con el código preexistente en **Squarespace**.

Para solucionar este problema hay que indicarle a tu sitio web que el código CSS que estás añadiendo es importante y tiene prioridad sobre el resto.

Eso lo hacemos utilizando el atributo !important.

## Vamos con un ejemplo:

En el siguiente ejemplo primero le estamos diciendo a la web que muestre el texto en rojo y acto seguido le decimos que lo muestre en negro.

```
p { color: red; } p { color: black; }
```

Como es lógico la web no puede mostrar el texto en dos colores al mismo tiempo, y por cómo funciona el código CSS la última orden es la que tiene efecto, así que en este ejemplo el texto se mostrará en negro.

En ejemplo anterior podríamos usar el atributo !important para forzar que se mostrase en rojo.

```
p { color: red !important; } p { color: black; }
```

En webs como **Squarespace**, las cuales ya tienen su hoja de estilos CSS preconfigurada tendremos que usar en muchas ocasiones el atributo !important para que nuestro CSS personalizado surja efecto.

Y recuerda, en caso de que necesites ayuda con tu web en **Squarespace** y su código CSS [puedes contactar conmigo](mailto:info@ajra.es).