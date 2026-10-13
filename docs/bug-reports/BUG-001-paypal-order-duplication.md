# Rapport d'Anomalie — BUG-001

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-001** |
| **Titre** | Duplication automatique des commandes lors d'un paiement via PayPal |
| **Module** | Tunnel de commande / Checkout (`app/routes/orders.py`, `app/routes/api.py`) |
| **Sévérité** | 🔴 **Critique (P0 - Blocker)** |
| **Priorité** | 🔥 **Immédiate (P0)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Lorsqu'un utilisateur final finalise son panier en choisissant le mode de paiement **PayPal**, le système exécute deux fois la fonction de création de commande `build_order()`. Deux commandes strictement identiques sont enregistrées en base de données avec deux identifiants distincts.

Ce bug entraîne une double facturation potentielle, une double préparation en cuisine par le restaurant et un mécontentement client immédiat.

---

## 2. Préconditions
* Utilisateur connecté (ex: `alice@example.com`).
* Au moins un article dans le panier (ex: "Classic Burger", 11.90 €).
* Une adresse de livraison valide sélectionnée.

---

## 3. Étapes de Reproduction
1. Se connecter à l'application.
2. Ajouter un produit au panier et se rendre sur `/checkout`.
3. Sélectionner une adresse de livraison.
4. Cocher le mode de paiement : **PayPal**.
5. Cliquer sur le bouton **"Confirmer la commande"**.
6. Accéder à l'espace profil `/profile` ou exécuter la requête SQLite `SELECT id, user_id, total, created_at FROM "order";`.

---

## 4. Résultat Attendu
Une seule commande doit être créée avec le statut `confirmed` et débitée via PayPal.

---

## 5. Résultat Obtenu
Deux enregistrements `Order` consécutifs sont créés en base de données (ex: Commande #1 et Commande #2) avec le même montant, les mêmes articles et la même heure de création.

---

## 6. Preuve Technique
Extrait du code source incriminé dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L118-L122) :
```python
# Ligne 118 dans app/routes/orders.py :
if payment == "paypal":
    duplicate, _ = build_order(user_id=current_user.id, address=address, restaurant=restaurant,
                               subtotal=subtotal, delivery_fee=delivery_fee, discount=discount,
                               total=total, payment=payment, customer_note="Copie de secours PayPal",
                               cash_received=cash_received)
    add_order_items(duplicate, items)
```
Le code crée explicitement un double de commande avec la mention "Copie de secours PayPal".

---

## 7. Recommandation de Correction
Supprimer le bloc de duplication conditionnelle `if payment == "paypal"` et implémenter un token d'idempotence unique généré côté client/session pour empêcher toute double création.
