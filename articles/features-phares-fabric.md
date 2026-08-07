---
title: "Les fonctionnalités phares de Microsoft Fabric"
date: 2026-08-07
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

Le Lakehouse réunit dans un même artefact deux mondes longtemps séparés : la souplesse d'un lac de données et la capacité d'interrogation SQL d'un entrepôt. La donnée est stockée une seule fois au format Delta dans OneLake, et reste accessible à la fois via Spark pour l'ingénierie et via un endpoint SQL en lecture pour l'analyse en T-SQL.

Ce que ça change : on n'a plus à choisir en amont entre un lac flexible mais peu pratique à requêter, et un entrepôt rigide mais confortable en SQL. Les deux cohabitent sur la même donnée.

La nuance terrain : l'endpoint SQL du Lakehouse est en lecture seule sur les tables Delta, et la synchronisation des métadonnées n'est pas toujours instantanée. Une table fraîchement créée côté Spark peut mettre un moment à apparaître côté SQL. Microsoft travaille à réduire ce décalage : on peut déjà forcer la synchronisation, et une nouvelle option New metadata sync, en preview, permet aux nouveaux endpoints de réduire fortement ce délai.

## Les Shortcuts

Un shortcut est un pointeur, un lien symbolique vers de la donnée qui vit ailleurs : un autre workspace, un autre Lakehouse, ou une source externe comme ADLS Gen2, Amazon S3 ou Google Cloud Storage. La donnée n'est pas copiée, simplement référencée.

Ce que ça change : on peut donner une vue unifiée sur des données dispersées entre plusieurs clouds ou plusieurs workspaces, sans les déplacer ni les dupliquer. Une seule copie, exploitée de partout.

La nuance terrain : au-delà de l'argument anti-duplication, le shortcut a une vraie valeur d'architecture. Il permet de découpler les couches d'une plateforme, un usage souvent sous-estimé.

## Le Mirroring

Le Mirroring réplique en quasi temps réel une base externe, comme Azure SQL, Cosmos DB, Snowflake, SQL Server et d'autres, directement dans OneLake, au format Delta, sans pipeline d'ingestion à construire. C'est l'approche dite zéro-ETL.

Ce que ça change : on obtient une copie continuellement synchronisée de sa source, sans écrire ni maintenir le pipeline de réplication associé. Les changements à la source se retrouvent dans Fabric en quasi-direct.

La nuance terrain : contrairement au shortcut qui ne fait que pointer, le Mirroring crée une copie physique dans OneLake. Ce stockage est toutefois inclus jusqu'à une limite liée à la taille de la capacité Fabric. Il ne couvre qu'un ensemble défini de sources, et reste un accélérateur d'ingestion, typiquement vers Bronze, pas un substitut à toute la logique de transformation en aval.

Les prérequis côté source sont également à anticiper. Sur SQL Server par exemple, le Mirroring s'appuie sur CDC et peut nécessiter des droits élevés pour sa configuration, notamment `sysadmin` lors de son activation initiale sur certaines versions. Un point qui n'est pas toujours acceptable côté production.

## Le Direct Lake

Le Direct Lake est un mode de connexion des semantic models Power BI qui exploite directement les tables Delta de OneLake, sans passer par le cycle classique d'import et de refresh des données.

Ce que ça change : il cherche à combiner ce qu'on recherchait des deux côtés jusque-là, les performances proches du mode Import et la fraîcheur du DirectQuery, le tout sur de gros volumes. C'est l'une des promesses les plus séduisantes de Fabric côté restitution.

La nuance terrain : Direct Lake est puissant, mais sous conditions. Il existe aujourd'hui deux approches. Direct Lake on SQL peut, dans certains cas, basculer en DirectQuery, avec l'impact de performance que ça implique. Direct Lake on OneLake, plus récent et désormais recommandé pour les nouveaux modèles, accède directement à OneLake et ne possède plus ce mécanisme de fallback.

Les deux approches ont leurs propres contraintes, notamment au moment d'industrialiser et de déployer les modèles. C'est typiquement une feature à adopter en connaissant ses limites, pas les yeux fermés.

## OneLake Security

OneLake Security permet de définir une sécurité fine, au niveau des tables, des dossiers, des lignes ou des colonnes, directement sur les données stockées dans OneLake. Ces règles sont ensuite appliquées lorsque la donnée est consommée via Spark, le SQL Analytics Endpoint ou Direct Lake.

La promesse : définir la sécurité au plus près de la donnée, plutôt que de devoir la reconstruire dans chaque moteur.

C'est une brique désormais disponible en GA, notamment sur les Lakehouses, et qui répond à un vrai besoin : unifier un modèle de sécurité jusque-là réparti entre les différents outils.


## Ce qu'il faut retenir

Ces fonctionnalités ont un point commun : elles reposent toutes sur OneLake comme socle. C'est ce qui fait de Fabric autre chose qu'un simple ré-emballage d'outils existants.

Elles changent surtout la manière de construire une plateforme : moins de copies, moins de mouvements de données et davantage de services capables de travailler directement sur un même socle.

Ce sont aussi des fonctionnalités qui évoluent vite, et dont il vaut mieux connaître les limites avant de bâtir une architecture dessus.

