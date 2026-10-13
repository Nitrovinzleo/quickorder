# Rapport d'Anomalie — BUG-005

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-005** |
| **Titre** | Acceptation d'un paiement en espèces d'un montant inférieur au total et calcul de monnaie négative |
| **Module** | Tunnel de paiement / Espèces (`app/routes/orders.py`, `app/routes/api.py`) |
| **Sévérité** | 🔴 **Critique (P0 - Blocker)** |
| **Priorité** | 🔥 **Immédiate (P0)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Lors d'un paiement en espèces ("Cash on delivery"), l'utilisateur est invité à saisir la somme qu'il donnera au livreur afin de calculer la monnaie à rendre (`change_due`). 

Le système accepte n'importe quelle somme, y compris un montant dérisoire ou inférieur au coût total de la commande (ex: 5.00 € pour une commande de 30.00 €). Le statut passe à `confirmed` / `paid` et le champ `change_due` devient négatif (-25.00 €), ouvrant la porte à des commandes non payées.

---

## 2. Préconditions
* Commande d'un montant total de 20.00 € ou plus.
* Utilisateur au stade du paiement.

---

## 3. Étapes de Reproduction
1. Créer un panier pour un montant total de 25.00 €.
2. Aller sur `/checkout`.
3. Choisir le mode de paiement : **Espèces (cash)**.
4. Dans le champ "Montant remis en espèces", saisir : `5.00`.
5. Confirmer la commande.

---

## 4. Résultat Attendu
Le système doit refuser la soumission avec une erreur de validation : "Le montant remis en espèces doit être supérieur ou égal au montant total de la commande (25.00 €)."

---

## 5. Résultat Obtenu
La commande est acceptée et marquée payée. En base, `cash_received = 5.00` et `change_due = -20.00`.

---

## 6. Preuve Technique
Extrait du code dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L39-L40) :
```python
# INTENTIONAL QA BUG: any cash amount is accepted, even if it is lower than the total.
change_due = (cash_received_decimal - total).quantize(Decimal("0.01"))
```
Aucun test `if cash_received_decimal < total` n'est réalisé.

---

## 7. Recommandation de Correction
Ajouter une règle de validation bloquante :
```python
if payment == "cash" and cash_received_decimal < total:
    flash(f"Le montant remis ({cash_received_decimal:.2f} €) est insuffisant pour régler le total de {total:.2f} €.", "danger")
    return redirect(url_for("orders.checkout"))
```
