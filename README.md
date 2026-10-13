# QuickOrder V3.1 — Audit Qualité Logicielle (QA)

[![QA Status](https://img.shields.io/badge/QA%20Status-Audit%20Termin%C3%A9-blue.svg)](#)
[![Décision](https://img.shields.io/badge/D%C3%A9cision-NO--GO%20Strict-critical.svg)](#)
[![Tests](https://img.shields.io/badge/Tests%20Ex%C3%A9cut%C3%A9s-28%20(15%20PASS%20%7C%2013%20FAIL)-orange.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.12%2B%20%7C%20Flask-green.svg)](#)

Ce dépôt contient le code source de l'application **QuickOrder** ainsi que l'ensemble des livrables de l'**Audit Qualité & Assurance Qualité (QA)** réalisés dans le cadre du module *Tests et qualité des solutions numériques* (Bachelor 3).

* **Auteur du rapport d'audit :** Vincent Hoebler ([@Nitrovinzleo](https://github.com/Nitrovinzleo))
* **Dépôt officiel GitHub :** [https://github.com/Nitrovinzleo/quickorder](https://github.com/Nitrovinzleo/quickorder)
* **Recommandation finale de livraison :** 🛑 **NO-GO STRICT POUR LA MISE EN PRODUCTION**

---

## 📁 Livrables de l'Audit Qualité (Dossier `docs/`)

Tous les livrables exigés par le cahier des charges ([docs/STUDENT_BRIEF.md](docs/STUDENT_BRIEF.md)) sont disponibles ci-dessous :

| Livrable | Description | Format |
| :--- | :--- | :---: |
| 📋 [**Stratégie de Test**](docs/test-strategy.md) | Périmètre, parcours critiques, typologie de tests et critères d'acceptation | Markdown |
| 🎯 [**Matrice des Risques**](docs/risk-matrix.md) | Analyse et cotation des 10 risques majeurs (probabilité × impact) | Markdown |
| 🧪 [**Cahier de Recette (Cas de Test)**](docs/test-cases.md) | **28 cas de test exécutés** (7 Nominaux, 7 Limites, 7 Erreurs, 7 Métier) | Markdown / [CSV](docs/test-cases.csv) |
| 📊 [**Rapport d'Exécution & Bilan**](docs/execution-report.md) | Synthèse chiffrée, taux de réussite, analyse des défauts et avis Go / No-Go | Markdown |
| 👥 [**Tests & Retours Utilisateurs**](docs/user-feedback.md) | Passation de 3 scénarios auprès de 2 testeurs cibles (Maxime & Sophie) | Markdown |
| 💡 [**Plan d'Amélioration Post-Audit**](docs/improvement-plan.md) | 8 recommandations concrètes priorisées selon la matrice Valeur / Effort | Markdown |

### 🐛 Rapports d'Anomalies Détaillés (`docs/bug-reports/`)

Au total, **10 fiches de bugs reproductibles** ont été documentées :
1. [**BUG-001** : Duplication automatique des commandes lors d'un paiement PayPal](docs/bug-reports/BUG-001-paypal-order-duplication.md) *(🔴 Critique)*
2. [**BUG-002** : Prise de commande autorisée dans un restaurant fermé](docs/bug-reports/BUG-002-order-on-closed-restaurant.md) *(🟠 Majeur)*
3. [**BUG-003** : Montant minimum de commande affiché mais jamais appliqué](docs/bug-reports/BUG-003-minimum-order-amount-bypassed.md) *(🟠 Majeur)*
4. [**BUG-004** : Achat de produits en rupture et passage des stocks en négatif](docs/bug-reports/BUG-004-out-of-stock-and-negative-inventory.md) *(🔴 Critique)*
5. [**BUG-005** : Paiement en espèces avec montant insuffisant accepté et monnaie négative](docs/bug-reports/BUG-005-cash-payment-insufficient-amount-accepted.md) *(🔴 Critique)*
6. [**BUG-006** : Discordance sur la promotion ATLAS (15% annoncés vs 10% appliqués)](docs/bug-reports/BUG-006-coupon-atlas15-rate-mismatch.md) *(🟡 Moyen)*
7. [**BUG-007** : Inversion de l'opérateur du filtre des frais de livraison en accueil](docs/bug-reports/BUG-007-delivery-fee-filter-inverted.md) *(🟡 Moyen)*
8. [**BUG-008** : Barre de recherche limitée au nom ignorant la description culinaire](docs/bug-reports/BUG-008-search-ignores-restaurant-description.md) *(🟡 Moyen)*
9. [**BUG-009** : Dépôt d'avis clients sans vérification d'achat préalable](docs/bug-reports/BUG-009-unverified-restaurant-reviews.md) *(🟡 Moyen)*
10. [**BUG-010** : Crash HTTP 500 (`AttributeError`) sur l'endpoint API `GET /api/orders`](docs/bug-reports/BUG-010-api-orders-crash-nonetype-error.md) *(🟠 Majeur)*

---

## 🚀 Démarrage Rapide de l'Application

### Option A — Python + Environnement virtuel (Local)

```powershell
# 1. Cloner et se placer dans le projet
cd c:\Users\vhoeb\Desktop\Ecole\B3\test\projet

# 2. Créer et activer le virtualenv
py -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Installer les dépendances
python -m pip install -r requirements.txt

# 4. Initialiser la base de données de démonstration
python seed.py

# 5. Lancer le serveur Flask
python run.py
```

* **Application Web :** [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Documentation Swagger API :** [http://127.0.0.1:5000/docs/](http://127.0.0.1:5000/docs/) (Clé d'autorisation : `quickorder-demo-key`)

### Option B — Docker Compose

```bash
docker compose up --build
```

---

## 🔑 Comptes de Démonstration

| Rôle | Email | Mot de passe |
| :--- | :--- | :--- |
| **Client Démo 1** | `alice@example.com` | `Password123!` |
| **Client Démo 2** | `bob@example.com` | `Password123!` |
| **Administrateur** | `admin@quickorder.local` | `Admin123!` |
| **Clé API Swagger** | `quickorder-demo-key` *(dans l'en-tête `X-API-Key`)* | — |

---

## 🧪 Lancer les Tests Automatisés

```bash
python -m pytest -v
```
*(Note : Le test `test_api_orders_with_key` échoue intentionnellement, révélant le bug `BUG-010` documenté dans notre rapport).*
