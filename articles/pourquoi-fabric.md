---
title: "Pourquoi j'écris sur Microsoft Fabric"
date: 2026-08-07
slug: pourquoi-j-ecris-sur-microsoft-fabric
excerpt: "Fabric est jeune, parfois instable, et probablement la plateforme data la plus ambitieuse du marché. Elle évolue aussi trop vite pour que la documentation suffise. C'est précisément pour ça que ce blog existe."
tags: [fabric, retour-terrain]
level: decouverte
serie: "Découverte Fabric"
serie_ordre: 2
draft: false
---

Microsoft Fabric est jeune. Parfois instable. Et c'est probablement la plateforme data la plus ambitieuse du marché en ce moment.

Ce qui la rend pertinente : du tout-en-un, en SaaS, de l'ingestion jusqu'au reporting Power BI, avec une plateforme qui s'étend désormais au temps réel et à l'intelligence artificielle. En quelques clics, on crée un Lakehouse, un Warehouse, un pipeline ou un notebook. Des briques qui demandaient auparavant davantage de configuration et d'infrastructure peuvent désormais être mises à disposition en quelques minutes. J'ai travaillé sur les anciennes stacks Microsoft, et le progrès est réel.

Mais il y a un revers.

## La plateforme va plus vite que sa documentation

Fabric évolue si vite que même en tant qu'architecte, tout suivre devient difficile. Ce qui était vrai il y a six mois ne l'est parfois plus aujourd'hui. Des fonctionnalités apparaissent, d'autres évoluent, et les bonnes pratiques changent avec elles.

Concrètement, ça implique trois choses :

- Les décisions d'architecture doivent anticiper l'évolution de la plateforme.
- La veille n'est plus optionnelle, elle fait partie du métier.
- Et certains choix techniques pertinents aujourd'hui le seront peut-être beaucoup moins demain.

C'est la force de Fabric. C'est aussi sa contrainte.

## Ce que la doc ne dit pas

Le vrai problème de cette vitesse, c'est qu'elle creuse un écart. La documentation officielle décrit ce que fait une fonctionnalité. Elle dit beaucoup moins ce qui se passe une fois confronté à un vrai projet : ce qui casse en production, quels choix se paient six mois plus tard, ou ce qu'on aurait aimé savoir avant de se lancer.

Ce savoir-là existe, mais il est dispersé. Une bonne partie vient simplement de l'expérience : des problèmes rencontrés, des mauvais choix, des contournements et des décisions prises projet après projet.

C'est exactement ce vide que ces articles cherchent à combler. Pas de la doc Microsoft reformulée, mais du retour de terrain : les choix que j'assume, ceux que je regrette, les pièges rencontrés, et ce qui tient vraiment une fois en production.

Parce que sur une plateforme qui change aussi vite, la vraie question n'est pas seulement de savoir si Fabric est mature. Elle est aussi de rester capable d'évoluer avec elle.
