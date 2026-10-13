# Rapport d'Anomalie — BUG-007

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-007** |
| **Titre** | Inversion de l'opérateur dans le filtre des frais de livraison en page d'accueil |
| **Module** | Catalogue / Filtres accueil (`app/routes/main.py`) |
| **Sévérité** | 🟡 **Moyenne (P2 - Medium)** |
| **Priorité** | 🟡 **Moyenne (P2)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Sur la page d'accueil, un filtre rapide permet à l'utilisateur de chercher les restaurants économiques avec des **frais de livraison réduits (<= 2.50 €)**.

Cependant, lorsque l'utilisateur sélectionne ce filtre, le système fait l'inverse exact : il n'affiche que les restaurants dont les frais sont strictement supérieurs à 2.50 € (les plus chers).

---

## 2. Préconditions
* Être sur la page d'accueil `/`.
* Restaurants en base : Burger Factory (2.99 €), Tokyo Bowl (3.49 €), Green Kitchen (1.99 €), Pizza Roma (2.49 €).

---

## 3. Étapes de Reproduction
1. Aller sur `http://127.0.0.1:5000/`.
2. Cliquer sur le filtre "Livraison <= 2.50 €".
3. Observer les restaurants retournés.

---

## 4. Résultat Attendu
Seuls Green Kitchen (1.99 €) et Pizza Roma (2.49 €) doivent apparaître.

---

## 5. Résultat Obtenu
Ce sont Burger Factory (2.99 €) et Tokyo Bowl (3.49 €) qui s'affichent. Les restaurants économiques sont masqués.

---

## 6. Preuve Technique
Dans [app/routes/main.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/main.py#L16-L18) :
```python
# INTENTIONAL QA BUG: the delivery filter is reversed. A maximum of 2.50 €
# is filtered with >= instead of <=.
if max_delivery:
    query = query.filter(Restaurant.delivery_fee >= Decimal(max_delivery))
```
L'opérateur utilisé est `>=` au lieu de `<=`.

---

## 7. Recommandation de Correction
Remplacer par :
```python
query = query.filter(Restaurant.delivery_fee <= Decimal(max_delivery))
```
