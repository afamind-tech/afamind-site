---
title: "Pourquoi j'écris sur Microsoft Fabric"
date: 2026-05-09
slug: pourquoi-j-ecris-sur-microsoft-fabric
excerpt: "Fabric est jeune, parfois instable, et probablement la plateforme data la plus ambitieuse du marché. Elle évolue aussi trop vite pour que la documentation suffise. C'est précisément pour ça que ce blog existe."
tags: [fabric, retour-terrain]
level: decouverte
serie: "Découverte Fabric"
serie_ordre: 2
draft: false
---

Microsoft Fabric est jeune. Parfois instable. Et c'est probablement la plateforme data la plus ambitieuse du marché en ce moment.

Ce qui la rend pertinente : du tout-en-un, en SaaS, de l'ingestion jusqu'au reporting Power BI. En quelques clics, un Lakehouse, un Warehouse, un pipeline, un notebook. Ce qui prenait des jours à configurer sur Synapse prend désormais quelques minutes. J'ai travaillé sur les anciennes stacks Microsoft, et le progrès est réel.

Mais il y a un revers.

## La plateforme va plus vite que sa documentation

Fabric évolue si vite que même en tant qu'architecte, tout suivre devient difficile. Ce qui était vrai il y a six mois ne l'est parfois plus aujourd'hui. Des fonctionnalités apparaissent. D'autres changent de comportement sans prévenir.

Concrètement, ça implique trois choses :

- Les décisions d'architecture doivent anticiper ce qui n'existe pas encore.

- La veille n'est plus optionnelle, elle fait partie du métier.

- Et certains choix techniques d'aujourd'hui seront peut-être obsolètes demain.

C'est la force de Fabric. C'est aussi sa contrainte.

## Ce que la doc ne dit pas

Le vrai problème de cette vitesse, c'est qu'elle creuse un écart. La documentation officielle décrit ce que fait une fonctionnalité. Elle ne dit pas ce qui casse en production, quels choix se paient six mois plus tard, ni ce qu'on aurait aimé savoir avant de se lancer.

Ce savoir-là existe, mais il reste dans la tête de ceux qui se sont cognés au mur. Personne ne l'écrit. On l'apprend en se trompant, projet après projet.

C'est exactement ce vide que ces articles cherchent à combler. Pas de la doc Microsoft reformulée, mais du retour de terrain : les choix que j'assume, ceux que je regrette, les pièges rencontrés, et ce qui tient vraiment une fois en production.

Parce que sur une plateforme qui change aussi vite, la vraie question n'est pas de savoir si Fabric est mature. Elle est de rester capable d'évoluer avec elle.
