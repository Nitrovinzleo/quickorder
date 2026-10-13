# Rapport d'Anomalie — BUG-003

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-003** |
| **Titre** | Non-respect du montant minimum de commande défini par le restaurant |
| **Module** | Tunnel de commande (`app/routes/orders.py`, `app/routes/api.py`) |
| **Sévérité** | 🟠 **Majeure (P1 - Major)** |
| **Priorité** | 🔥 **Haute (P1)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Chaque restaurant définit un seuil de commande minimum (`minimum_order`), par exemple 20.00 € chez Burger Factory ou 15.00 € chez Tokyo Bowl. Ce montant est explicitement affiché sur la fiche du restaurant et dans l'API. Cependant, le tunnel d'achat autorise la commande pour un panier d'un montant inférieur.

Ce comportement enfreint les accords contractuels avec les restaurateurs, qui se retrouvent à livrer de trop petits paniers non rentables.

---

## 2. Préconditions
* Restaurant ayant un `minimum_order` > 0 € (ex: Burger Factory, min 20.00 €).
* Client connecté.

---

## 3. Étapes de Reproduction
1. Aller sur `/restaurant/1` (Burger Factory).
2. Ajouter au panier un seul article : "Frites maison" à 3.50 € (ou "Classic Burger" à 11.90 €).
3. Accéder à `/checkout` (le montant sous-total est inférieur à 20.00 €).
4. Sélectionner une adresse et confirmer la commande.

---

## 4. Résultat Attendu
Le système doit afficher une alerte bloquante : "Le montant minimum de commande chez Burger Factory est de 20.00 €. Il vous manque X.XX €." et désactiver le bouton de validation.

---

## 5. Résultat Obtenu
La commande est acceptée et enregistrée avec succès avec un total inférieur au minimum contractuel.

---

## 6. Preuve Technique
Extrait du code dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L106) :
```python
# INTENTIONAL QA BUGS:
# 2) minimum_order is displayed but never enforced;
```
Et dans l'API [app/routes/api.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/api.py#L180) :
```python
# INTENTIONAL QA BUGS: no restaurant-open check, no minimum-order check,
```

---

## 7. Recommandation de Correction
Ajouter une vérification avant confirmation :
```python
if subtotal < restaurant.minimum_order:
    flash(f"Montant minimum de {restaurant.minimum_order:.2f} € requis pour ce restaurant.", "warning")
    return redirect(url_for("shop.cart"))
```
