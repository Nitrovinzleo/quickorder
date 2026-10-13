# Rapport d'Anomalie — BUG-002

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-002** |
| **Titre** | Absence de contrôle sur le statut d'ouverture du restaurant lors du checkout |
| **Module** | Catalogue / Panier / Commandes (`app/routes/shop.py`, `app/routes/orders.py`) |
| **Sévérité** | 🟠 **Majeure (P1 - Major)** |
| **Priorité** | 🔥 **Haute (P1)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Un restaurant partenaire dont la propriété `is_open` est positionnée à `False` en base de données peut continuer à recevoir des commandes payées sans aucun avertissement ni blocage dans le tunnel d'achat.

Les clients peuvent donc commander et payer des repas chez un établissement fermé, entraînant des commandes non honorées et une obligation de remboursement manuel.

---

## 2. Préconditions
* Un restaurant partenaire a son champ `is_open = False`.
* Un client a ajouté des plats de ce restaurant dans son panier.

---

## 3. Étapes de Reproduction
1. Positionner un restaurant comme fermé (ex: `UPDATE restaurant SET is_open = 0 WHERE id = 1;`).
2. Accéder à l'URL du restaurant `/restaurant/1`.
3. Cliquer sur "Ajouter au panier".
4. Accéder à `/checkout` et valider la commande par carte ou espèces.

---

## 4. Résultat Attendu
Le système doit désactiver l'ajout au panier avec la mention "Restaurant actuellement fermé" et refuser la validation finale au checkout.

---

## 5. Résultat Obtenu
La commande est acceptée, validée en base de données et débitée sans qu'aucune vérification du booléen `restaurant.is_open` ne soit effectuée.

---

## 6. Preuve Technique
Extrait du code source dans [app/routes/shop.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/shop.py#L16-L20) :
```python
# INTENTIONAL QA BUGS:
# - stock=0 is allowed into the cart;
# - a closed restaurant can still receive orders;
# - stock is not rechecked against the requested quantity.
if not product.available:
    flash("Produit indisponible.", "danger")
```
Et dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L104-L105) :
```python
# INTENTIONAL QA BUGS:
# 1) restaurant.is_open is not checked here;
```

---

## 7. Recommandation de Correction
Ajouter une vérification préalable :
```python
if not restaurant.is_open:
    flash("Ce restaurant est actuellement fermé et n'accepte pas de commande.", "danger")
    return redirect(url_for("shop.cart"))
```
