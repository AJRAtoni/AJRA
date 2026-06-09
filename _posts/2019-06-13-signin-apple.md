---
layout: post
title: "Sign in with Apple: login rápido con foco en privacidad"
date: 2019-06-13 10:00:00 +0300
image: /images/blog/apple-gradient.webp
image_alt: "Logotipo de Apple en una noticia sobre Sign in with Apple"
recursos_logo: /images/blog/apple.png
recursos_logo_alt: "Logo de Apple"
description: "Apple presentó Sign in with Apple en WWDC 2019, una alternativa a los logins sociales basada en privacidad, Face ID, Touch ID y alias de email."
card_subtitle: "Sign in with Apple fue una respuesta directa a los botones de login de Facebook y Google."
resumen: "Sign in with Apple fue una respuesta directa a los botones de login de Facebook y Google: menos tracking y más control sobre el email que compartes."
source: AJRA-v09/_posts/2019-06-13-signin-apple.md
---

En la WWDC 2019 Apple presentó iPadOS, iOS 13, macOS Catalina y muchas novedades más.

Pero una de las más interesantes fue Sign in with Apple, una API de login centrada en privacidad.

## El problema de los logins sociales

Registrarse en una app o web suele ser aburrido: formulario, email, contraseña, verificación y más datos.

Facebook, Google y Twitter ya habían resuelto parte de esa fricción con botones de login.

<figure>
<img src="/images/blog/146.png" alt="Botones de login social con Facebook, Google y Twitter" />
</figure>

El problema es que esos botones también pueden compartir datos de uso con la plataforma que facilita el registro.

Ahorras tiempo, pero entregas información.

## Qué propuso Apple

Apple presentó Sign in with Apple como una alternativa similar en comodidad, pero distinta en tratamiento de datos.

La promesa era clara: facilitar el registro sin trackear ni monetizar el uso de la app.

<figure>
<img src="/images/blog/146-2.jpg" alt="Pantalla de Sign in with Apple como alternativa privada de registro" />
</figure>

El sistema funcionaba con Touch ID o Face ID, lo que hacía el registro rápido y seguro dentro del ecosistema Apple.

## Email aleatorio y de uso único

<figure>
<img src="/images/blog/146-3.jpg" alt="Opción de ocultar email real mediante alias en Sign in with Apple" />
</figure>

La función más interesante era ocultar tu email real.

Al registrarte, Apple podía generar un alias único para esa app o web.

Si más adelante esa empresa filtraba datos, vendía listas o empezaba a enviarte spam, podías desactivar ese alias sin exponer tu dirección principal.

Esto conectaba muy bien con hábitos de seguridad como usar [contraseñas únicas](/blog/passwords-seguros/) y reducir la exposición de datos personales.

## Obligatorio si había otros logins

Apple anunció a los desarrolladores que Sign in with Apple sería obligatorio en apps que ofrecieran login con terceros.

Es decir: si una app ofrecía "login con Facebook" o "login con Google", también tendría que ofrecer la opción de Apple.

Esto no era solo una función. Era una decisión de plataforma.

## Lectura retrospectiva

Sign in with Apple reforzó una línea estratégica de Apple: privacidad como diferenciación.

En un contexto de problemas como [Facebook Research](/blog/facebook-espia/) o [Cambridge Analytica](/blog/facebook-filtrados/), Apple encontró una forma de convertir seguridad y control de datos en ventaja de producto.

Si quieres revisar privacidad, login, formularios o gestión de datos de usuarios en tu producto digital, puedes [escribirme a ajra@ajra.es](mailto:ajra@ajra.es).
