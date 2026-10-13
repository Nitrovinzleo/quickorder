# Retours d'Expérience & Tests Utilisateurs — QuickOrder

| Métadonnée | Valeur |
| :--- | :--- |
| **Projet** | QuickOrder QA Audit |
| **Document** | Synthèse des Sessions de Tests Utilisateurs (UX Feedback) |
| **Auteur** | Équipe QA — Vincent Hoebler (Nitrovinzleo) |
| **Échantillon** | 2 testeurs cibles (Profils variés) |
| **Nombre de scénarios** | 3 scénarios représentatifs |

---

## 1. Profils des Testeurs

### Testeur 1 : Maxime, 23 ans
* **Profil :** Étudiant en école de commerce, utilisateur quotidien d'applications de livraison (UberEats, Deliveroo).
* **Attentes :** Rapidité, transparence sur les frais, fluidité du panier.

### Testeuse 2 : Sophie, 44 ans
* **Profil :** Responsable administrative, commande occasionnellement pour la famille le week-end. Moins familière des interfaces complexes.
* **Attentes :** Clarté des étapes de paiement, lisibilité des filtres et sécurité des transactions.

---

## 2. Déroulement des Scénarios de Test

### Scénario 1 : Recherche d'un repas végétarien et commande rapide
* **Tâche confiée :** Trouver un restaurant proposant des plats végétariens, ajouter un plat et aller jusqu'au récapitulatif.
* **Retours & Observations :**
  * *Maxime :* « J'ai tapé "veggie" dans la barre de recherche et aucun resto n'est sorti alors que Burger Factory a un Veggie Burger. C'est frustrant de devoir cliquer sur chaque restaurant pour vérifier le menu. »
  * *Sophie :* « J'ai cliqué sur le filtre pour avoir des frais de livraison pas chers (<= 2.50 €) et ça m'a affiché Tokyo Bowl à 3.49 € ! Je ne comprenais pas pourquoi. »
* **Problème identifié :** Moteur de recherche limité au nom du restaurant et filtre de livraison inversé.
* **Impact :** Friction dès l'entrée sur le site, risque d'abandon immédiat.
* **Priorité :** Haute (P1).

### Scénario 2 : Utilisation d'un code de réduction promotionnel
* **Tâche confiée :** Commander pour environ 25 € et utiliser le code promo affiché en bannière (`ATLAS15`).
* **Retours & Observations :**
  * *Maxime :* « La bannière disait -15%, mais quand j'ai validé le code ATLAS15, j'ai vu seulement 2.50 € de réduction sur mon panier de 25 € au lieu de 3.75 €. Je me suis senti trompé sur le calcul. »
  * *Sophie :* « Le message d'erreur quand le coupon ne passe pas est en anglais ou peu explicite. Ce serait bien d'avoir un rappel des conditions directement sous le champ de saisie. »
* **Verbatim clé :** « Si une appli me promet 15% et n'en applique que 10%, j'annule ma commande tout de suite. »
* **Impact :** Rupture de confiance commerciale, réclamations client.
* **Priorité :** Haute (P1).

### Scénario 3 : Paiement et finalisation de commande
* **Tâche confiée :** Sélectionner le mode de paiement (PayPal ou Espèces) et finaliser la commande.
* **Retours & Observations :**
  * *Maxime (Paiement PayPal) :* « J'ai payé avec PayPal, puis en allant dans mon profil j'ai vu deux commandes avec deux numéros différents créées à la même minute. Si j'étais débité deux fois, je contacterais immédiatement le service client pour bloquer le prélèvement. »
  * *Sophie (Paiement Espèces) :* « J'ai tapé 10 € pour une commande de 22 € pour voir si le site calculait, et ça a validé ! Le site m'indique "Monnaie à rendre : -12.00 €". Ça n'a aucun sens mathématique. »
* **Impact :** Incompréhension totale et sentiment de faille technique majeure.
* **Priorité :** Critique (P0).

---

## 3. Synthèse des Frictions UX & Recommandations

| ID | Point de Friction UX | Fréquence | Impact | Verbatim Utilisateur | Amélioration Recommandée | Priorité |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: |
| **UX-01** | Recherche textuelle inefficace | 100 % | Majeur | « La recherche ne trouve pas les plats. » | Indexer les ingrédients, descriptions et catégories de produits. | P1 |
| **UX-02** | Filtre de livraison erroné | 100 % | Moyen | « Le filtre fait le contraire de ce qu'il dit. » | Corriger l'opérateur SQL (`<= 2.50 €`). | P2 |
| **UX-03** | Taux de coupon incohérent | 100 % | Majeur | « J'ai l'impression d'une fausse promotion. » | Aligner la remise réelle en base sur la promesse de la bannière. | P1 |
| **UX-04** | Double commande PayPal | 100 % | Critique | « J'ai été commandé en double sans le vouloir. » | Supprimer la duplication et fiabiliser le callback PayPal. | P0 |
| **UX-05** | Rendu de monnaie négatif | 100 % | Majeur | « Ça affiche de la monnaie négative ! » | Valider `cash_received >= total` dès la saisie du champ. | P0 |
