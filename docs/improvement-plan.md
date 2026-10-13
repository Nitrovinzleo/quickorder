# Plan d'Amélioration & Recommandations Post-Audit — QuickOrder

| Métadonnée | Valeur |
| :--- | :--- |
| **Projet** | QuickOrder QA Audit |
| **Document** | Plan d'Améliorations Techniques, Métier et Ergonomiques |
| **Auteur** | Équipe QA — Vincent Hoebler (Nitrovinzleo) |
| **Nombre de propositions** | **8 améliorations concrètes et priorisées** |

---

## 1. Méthodologie de Priorisation

Les recommandations sont ordonnées selon la matrice standard **Impact Métier vs Effort de Développement** :
* **Sprint 0 (Urgences Bloquantes) :** Correctifs immédiats indispensables avant tout Go-Live.
* **Sprint 1 (Améliorations Majeures) :** Sécurisation et intégrité de la plateforme.
* **Sprint 2 (Optimisations UX) :** Amélioration du confort d'utilisation et conversion.

---

## 2. Feuille de Route des Améliorations

### 1. Sécurisation et Idempotence des Paiements PayPal (P0 — Urgence Immédiate)
* **Constat :** Deux commandes identiques créées lors d'un règlement PayPal (`BUG-001`).
* **Solution :** Supprimer la création redondante dans `orders.py` et intégrer un jeton d'idempotence (`idempotency_key`) généré côté client et vérifié en base pour interdire la duplication de transactions.
* **Effort :** Faible (1 jour/homme) | **Impact :** Critique (Évite double facturation et litiges bancaires).

### 2. Contrôle Transactionnel des Stocks et Empêchement des Stocks Négatifs (P0)
* **Constat :** Des plats en rupture (`stock=0`) peuvent être achetés et le stock passe en négatif (`BUG-004`).
* **Solution :**
  1. Utiliser une clause de verrouillage optimiste/pessimiste (`SELECT ... FOR UPDATE` ou transaction atomique).
  2. Plafonner l'ajout au panier au stock disponible.
  3. Ajouter une contrainte d'intégrité SQL : `CHECK (stock >= 0)`.
* **Effort :** Moyen (2 jours/homme) | **Impact :** Critique (Supprime les ruptures en cuisine).

### 3. Validation Stricte des Espèces et Rendu de Monnaie Positif (P0)
* **Constat :** N'importe quelle somme en espèces est acceptée, aboutissant à une monnaie négative (`BUG-005`).
* **Solution :** Valider obligatoirement côté frontend et backend que `cash_received >= total`. Si insuffisant, afficher une erreur bloquante et désactiver la soumission.
* **Effort :** Faible (0.5 jour/homme) | **Impact :** Critique (Évite les pertes financières pour les livreurs).

### 4. Vérification d'Ouverture du Restaurant et Montant Minimum (P1)
* **Constat :** Les commandes peuvent être passées dans des restaurants fermés (`BUG-002`) et sous le seuil minimum (`BUG-003`).
* **Solution :**
  1. Interdire l'ajout au panier et bloquer le checkout si `restaurant.is_open == False`.
  2. Bloquer le passage au checkout si `subtotal < restaurant.minimum_order` avec affichage du montant manquant.
* **Effort :** Faible (1 jour/homme) | **Impact :** Majeur (Respect des engagements contractuels des partenaires).

### 5. Recalcul Sécurisé du Sous-Total dans l'API de Coupons (P1)
* **Constat :** L'endpoint `/api/coupons/validate` fait confiance au `subtotal` arbitraire transmis dans le corps de la requête par le client (`BUG-012`).
* **Solution :** L'API doit recalculer le sous-total réel à partir des identifiants des plats et quantités en base de données, sans jamais se fier aux montants soumis par le client.
* **Effort :** Moyen (1.5 jours/homme) | **Impact :** Majeur (Prévention des fraudes aux réductions).

### 6. Correction du Filtre de Livraison et Recherche Multicritère (P2)
* **Constat :** Le filtre des frais de livraison est inversé (`BUG-007`) et la recherche ignore les descriptions des restaurants et plats (`BUG-008`).
* **Solution :**
  1. Corriger l'opérateur SQL (`<= Decimal(max_delivery)`).
  2. Indexer et rechercher sur `Restaurant.name`, `Restaurant.description` et `Product.name`.
* **Effort :** Moyen (1.5 jours/homme) | **Impact :** Moyen (Augmentation du taux de conversion et satisfaction UX).

### 7. Conditionnement des Avis Clients à une Commande Livrée Réelle (P2)
* **Constat :** N'importe quel internaute inscrit peut déposer une note sans avoir jamais commandé (`BUG-009`).
* **Solution :** Vérifier l'existence d'une commande au statut `delivered` associée au couple `(user_id, restaurant_id)` avant d'autoriser la publication de l'évaluation.
* **Effort :** Faible (0.5 jour/homme) | **Impact :** Moyen (Protection de la réputation des restaurateurs).

### 8. Machine à États Stricte pour les Statuts de Commande (Admin) (P2)
* **Constat :** Dans l'administration, une commande déjà livrée peut être rétrogradée en `pending`.
* **Solution :** Définir une machine à états (State Machine) avec transitions autorisées unidirectionnelles :
  `pending` ➔ `confirmed` ➔ `preparing` ➔ `in_delivery` ➔ `delivered` (ou `cancelled`).
* **Effort :** Moyen (1 jour/homme) | **Impact :** Moyen (Cohérence du suivi logistique).

---

## 3. Synthèse de Planification des Sprints

| Recommandation | Responsable | Sprint Cible | Effort Estimé | Priorité |
| :--- | :--- | :---: | :---: | :---: |
| **Fix Paiement PayPal (BUG-001)** | Backend Dev | Sprint 0 | 1 j/h | P0 |
| **Fix Contrôle Stocks & Intégrité (BUG-004)** | Backend / DB Dev | Sprint 0 | 2 j/h | P0 |
| **Fix Espèces & Rendu monnaie (BUG-005)** | Fullstack Dev | Sprint 0 | 0.5 j/h | P0 |
| **Fix Statut Ouvert & Minimum (BUG-002, 003)** | Backend Dev | Sprint 1 | 1 j/h | P1 |
| **Fix API Sous-total Coupon (BUG-012)** | API Dev | Sprint 1 | 1.5 j/h | P1 |
| **Fix Recherche & Filtres (BUG-007, 008)** | Frontend / Backend | Sprint 1 | 1.5 j/h | P2 |
| **Vérification d'achat sur Avis (BUG-009)** | Backend Dev | Sprint 2 | 0.5 j/h | P2 |
| **Machine à états des commandes (Admin)** | Backend Dev | Sprint 2 | 1 j/h | P2 |
