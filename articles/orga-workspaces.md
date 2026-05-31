---
title: "Organiser ses workspaces Fabric : le découpage qui survit à l'industrialisation"
date: 2026-05-29
slug: organiser-workspaces-fabric-industrialisation
excerpt: "Au démarrage, un workspace unique suffit. Dès qu'on parle CI/CD, cette organisation devient le frein principal. Comment découper ses workspaces Fabric pour industrialiser sans douleur, et pourquoi ce découpage n'est peut-être que temporaire."
tags: [fabric, architecture, cicd, workspaces, onelake, retour-terrain]
level: avance
serie: "Industrialisation Fabric"
serie_ordre: 2
draft: true
---

> Deuxième volet d'une série sur l'industrialisation des plateformes data dans Microsoft Fabric : concevoir, structurer, automatiser. Le premier volet posait l'architecture médaillon et le choix des artefacts à chaque étage.

## Au début, un workspace suffit

Quand je démarre un projet Fabric, je mets presque tout dans un seul workspace : l'architecture médaillon complète, avec ses Lakehouses Bronze et Silver, son Warehouse Gold et ses pipelines. À côté, un second workspace pour la partie analytics : semantic models et rapports Power BI.

C'est simple, lisible, et ça suffit largement. Tant qu'on développe et qu'on livre à la main, cette organisation ne pose aucun problème. Elle a même le mérite de la clarté : un endroit pour la donnée, un endroit pour la restitution.

Et puis arrive le moment où on parle d'industrialisation.

## Le moment où ça coince

Dès qu'on vise un vrai cycle CI/CD, avec des environnements Dev / Recette / Production et du travail isolé sur des branches, l'organisation des workspaces cesse d'être un détail de confort pour devenir une décision structurante.

Le mécanisme central de Fabric pour ça, c'est le branch-out to workspace : depuis un workspace connecté à Git, on dérive une branche et un workspace jumeau pour travailler isolément avant de réintégrer. Sur le papier, parfait.

Le problème, c'est que le branch-out clone le workspace entier. Si tout vit au même endroit, brancher une simple évolution embarque aussi toute la couche d'ingestion : Lakehouses, notebooks, pipelines techniques. Des artefacts lourds, qui traînent leurs propres contraintes. (Dans une architecture hybride Lakehouse / Warehouse comme la mienne, ça va même plus loin, car les vues SQL du Warehouse dépendent des tables du Lakehouse, un ordre de dépendance que le branch-out ne gère pas, mais c'est un sujet à part entière.)

Autrement dit : l'organisation qui simplifiait la vie au démarrage devient le frein principal à l'industrialisation.

## Le principe : à chaque couche son propre cycle de vie

La bonne nouvelle, c'est qu'on n'a pas à choisir entre tout mettre ensemble et tout dupliquer. Les shortcuts OneLake permettent de référencer une donnée restée dans un autre workspace sans la copier. Au-delà de l'argument anti-duplication, c'est un vrai outil d'architecture : on sort la couche d'ingestion du périmètre branché, et on la rend accessible aux couches en aval via shortcut.

Le principe est simple : chaque couche vit dans son propre workspace, avec son propre repository et son propre cycle de vie, indépendamment des autres.

Concrètement, le découpage que je privilégie aujourd'hui :

Ingest (Bronze + Silver) : la couche d'ingestion. Stable, elle évolue lentement et n'est pas perturbée par les itérations des couches en aval.

Serve (Gold + Semantic Model) : la couche métier. C'est elle qui bouge le plus, au rythme des besoins. Elle consomme les tables Silver via shortcuts, sans les embarquer.

Analytics (rapports Power BI) : la couche de restitution, séparée du modèle pour que les rapports évoluent à leur propre cadence, sans toucher au semantic model.

Orchestration (pipelines et triggers) : le chef d'orchestre, isolé pour ne pas mélanger la mécanique de déclenchement avec le reste.

L'intérêt dépasse le seul CI/CD. Cette séparation correspond aussi à une répartition naturelle des responsabilités : une équipe BI sur les vues Gold et la modélisation, un profil plus senior sur la couche d'ingestion, souvent plus complexe et plus stable. C'est une organisation qu'on retrouve sur beaucoup de plateformes data modernes.

## Un découpage daté, pas gravé dans le marbre

Une précision honnête : ce découpage est la bonne réponse au tooling d'aujourd'hui, pas une vérité éternelle. Microsoft avance vite sur le sujet. Le Selective Branching, par exemple, permet déjà de cocher les items à embarquer dans un branch-out, même s'il reste pour l'instant limité à l'UI et non scriptable proprement.

Le jour où ces mécanismes seront pleinement automatisables, il n'est pas impossible qu'on revienne à des organisations plus simples, voire à un workspace unique pour le médaillon. En attendant, donner à chaque couche son propre cycle de vie reste le moyen le plus fiable d'industrialiser sans douleur.

## Et après

Le découpage pose les fondations. Reste à l'automatiser : c'est l'objet du troisième volet de la série, sur le CI/CD Fabric avec Azure DevOps, la branching strategy, les deployment pipelines, et les pièges qui subsistent.
