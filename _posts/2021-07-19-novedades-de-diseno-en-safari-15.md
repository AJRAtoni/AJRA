---
title: Novedades de diseño en Safari 15
description: He estado revisando las novedades de Safari 15 presentadas en la #WWDC21
image: https://cdn-images-1.medium.com/max/800/0*2HOAArFwCXuZ7IUw.jpeg
slug: novedades-de-diseno-en-safari-15
date: 2021-07-19T07:00:00.000Z
---

He estado revisando las [novedades de Safari 15](https://developer.apple.com/videos/play/wwdc2021/10029/) presentadas en la #WWDC21

Dejo por aquí una recopilación de las novedades más destacadas.

Safari 15 se actualiza en todas sus versiones: iOS, iPadOS y macOS.

La interfaz se ha rediseñado e incorpora la posibilidad de cambiar el color de la barra de navegación para fusionarse con tu web.

Para conseguir esto tenemos que añadir una línea de código a nuestra web.

Es tan sencillo como añadir este metatag en el `<Head>`.

Si en nuestra web usamos el modo oscuro también podemos utilizar un código para que la toolbar de Safari de adapte.

Si nosotros no añadimos la metatag a nuestra web, Safari intentará cambiar el color de la toolbar al que considere que se adapte mejor a nuestra web.

Como curiosidad, si el sistema detecta que el color elegido interfiere con la usabilidad (colores iguales al icono de cerrar ventana, o minimizar), Safari cambiará el color de la toolbar automáticamente.

El color de la toolbar de Safari 15 puede ser diferente en cada página de tu web.

Esto lo puedes hacer cambiando el código en el `<Head>` de tu HTML o mediante JavaScript.

En iOS 15 la barra de navegación ha cambiado por completo.

Ahora está en la parte de abajo, es más fácil de alcanzar con una sola mano (pero nos costará un tiempo acostumbrarnos).

Y esa barra de navegación se muestra o se oculta dependiendo de la dirección del scroll que hagamos en la página web.

Esto puede dar problemas en diferentes casos como, por ejemplo, si usamos contenido fijado en la página inferior de nuestra web.

Y puede que la toolbar oculte parte de nuestro Footer (como es mi caso).

Para solucionar esto podemos utilizar este código:

`env(safe-area-inset-bottom)`

Para que la toolbar deje un área de seguridad y no colapse con el contenido del Footer de nuestra web.

También tenemos unos códigos para ajustar el contenido en el modo landscape.

`viewport-fit=cover`

Y otros para mantener el área segura y que el contenido no quede oculto bajo el notch.

`env(safe-area-inset-top)` `env(safe-area-inset-left)` `env(safe-area-inset-right)`

Otra de las novedades de Safari 15 es la posibilidad de agregar vídeo a la previsualización cuando se comparte el link de nuestra web.

Y para acabar en Safari 15 podremos seleccionar el texto que aparece en las imágenes.

(Tengo que investigar cómo esto afectará al SEO)

Apple ha presentado una serie de novedades interesantes para Safari 15 y ahora es el turno de que los desarrolladores web se pongan las pilas y las aprovechen implementándolas en todas las webs posibles.
