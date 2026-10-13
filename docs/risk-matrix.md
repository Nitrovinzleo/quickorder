# Matrice des Risques — QuickOrder

| Métadonnée | Valeur |
| :--- | :--- |
| **Projet** | QuickOrder QA Audit |
| **Document** | Matrice d'Analyse et de Priorisation des Risques |
| **Auteur** | Équipe QA — Vincent Hoebler (Nitrovinzleo) |
| **Version** | 1.0 |

---

## 1. Méthodologie d'Évaluation

La criticité de chaque risque est calculée selon la formule standard :
$$\text{Score de Criticité} = \text{Probabilité (1 à 4)} \times \text{Impact (1 à 4)}$$

### Échelle de Probabilité :
* **1 (Faible) :** Scénario rare nécessitant une manipulation inhabituelle.
* **2 (Moyenne) :** Susceptible de se produire périodiquement.
* **3 (Élevée) :** Très probable lors d'un usage quotidien standard.
* **4 (Certaine) :** Inhérent au code actuel, systématique dès l'action réalisée.

### Échelle d'Impact :
* **1 (Mineur) :** Gêne visuelle ou cosmétique mineure.
* **2 (Moyen) :** Fonctionnalité secondaire dégradée, contournement facile.
* **3 (Majeur) :** Blocage d'un parcours clé ou mécontentement client fort.
* **4 (Critique) :** Perte financière directe, corruption de données, rupture de service.

---

## 2. Tableau de la Matrice des Risques

| ID | Risque Identifié | Catégorie | Probabilité | Impact | Score | Criticité | Mesure d'Atténuation (Mitigation) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **R-01** | **Duplication de commandes lors du paiement PayPal** | Financier / Facturation | 4 | 4 | **16** | 🔴 **Critique** | Rendre les transactions de création idempotentes avec un identifiant unique de transaction. |
| **R-02** | **Encaissement insuffisant en espèces (Cash underpayment)** | Financier / Fraude | 4 | 4 | **16** | 🔴 **Critique** | Valider obligatoirement que `cash_received >= total` avant d'accepter la commande. |
| **R-03** | **Vente de plats en rupture de stock (Stock négatif)** | Logistique / Exploitation | 4 | 4 | **16** | 🔴 **Critique** | Verrouiller transactionnellement les stocks lors du passage de commande avec rollback si stock insuffisant. |
| **R-04** | **Prise de commandes dans un établissement fermé** | Légal / Relationnel | 4 | 3 | **12** | 🟠 **Majeur** | Vérifier le statut `is_open == True` au moment de l'ajout au panier et au checkout. |
| **R-05** | **Ignorance du montant minimum de commande** | Financier / Partenariat | 4 | 3 | **12** | 🟠 **Majeur** | Bloquer la soumission du checkout si `subtotal < minimum_order`. |
| **R-06** | **Falsification du sous-total via l'API pour bypasser un coupon** | Sécurité / API | 3 | 4 | **12** | 🟠 **Majeur** | Ne jamais faire confiance au montant fourni par le client ; recalculer le panier côté serveur. |
| **R-07** | **Crash non géré de l'API (HTTP 500) sur listing de commandes** | Technique / Disponibilité | 4 | 3 | **12** | 🟠 **Majeur** | Corriger la fonction `api_customer()` pour gérer l'absence d'utilisateur authentifié. |
| **R-08** | **Taux de promotion trompeur (Coupon ATLAS annoncé 15% mais 10% appliqué)** | Juridique / Consommateur | 4 | 2 | **8** | 🟡 **Moyen** | Aligner la configuration en base de données ou le texte promotionnel pour éviter les litiges. |
| **R-09** | **Filtre de livraison inversé masquant les restaurants économiques** | Ergonomie / Rétention | 4 | 2 | **8** | 🟡 **Moyen** | Inverser l'opérateur de comparaison dans le filtre SQL (`<=` au lieu de `>=`). |
| **R-10** | **Publication d'avis frauduleux sans preuve d'achat** | Intégrité / Réputation | 3 | 2 | **6** | 🟡 **Moyen** | Restreindre le formulaire d'évaluation aux utilisateurs ayant une commande `delivered` pour ce restaurant. |

---

## 3. Matrice Visuelle Criticité / Priorisation

```text
 IMPACT
   ▲
 4 │ [ ]                  [R-06]             [R-01] [R-02] [R-03]
 3 │ [ ]                  [ ]                [R-04] [R-05] [R-07]
 2 │ [ ]                  [R-10]             [R-08] [R-09]
 1 │ [ ]                  [ ]                [ ]
   └─────────────────────────────────────────────────────────────►
     1                    2                  3                    4  PROBABILITÉ
```
