---
title: "Architecture médaillon dans Microsoft Fabric : quel artefact à quel étage"
date: 2026-05-20
slug: architecture-medaillon-fabric-quel-artefact-quel-etage
excerpt: "Sur le papier, le médaillon Bronze / Silver / Gold est simple. Dans Fabric, la vraie question c'est : quel artefact à quel étage ? Mes choix par défaut après plusieurs projets, et pourquoi."
tags: [fabric, architecture, lakehouse, warehouse, medaillon, retour-terrain]
level: intermediaire
serie: "Industrialisation Fabric"
serie_ordre: 1
draft: false
---

> Premier volet d'une série sur l'industrialisation des plateformes data dans Microsoft Fabric : concevoir, structurer, automatiser.

Sur le papier, le médaillon Bronze / Silver / Gold est simple. Dans Fabric, la vraie question, c'est : quel artefact à quel étage ?

Voici mes choix par défaut, après plusieurs projets.

## Bronze : Lakehouse unique, organisé par schéma et folder par système source

Données brutes, telles que reçues des sources. Le Lakehouse encaisse tout (fichiers, Parquet, CSV, Delta) sans schéma imposé. L'organisation se fait par schéma, avec un folder par système source (Sage, SAP, etc.). Chaque source a son framework d'ingestion dédié, isolé proprement.

## Silver : Lakehouse et Notebooks

Nettoyage, conformage, conversion. Delta natif partout, pour rester compatible OneLake de bout en bout.

Les Notebooks Spark portent la logique de transformation : un notebook main, un pipeline ForEach qui boucle sur une table de configuration. Une ligne de config égale une table et ses règles de transformation (SCD, conversions, etc.). C'est une approche metadata-driven, scalable et maintenable.

## Gold : Warehouse

Modèle métier, calculs analytiques, vues exposées au reporting.

Choix assumé : Warehouse plutôt que Lakehouse, dès lors que toute la logique se fait en SQL. On gagne en confort de développement, en industrialisation des vues, et en lisibilité pour les équipes data côté client, notamment grâce aux CTEs.

## Restitution : semantic models et rapports Power BI

Pas de surprise ici. Le semantic model branché en mode Import ou Direct Lake, selon le contexte et les besoins.

## La couche transverse, souvent oubliée

Au-delà des étages du médaillon, une couche transverse porte tout l'édifice :

Les **pipelines** orchestrent l'ensemble : ingestion, déclenchement des notebooks, refresh du semantic model, refresh des SQL endpoints des Lakehouses.

Les **notebooks et pipelines génériques paramétrables** prennent en charge les transformations et tâches répétitives : UDF, transformations génériques, archivage, création de schémas de Lakehouse.

La **Variable Library** centralise les paramètres d'environnement (Item Reference, connexions, IDs). Récente dans Fabric, mais déjà indispensable.

## Un cadre, pas un dogme

Ces choix ne sont pas universels. Une équipe data 100 % Python ira peut-être full Lakehouse jusqu'au Gold. Une équipe BI legacy poussera tout en SQL dès Silver. Le médaillon, c'est un cadre, pas un dogme.

Poser les bons artefacts, c'est une chose. Les organiser entre workspaces en est une autre, et c'est là que l'industrialisation réserve quelques surprises. C'est l'objet du prochain volet de la série.
