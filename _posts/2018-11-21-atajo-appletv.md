---
layout: post
title: "Atajo de Siri para encender el Apple TV con la voz"
date: 2018-11-21 10:00:00 +0300
image: /images/117.png
image_alt: "Atajo de Siri para encender un Apple TV mediante comando de voz"
description: "Cómo crear un Atajo de Siri para encender el Apple TV usando su IP, número de serie y una URL local."
card_subtitle: "Los Atajos de Siri permiten automatizar tareas pequeñas."
resumen: "Los Atajos de Siri permiten automatizar tareas pequeñas. Encender el Apple TV con la voz fue un buen ejemplo de automatización doméstica sencilla."
source: AJRA-v09/_posts/2018-11-21-atajo-appletv.md
---

Apple lanzó Atajos de Siri para permitir automatizaciones sencillas desde iOS.

La app permite crear pequeñas secuencias de acciones para tareas repetitivas: procesar imágenes, convertir archivos, lanzar rutinas, abrir apps o controlar dispositivos.

En este caso, vamos a usarla para encender el Apple TV con un comando de voz.

## Qué necesitas

Para crear este atajo necesitas dos datos del Apple TV:

- Número de serie.
- Dirección IP local.

Puedes encontrarlos en:

`Ajustes > General > Información`

Apunta ambos datos porque los usarás en la URL del atajo.

## La URL local

El atajo utiliza una URL con esta estructura:

```text
http://TUIP:3689/?pairing-guid=NUMEROSERIEAPPLETV#
```

Debes sustituir:

- `TUIP` por la dirección IP del Apple TV.
- `NUMEROSERIEAPPLETV` por el número de serie.

## Crear el atajo

En Atajos, crea una acción que abra esa URL.

A continuación puedes asignarle un nombre claro, por ejemplo:

`Encender Apple TV`

Después configura la frase de Siri que quieres usar, por ejemplo:

`Siri, enciende la tele`

Si todo está bien configurado y el Apple TV está en la misma red, el atajo debería enviar la petición y activar el dispositivo.

## Por qué me gustan los Atajos

Atajos es interesante porque acerca la automatización a usuarios que no quieren programar.

No sustituye a sistemas domóticos avanzados, pero permite resolver pequeños problemas cotidianos con bastante flexibilidad.

También encaja muy bien con flujos de productividad personal, como los que he ido comentando al hablar de [GTD](/blog/gtd-flujo-de-trabajo-y-productividad-sin-estres/) o del iPad como herramienta de trabajo.

Si quieres automatizar tareas repetitivas en iPhone, iPad, Mac o herramientas de trabajo, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
