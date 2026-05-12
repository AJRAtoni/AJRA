---
layout: post
title: Apple lanza “Sign in with Apple”
date: 2019-06-13 10:00:00 +0300
image: /images/logo-apple.jpg
source: AJRA-v09/_posts/2019-06-13-signin-apple.md
---

La semana pasada se celebró la WWDC 2019 donde Apple presentó cantidad de cosas interesantes, desde iPadOS, iOS 13, macOS Catalina, etc… pero hay algo que fue realmente interesante y sorprendente, el lanzamiento de una nueva API que como suele ser normal con Apple se basa en la seguridad y privacidad del usuario.

Actualmente cuando nos descargamos una app, un juego o queremos crearnos una cuenta en alguna web o red social se nos pide que rellenemos un formulario con nuestros datos. Este es un proceso lento y que a muchos les da pereza y acaban por no crearse una cuenta.

Eso es algo que Facebook, Google o Twitter ya sabían y por eso lanzaron sus propios botones de login.

<figure>
<img src="/images/146.png" alt="" />
</figure>

Estos botones son un arma de doble filo. Por un lado nos facilitan el registro ofreciendo los datos que Facebook o Google ya tienen de nosotros, pero al usarlos estamos aceptando que toda la información relacionada con la app y el uso que hacemos de ella acabe en manos de la compañía que nos ha facilitado el registro y usen esos datos para ganar dinero con ellos.

Por eso Apple ha decidido presentar “Sign in with Apple” un sistema de login similar al que tienen Facebook, Google o Twitter, con la principal diferencia de que Apple no trackeara ni negociará con tus datos.

<figure>
<img src="/images/146-2.jpg" alt="" />
</figure>

## Email aleatorio y de uso único.

Algo muy curioso y que demuestra el grado de privacidad que quiere ofrecernos Apple es que cuando usamos Sign in with Apple para realizar un registro en una web o app, Apple nos ofrecerá usar nuestros datos reales o utilizar un alias de email generado aleatoriamente y únicamente para esa web/app.

<figure>
<img src="/images/146-3.jpg" alt="" />
</figure>

## ¿De qué me sirve esto?

En el blog casi cada semana publicamos que alguna empresa ha sido hackeada y por lo general la base de datos de emails acaba subastada en la Dark Web.

Esos datos y emails suelen acabar filtrados y tú acabas recibiendo emails de spam que no te interesan lo más mínimo.

Pues bien, con este sistema tu no has dado tu verdadero email, has usado un alias que puedes gestionar y borrar en cualquier momento desde tu dispositivo.

Un extra de seguridad y privacidad muy valioso.

El servicio de “Sign in with Apple” funcionará mediante Touch ID / Face ID, lo cual aporta varios beneficios.

Por un lado tendremos Logins y Registros más rápidos, con un solo click ya estaremos registrados en la app.

Y por otro lado la seguridad que proporcionan los servicios de reconocimiento biométricos de Apple.

## Obligatorio en las Apps que integren servicio de login de terceros.

Apple ha anunciado a los desarrolladores que será obligatorio incluir “Sign in with Apple” en todas las Apps que ofrezcan servicios de login de terceros.

Es decir, si una app ofrece login con Facebook obligatoriamente tendrá que actualizarse e incluir la opción de “Sign in with Apple” antes de 2020.