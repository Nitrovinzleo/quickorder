# Rapport d'Anomalie — BUG-006

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-006** |
| **Titre** | Discordance entre le taux de remise affiché pour ATLAS (15%) et la réduction appliquée (10%) |
| **Module** | Moteur de coupons / Marketing (`seed.py`, `app/routes/orders.py`) |
| **Sévérité** | 🟡 **Moyenne (P2 - Medium)** |
| **Priorité** | 🟡 **Moyenne (P2)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
La promotion pour le partenaire Atlas / Orient est annoncée sur les bannières et dans le code avec le libellé **ATLAS15** promettant **15% de réduction**. Cependant, lors de l'application du coupon, la réduction calculée et déduite n'est que de **10%**.

Il s'agit d'une publicité trompeuse envers le consommateur pouvant entraîner des plaintes et un mécontentement des clients.

---

## 2. Préconditions
* Panier éligible d'au moins 20.00 €.
* Utilisation du code coupon `ATLAS15`.

---

## 3. Étapes de Reproduction
1. Remplir un panier pour 100.00 €.
2. Aller sur `/checkout`.
3. Saisir le coupon `ATLAS15` et cliquer sur valider.
4. Constater la ligne de réduction affichée.

---

## 4. Résultat Attendu
Une réduction de 15% (15.00 €) doit être déduite du sous-total.

---

## 5. Résultat Obtenu
La réduction appliquée est de 10.00 € (10%).

---

## 6. Preuve Technique
Dans [seed.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/seed.py#L88) :
```python
Coupon(code="ATLAS15", discount_percent=Decimal("10"), min_order_amount=Decimal("20"), max_discount=Decimal("50"), active=True, expires_at=datetime.utcnow() + timedelta(days=60))
```
La colonne `discount_percent` est initialisée à `Decimal("10")` au lieu de `15`.
Dans [app/routes/orders.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/orders.py#L24) :
```python
# INTENTIONAL QA BUG: the ATLAS promotion is advertised as 15% but the stored coupon is 10%.
```

---

## 7. Recommandation de Correction
Mettre à jour la base de données : `UPDATE coupon SET discount_percent = 15 WHERE code = 'ATLAS15';`.
