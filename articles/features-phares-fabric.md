---
title: "Les fonctionnalités phares de Microsoft Fabric"
date: 2026-05-10
slug: fonctionnalites-phares-microsoft-fabric
excerpt: "Fabric hérite d'une bonne partie de l'arsenal data de Microsoft, mais ce n'est pas là qu'est sa spécificité. Tour d'horizon des fonctionnalités réellement nouvelles : Lakehouse, Shortcuts, Mirroring, Direct Lake et OneLake Security."
tags: [fabric, lakehouse, shortcuts, mirroring]
level: decouverte
serie: "Découverte Fabric"
serie_ordre: 3
draft: false
---

Fabric hérite d'une bonne partie de l'arsenal data de Microsoft : pipelines, notebooks, Spark, T-SQL. Ces briques sont connues, éprouvées, et ne sont pas ce qui fait la spécificité de la plateforme. On ne va donc pas les détailler ici.

En revanche, Fabric apporte un ensemble de fonctionnalités nouvelles, ou profondément repensées, qui méritent qu'on s'y arrête : ce sont elles qui changent la façon de concevoir une plateforme data. En voici les principales.

## Le Lakehouse

Le Lakehouse réunit dans un même artefact deux mondes longtemps séparés : la souplesse d'un lac de données et la capacité d'interrogation SQL d'un entrepôt. La donnée est stockée une seule fois au format Delta dans OneLake, et reste accessible à la fois via Spark (pour l'ingénierie) et via un endpoint SQL en lecture (pour l'analyse en T-SQL).

Ce que ça change : on n'a plus à choisir en amont entre un lac flexible mais peu pratique à requêter, et un entrepôt rigide mais confortable en SQL. Les deux cohabitent sur la même donnée.

La nuance terrain : l'endpoint SQL du Lakehouse est en lecture seule, et sa synchronisation des métadonnées n'est pas toujours instantanée. Une table fraîchement créée côté Spark peut mettre un moment à apparaître côté SQL. Microsoft travaille à réduire ce décalage : on peut déjà forcer la synchronisation via une activité dédiée dans les pipelines, et une nouvelle option New metadata sync (en preview) est apparue au niveau du workspace.

## Les Shortcuts

Un shortcut est un pointeur, un lien symbolique vers de la donnée qui vit ailleurs : un autre workspace, un autre Lakehouse, ou une source externe comme ADLS Gen2, Amazon S3 ou Google Cloud Storage. La donnée n'est pas copiée, simplement référencée.

Ce que ça change : on peut donner une vue unifiée sur des données dispersées entre plusieurs clouds ou plusieurs workspaces, sans les déplacer ni les dupliquer. Une seule copie, exploitée de partout.

La nuance terrain : au-delà de l'argument anti-duplication, le shortcut a une vraie valeur d'architecture. Il permet de découpler les couches d'une plateforme, un usage souvent sous-estimé.

## Le Mirroring

Le Mirroring réplique en quasi temps réel une base externe (Azure SQL, Cosmos DB, Snowflake, et d'autres) directement dans OneLake, au format Delta, sans pipeline d'ingestion à construire. C'est l'approche dite zéro-ETL.

Ce que ça change : on obtient une copie continuellement synchronisée de sa source, sans écrire ni maintenir le moindre pipeline de réplication. Les changements à la source se retrouvent dans Fabric en quasi-direct.

La nuance terrain : contrairement au shortcut qui ne fait que pointer, le Mirroring crée une copie physique, donc un coût de stockage. Il ne couvre qu'un ensemble défini de sources, et reste un accélérateur d'ingestion (typiquement vers Bronze), pas un substitut à toute la logique de transformation en aval. J'ai personnellement testé le mirroring de SQL Server, qui nécessite malheureusement des droits élevés sur la base source : sysadmin, et db_owner pour chaque ajout de nouvelle table. Un point à anticiper, car ce n'est pas toujours acceptable côté production.

## Le Direct Lake

Le Direct Lake est un mode de connexion des semantic models Power BI qui interroge directement les tables Delta de OneLake, sans import préalable ni latence de rafraîchissement.

Ce que ça change : il combine ce qu'on cherchait des deux côtés jusque-là, la rapidité du mode Import et la fraîcheur du DirectQuery, le tout sur de gros volumes. C'est l'une des promesses les plus séduisantes de Fabric côté restitution.

La nuance terrain : Direct Lake est puissant, mais sous conditions. Dans certains cas, il bascule en repli sur DirectQuery, avec l'impact de performance que ça implique. Il porte aussi des contraintes qui surprennent au moment d'industrialiser, notamment côté déploiement, où le comportement diffère selon qu'on est en Direct Lake on OneLake ou en Direct Lake on SQL. C'est typiquement une feature à adopter en connaissant ses limites, pas les yeux fermés.

## OneLake Security

OneLake Security permet de définir une sécurité fine (sécurité au niveau des lignes, des colonnes, rôles d'accès) directement au niveau du datalake, et de l'appliquer quel que soit le moteur qui consomme la donnée. La promesse : définir la règle une fois, et la voir s'appliquer que la donnée soit lue via Spark, en SQL ou dans Power BI, sans la reconfigurer dans chaque outil.

C'est une brique encore en maturation, mais qui répond à un vrai besoin : unifier un modèle de sécurité jusque-là éclaté entre les différents outils.

## Ce qu'il faut retenir

Ces fonctionnalités ont un point commun : elles reposent toutes sur OneLake comme socle. C'est ce qui fait de Fabric autre chose qu'un simple ré-emballage d'outils existants. Ce sont aussi des fonctionnalités jeunes, qui évoluent vite, et dont il vaut mieux connaître les limites avant de bâtir une architecture dessus.
