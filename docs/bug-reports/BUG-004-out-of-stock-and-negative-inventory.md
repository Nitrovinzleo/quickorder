# Rapport d'Anomalie — BUG-004

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-004** |
| **Titre** | Possibilité de commander des produits en rupture et passage des stocks en négatif |
| **Module** | Gestion des stocks / Panier / Commandes (`app/routes/shop.py`, `app/routes/orders.py`) |
| **Sévérité** | 🔴 **Critique (P0 - Blocker)** |
| **Priorité** | 🔥 **Immédiate (P0)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
L'application ne vérifie pas le stock réel des produits :
1. Un produit ayant un stock de 0 peut être ajouté au panier et commandé normalement.
2. Un utilisateur peut commander une quantité supérieure au stock restant (ex: demander 50 unités alors qu'il n'en reste que 2).
3. Lors de la commande, le stock est décrémenté sans garde-fou, ce qui fait passer la colonne `stock` en valeur négative en base de données.

---

## 2. Préconditions
* Produit "Salmon Bowl" (Restaurant Tokyo Bowl) ayant `stock = 2`.
* Ou produit "Veggie Burger" ayant `stock = 0`.

---

## 3. Étapes de Reproduction
1. Aller sur Tokyo Bowl (`/restaurant/2`).
2. Ajouter le "Salmon Bowl" au panier.
3. Dans `/cart`, modifier la quantité à `10` et cliquer sur "Mettre à jour".
4. Passer au checkout et confirmer la commande.
5. Vérifier la table `product` en base SQLite : `SELECT id, name, stock FROM product WHERE id = 7;`.

---

## 4. Résultat Attendu
La quantité maximale sélectionnable doit être bloquée à 2 (stock disponible). Si un produit a un stock de 0, il doit être étiqueté "Épuisé" et l'ajout au panier rendu impossible.

---

## 5. Résultat Obtenu
La commande de 10 unités est validée. En base de données, le stock du produit devient **-8**.

---

## 6. Preuve Technique
Dans [app/routes/shop.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/shop.py#L38) :
```python
# INTENTIONAL QA BUG: quantity is not capped by current stock.
update_cart(product_id.replace("qty_", ""), int(quantity))
```
Dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L68-L69) :
```python
# INTENTIONAL QA BUG: stock is reduced without checking whether it is sufficient.
product.stock -= item["quantity"]
```

---

## 7. Recommandation de Correction
1. Interdire l'ajout au panier si `product.stock <= 0`.
2. Plafonner la quantité maximale au stock restant : `qty = min(requested_qty, product.stock)`.
3. Utiliser une contrainte d'intégrité en base : `CHECK (stock >= 0)`.
