# Rapport d'Anomalie — BUG-009

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-009** |
| **Titre** | Possibilité de publier un avis et une note sans avoir jamais commandé dans le restaurant |
| **Module** | Système d'avis clients (`app/routes/shop.py`) |
| **Sévérité** | 🟡 **Moyenne (P2 - Medium)** |
| **Priorité** | 🟡 **Moyenne (P2)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Tout utilisateur connecté peut déposer une note et un commentaire sur la fiche de n'importe quel restaurant sans que le système ne vérifie s'il a déjà commandé ou consommé dans cet établissement.

Cette faille ouvre la porte au review bombing, à la diffamation malveillante ou aux faux avis de complaisance, faussant la note moyenne du restaurant.

---

## 2. Préconditions
* Utilisateur connecté (ex: nouvellement inscrit sans aucune commande).
* Page d'un restaurant (ex: `/restaurant/3`).

---

## 3. Étapes de Reproduction
1. Créer un nouveau compte utilisateur `test-avis@example.com`.
2. Se rendre sur la fiche de "Green Kitchen" (`/restaurant/3`).
3. Descendre à la section "Laisser un avis", mettre une note de 1/5 et un commentaire négatif.
4. Cliquer sur "Publier mon avis".

---

## 4. Résultat Attendu
Le système doit rejeter la publication avec un message : "Vous devez avoir reçu au moins une commande de cet établissement pour pouvoir donner votre avis."

---

## 5. Résultat Obtenu
L'avis est publié instantanément et la note du restaurant est immédiatement recalculée à la baisse.

---

## 6. Preuve Technique
Dans [app/routes/shop.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/shop.py#L89-L93) :
```python
# INTENTIONAL QA BUG: any logged-in user can review a restaurant without ordering it.
review = Review(user_id=current_user.id, restaurant_id=restaurant.id, rating=rating, comment=comment)
db.session.add(review)
```
Aucune vérification n'est effectuée sur la table `Order`.

---

## 7. Recommandation de Correction
Vérifier l'historique d'achat :
```python
has_ordered = Order.query.filter_by(
    user_id=current_user.id,
    restaurant_id=restaurant.id,
    status="delivered"
).first()
if not has_ordered:
    flash("Seuls les clients ayant commandé peuvent publier un avis.", "warning")
    return redirect(url_for("shop.restaurant_detail", restaurant_id=restaurant.id))
```
