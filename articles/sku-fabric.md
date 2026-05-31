---
title: "Quel SKU Fabric choisir ?"
date: 2026-05-11
slug: quel-sku-fabric-choisir
excerpt: "Le raisonnement que j'utilise avec mes clients pour choisir une capacité Fabric : commencer par le trial, puis arbitrer entre PAYG et réservation selon le profil, et optimiser avant de scaler."
tags: [fabric, architecture, sku, capacite, couts, powerbi, retour-terrain]
level: intermediaire
draft: false
---

Quel SKU Fabric choisir ? Voilà le raisonnement que j'utilise avec mes clients.

## Étape 1 : le trial Fabric (60 jours)

Avant tout choix de SKU, le trial est votre meilleur allié. 60 jours pour explorer la plateforme, tester les workloads (Spark, Warehouse, Notebooks, Pipelines, Power BI) et mener des POC ou MVP.

Bonus : la capacité du trial est désormais ajustable de FTL4 à FTL64, ce qui permet de calibrer directement vos tests sur la cible visée.

Une fois les tests concluants, deux scénarios se présentent.

## Cas 1 : PME, budget contraint et/ou équipe data qui démarre

PAYG sur F4 (~507 €/mois) ou F8 (~1 014 €/mois) en France Central, en s'appuyant sur les retours de votre trial et sur le Fabric Capacity Estimator pour affiner.

Les avantages du PAYG : flexibilité totale, sans engagement. Vous pouvez pauser la capacité hors heures ouvrées, mesurer un ou deux mois de plus en conditions réelles, et scaler ou réduire à la demande.

Puis, quand votre consommation est stabilisée : bascule en réservation, soit environ 41 % d'économies.

## Cas 2 : Fabric devient votre plateforme data principale

Si vous avez le budget et la volonté de capitaliser sur Fabric, le F64 réservé est souvent le bon point de départ. Comptez environ 4 825 €/mois en réservation 1 an (France Central).

Les avantages :

- Des ressources confortables pour Spark, Warehouse, Notebooks, Pipelines, Power BI, etc.

- La fin des licences Pro/PPU pour les consommateurs : ils accèdent aux contenus hébergés sur la capacité sans licence individuelle. Sur 100 utilisateurs, c'est environ 1 400 €/mois de licences Pro qui disparaissent. 

- À partir de quelques centaines d'utilisateurs, le F64 devient mécaniquement plus rentable que l'addition Pro plus une capacité plus petite.

- L'accès aux fonctionnalités Premium de Power BI (paginated reports, déploiement par pipeline, etc.).

## Retour terrain

J'ai un client avec une architecture médaillon (Lakehouse, Warehouse, Notebooks, Pipelines, Orchestration et Power BI). Ça tourne sereinement sur une F4 plus licences Pro.

Certes, la volumétrie n'est pas monumentale et la parallélisation est limitée sur une F4. Mais ça tourne. Et le jour où on se heurtera à de vrais soucis de perf, on envisagera de scaler.

Parce que le sujet n'est pas seulement l'architecture. C'est l'optimisation des traitements. Avant de scaler : assurez-vous que vous ne consommez pas deux à trois fois plus de ressources que nécessaire.

## Pour Copilot / IA Fabric

La Fabric Copilot Capacity est faite pour ça : une capacité dédiée permettant d'isoler la consommation IA, d'éviter l'impact sur les workloads data, et de suivre clairement les coûts. Minimum F2, dans la région home du tenant.

---

*Tarifs relevés en mai 2026, France Central. Les prix Fabric évoluent régulièrement et varient par région : référez-vous à la page de tarification Azure et au Fabric Capacity Estimator pour les montants à jour.*
