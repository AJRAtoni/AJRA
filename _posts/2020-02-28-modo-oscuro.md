---
layout: post
title: Código para aplicar el “Modo Oscuro” en tu web.
date: 2020-02-18 10:00:00 +0300
image: /images/190.jpg
source: AJRA-v09/_posts/2020-02-28-modo-oscuro.md
---

Últimamente esta muy de moda lo del “Modo Oscuro”.
La mayoría de los dispositivo ya vienen con la opción a nivel de OS de configurar el “modo oscuro” para que las aplicaciones adapten sus colores dependiendo de cómo lo tengamos configurado.

## ¿Pero qué pasa con las páginas web?
Bien, pues hoy os traigo un sencillo código CSS mediante el cual podremos hacer que los colores de nuestra web se adapten al “modo oscuro” dependiendo de la configuración del dispositivo de cada usuario.

Lo que tendremos que usar él la función *prefers-color-scheme*.
La cual nos permitirá detectar si un usuario tiene activado o no el modo oscuro.

<figure>
<img src="/images/190-1.jpg" alt="" />
</figure>

## PREFERS-COLOR-SCHEME
El prefers-color-scheme tiene tres opciones:

prefers-color-scheme: no-preference
prefers-color-scheme: Light
prefers-color-scheme: Dark

Vamos a ver un ejemplo:

```
@media (prefers-color-scheme: dark) { 
.body.dark-scheme { 
height: 100%;
background: black;
color: white;
}
```

Con este código le estaremos diciendo al navegador que si el dispositivo tiene el “modo oscuro” (Dark) modifique el color de fondo a negro y el texto a blanco.

---

Os animo a probar y experimentar con el código prefers-color-scheme.

Por si lo necesitáis os dejo [un código de ejemplo en mis CodePen’s](https://codepen.io/AJRA_TONI/pen/ExYKrZd).

---

Y recordad, si necesita ayuda para implementar el modo oscuro en vuestras webs [podéis contactar conmigo](mailto:info@ajra.es) y os ayudaré en todo lo posible.
