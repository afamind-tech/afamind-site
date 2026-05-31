---
title: "Microsoft Fabric, c'est quoi ?"
date: 2026-05-05
slug: microsoft-fabric-c-est-quoi
excerpt: "Une plateforme data tout-en-un, en SaaS, de l'ingestion jusqu'au reporting. Voici ce qu'est Microsoft Fabric, le problème qu'elle résout, et ses briques principales, expliqués simplement."
tags: [fabric, onelake, data, retour-terrain]
level: decouverte
serie: "Découverte Fabric"
serie_ordre: 1
draft: false
---

## Le problème avant Fabric

Pendant des années, construire une plateforme data revenait à assembler des outils séparés. Azure Data Factory pour l'orchestration, Databricks ou Spark pour l'ingénierie, Synapse pour le warehouse, Power BI pour la restitution. Chacun excellent dans son domaine, mais qu'il fallait connecter entre eux.

Le résultat : de la donnée dupliquée d'un service à l'autre (et donc des coûts qui se multiplient), un modèle de sécurité éclaté entre plusieurs produits, et une facturation répartie sur autant de lignes que d'outils. Les connecteurs existaient, ces briques savaient se parler, mais les faire tenir ensemble dans le temps avait un coût bien réel.

## Ce qu'est Microsoft Fabric

Fabric est la réponse de Microsoft à ce problème : une plateforme analytics unifiée, livrée en SaaS, qui couvre toute la chaîne de la donnée, de l'ingestion jusqu'au reporting Power BI.

L'idée centrale n'est pas d'ajouter un outil de plus, mais de réunir tous ces outils dans une seule plateforme cohérente, où ils partagent le même stockage, le même modèle de sécurité, et la même facturation. La donnée ne se déplace plus entre les systèmes, parce qu'il n'y a plus de systèmes séparés.

Concrètement, en quelques clics, on crée un Lakehouse, un Warehouse, un pipeline ou un notebook, sans provisionner ni configurer de serveurs. Ce qui prenait des jours à mettre en place sur les anciennes stacks prend désormais quelques minutes.

Une précision utile, parce qu'on lit souvent que Fabric remplace tout l'ancien arsenal : c'est vrai pour Synapse, beaucoup moins pour Azure Data Factory. Synapse était la précédente promesse de plateforme unifiée de Microsoft ; il fait aujourd'hui doublon quasi total avec Fabric et a vocation à disparaître au profit de ce dernier. ADF, lui, garde un périmètre propre. Les nouveautés des Fabric Pipelines, comme le refresh de semantic model, la maintenance de Lakehouse ou le déclenchement de notebooks, sont natives à l'écosystème Fabric, et ADF n'en a pas besoin pour rester pertinent : il reste justifiable pour orchestrer Databricks ou Snowflake, pour des projets purement ETL, ou dans des environnements hors Fabric. Autrement dit, Fabric absorbe Synapse, mais ne rend pas ADF obsolète pour autant.

## OneLake : le cœur du réacteur

S'il ne fallait retenir qu'un concept, ce serait OneLake.

OneLake est le lac de données unique et logique de toute l'organisation. La comparaison officielle de Microsoft est parlante : OneLake est au data ce que OneDrive est aux documents. Un seul endroit pour stocker la donnée, accessible par tous les outils de la plateforme.

Tous les workloads écrivent et lisent dans OneLake, au format ouvert Delta Parquet. Si un data engineer charge des données avec Spark, et qu'un développeur SQL les exploite ensuite en T-SQL, les deux travaillent sur la même donnée, au même endroit, sans copie. C'est ce qui élimine la duplication et fait de Fabric une plateforme réellement intégrée, et pas une juxtaposition d'outils.

## Les workloads : un outil par métier

Fabric s'organise en workloads, des ensembles de capacités pensés pour un usage précis :

**Data Factory** : l'ingestion et l'orchestration. Des centaines de connecteurs pour faire entrer la donnée, et des pipelines pour enchaîner les traitements.

**Data Engineering** : l'ingénierie de données à base de Spark, via les Lakehouses et les notebooks. C'est là que se font les transformations lourdes.

**Data Warehouse** : un entrepôt SQL transactionnel et scalable, pour ceux qui travaillent en T-SQL.

**Real-Time Intelligence** : le traitement et l'analyse de flux de données en temps réel.

**Data Science** : l'entraînement et l'exécution de modèles de machine learning, intégrés au reste de la plateforme.

**Power BI** : la restitution, les rapports et la visualisation, brique historique de Microsoft désormais intégrée nativement.

Tous ces workloads partagent OneLake comme socle commun, et une couche de gouvernance unifiée pour le catalogue, la traçabilité et la sécurité.

## Un modèle de capacité, pas de serveurs

Dernier point qui dépayse quand on vient du monde Azure classique : on ne provisionne pas de serveurs ni de clusters. On provisionne une capacité, c'est-à-dire un pool de puissance de calcul partagé entre tous les workloads.

Sur le papier, ça simplifie les choses : un seul curseur de puissance, une facturation consolidée. En pratique, c'est l'un des sujets les plus délicats de Fabric. Le comportement d'une capacité (lissage de la consommation, throttling quand elle sature, partage entre workloads) est loin d'être transparent, et comprendre pourquoi une capacité ralentit ou comment la dimensionner correctement est un vrai sujet, sur lequel beaucoup d'équipes butent.

## Ce qu'il faut en retenir

Fabric n'est pas un nouvel outil de plus. C'est une tentative de réunir toute la chaîne data dans une plateforme unique, autour d'un lac de données partagé. Le progrès est réel par rapport aux anciennes stacks Microsoft, et c'est probablement la plateforme data la plus ambitieuse du marché aujourd'hui.

C'est aussi une plateforme jeune, qui évolue très vite. Ce qui en fait sa force, et parfois sa contrainte.
