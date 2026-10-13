# Stratégie de Test — QuickOrder

| Métadonnée | Valeur |
| :--- | :--- |
| **Projet** | QuickOrder (Plateforme de livraison de repas) |
| **Document** | Stratégie et Plan Général de Test QA |
| **Auteur** | Équipe QA — Vincent Hoebler (Nitrovinzleo) |
| **Version** | 1.0 — Campagne Initiale Pré-Production |
| **Date** | Octobre 2026 |
| **Statut** | Validé |

---

## 1. Contexte & Objectifs

QuickOrder est une application web de commande et livraison de repas en ligne développée en Python (Flask) avec base SQLite et API REST OpenAPI / Swagger.

Avant le lancement commercial auprès du grand public et des restaurateurs partenaires, l'équipe QA est mandatée pour évaluer la qualité logicielle globale, identifier les défaillances fonctionnelles et de sécurité, tester la robustesse des flux financiers et statuer sur l'aptitude au déploiement en production (**Recommandation Go / No-Go**).

---

## 2. Périmètre des Tests (Scope)

### 2.1. Éléments dans le périmètre (In-Scope)
* **Parcours Client Web (Front-Office) :**
  * Authentification (Inscription, Connexion, Déconnexion, Gestion de session).
  * Navigation dans le catalogue, filtres par catégorie, recherche textuelle et filtrage par frais de livraison.
  * Consultation des restaurants partenaires (statut ouvert/fermé, notes, menus, plats).
  * Gestion du panier d'achat (ajout, modification des quantités, suppression, contrôle des restaurants multiples).
  * Tunnel de commande et Checkout (sélection d'adresse, application de coupons de réduction, calcul du sous-total et des frais).
  * Modes de paiement (Carte bancaire simulée, PayPal, Espèces à la livraison avec rendu de monnaie).
  * Espace profil (historique des commandes, détail des commandes, carnet d'adresses).
* **Parcours Administrateur (Back-Office) :**
  * Accès restreint `/admin`.
  * Consultation et transition des statuts de commande.
* **API REST & Swagger (Interfaçage technique) :**
  * Documentation interactive Swagger `/docs/` avec authentification par en-tête `X-API-Key`.
  * Endpoints `/api/health`, `/api/restaurants`, `/api/restaurants/{id}/products`, `/api/coupons/validate`, `/api/orders`.
* **Règles Métier & Intégrité des données :**
  * Décrémentation des stocks et gestion de l'indisponibilité.
  * Application stricte des conditions de validité des coupons (date, seuil minimum, plafond).
  * Cohérence des totaux et des transactions financières.

### 2.2. Éléments hors périmètre (Out-of-Scope)
* Tests de charge extrême et scalabilité infrastructure (> 10 000 requêtes/seconde).
* Intégration bancaire réelle (les paiements sont simulés en environnement bac à sable).
* Compatibilité sur navigateurs obsolètes (Internet Explorer <= 11).

---

## 3. Parcours Critiques Identifiés

| ID | Parcours Critique | Priorité | Risque associé en cas de défaillance |
| :---: | :--- | :---: | :--- |
| **PC-01** | Tunnel de commande complet (Panier -> Paiement -> Confirmation) | **P0 (Bloquant)** | Perte sèche de chiffre d'affaires, commandes non enregistrées. |
| **PC-02** | Validation des paiements & calcul des montants | **P0 (Bloquant)** | Fraude, encaissement insuffisant, calcul erroné de la monnaie. |
| **PC-03** | Intégrité des stocks & disponibilité des restaurants | **P1 (Majeur)** | Vente de plats en rupture, commandes passées chez des partenaires fermés. |
| **PC-04** | Moteur d'application des coupons de réduction | **P1 (Majeur)** | Abus de promotions, coupons expirés appliqués à tort. |
| **PC-05** | API REST de commande et d'interfaçage | **P1 (Majeur)** | Crashs serveur, bypass de validation côté client. |
| **PC-06** | Authentification et cloisonnement des données | **P2 (Moyen)** | Usurpation de compte, accès non autorisé aux commandes d'un tiers. |

---

## 4. Typologie des Tests Réalisés

1. **Tests Fonctionnels & Nominaux :** Vérification de la conformité des flux utilisateurs standards selon les spécifications.
2. **Tests aux Limites (Boundary Value Analysis) :** Test des quantités `0`, `1`, `stock max`, `stock + 1`, coupons au centime près du montant minimum.
3. **Tests d'Erreur & Robustesse :** Soumission de données invalides, types inattendus, identifiants inexistants, montants négatifs.
4. **Tests de Règles Métier :** Vérification du non-cumul multi-restaurants, des conditions d'ouverture et de seuil minimum.
5. **Tests d'API & Sécurité :** Requêtes directes via Swagger et Postman, vérification de l'authentification par clé API, manipulation de payloads JSON.
6. **Tests Utilisateurs (UX Testing) :** Passation de scénarios guidés auprès d'utilisateurs représentatifs pour évaluer l'ergonomie et la clarté.

---

## 5. Environnement de Test & Outils

* **Application sous test :** QuickOrder V3.1 (Flask 3.1.1, SQLite, SQLAlchemy 3.1.1)
* **Navigateurs de test :** Google Chrome 129+, Mozilla Firefox 131+, Microsoft Edge 129+
* **Outils d'inspection :** Chrome DevTools (Console, Réseau, Stockage de session)
* **Outils API :** Swagger UI (`/docs/`), Postman v11, Python `requests` & `pytest`
* **Jeu de données de test :** Initialisé via `seed.py` (Restaurants : *Burger Factory, Tokyo Bowl, Green Kitchen, Pizza Roma* ; Comptes : `alice@example.com`, `bob@example.com`, `admin@quickorder.local`).

---

## 6. Critères d'Acceptation et Décision Go / No-Go

* **Critère Go (Feu Vert) :**
  * 0 anomalie bloquante (P0 / Critical).
  * Moins de 2 anomalies majeures (P1), toutes contournables sans risque financier ni perte de données.
  * Taux de succès des cas de test nominaux > 95 %.
* **Critère No-Go (Feu Rouge) :**
  * Présence d'au moins 1 bug critique touchant la facturation, les stocks, ou la duplication de commandes.
  * Vulnérabilités de sécurité permettant de bypasser les montants réels.
