---
layout: post
title: SQUARESPACE TIPS 002 — Como usar tu propia fuente en Squarespace
date: 2018-10-11 10:00:00 +0300
image: /images/115.jpg
source: AJRA-v09/_posts/2018-10-11-squarespace-tip-2.md
---

Squarespace tiene decenas de fuentes que podemos utilizar en nuestros sitios web.

Pero en ocasiones nuestro clientes quieren usar una fuente en concreto o tienen su propia fuente personalizada y desean usar esa, así que vamos a ver los pasos a seguir en esa situación.

Vamos a suponer que tenemos una fuente llamada “cubodekubrick” y la queremos usar para los títulos H1 de nuestra web.Lo primero que tenemos que hacer es subir la fuente a Squarespace, y luego mediante código CSS haremos que esa fuente se muestre en la web.
Para ello tenemos que ir al menu de Squarespace **Diseño / CSS Personalizado**.


En esa ventana usaremos la opción **Gestionar archivos externos** y subiremos nuestra fuente “cubodekubrick”.


Y luego en el espacio destinado para usar código CSS personalizado copiaremos y pegaremos el siguiente código.

```
@font-face { font-family: ‘cubodekubrick’; src: url(‘//xxxxxxxxxxxxxxxxxxxx’); } h1 { font-family: ‘cubodekubrick ‘; }
```

Lo único que tenemos que cambiar de ese código es donde pone xxxxxxxxxxxxxxxxxxxx.

Ahí tenemos que poner la url que Squarespace ha creado para la fuente que hemos subido.

Si no sabemos cual es la url podemos seguir unos sencillos pasos:

1. Hacer doble click sobre las xxxxxxxxxxxxxxxxxxx para seleccionarlas.
2. Hacer click en el botón **Gestionar archivos externos**.
3. En la ventana que se abre debemos seleccionar la fuente que hemos subido.

Y listo, con estos pasos veremos como las xxxxxxxxxxxxxxxxxxxx se habrán transformado en la url de nuestra fuente.

Ahora ya podemos guardar y salir.

Nuestra fuente "cubodekubrick" se estará mostrando en todos los títulos H1 de nuestra web.

Tranquilos, se que en ocasiones, cuando vemos que hay que tocar código puede dar un poco de miedo, pero siguiendo estos pasos podréis conseguirlo sin problemas.

En caso de tener cualquier duda [podéis contactar conmigo](mailto:info@ajra.es) e intentare ayudaros.