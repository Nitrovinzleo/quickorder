# Rapport d'Anomalie — BUG-008

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-008** |
| **Titre** | La barre de recherche ignore la description et les spécialités culinaires des restaurants |
| **Module** | Moteur de recherche (`app/routes/main.py`, `app/routes/api.py`) |
| **Sévérité** | 🟡 **Moyenne (P2 - Medium)** |
| **Priorité** | 🟡 **Moyenne (P2)** |
| **Statut** | Ouvert / Reproductible |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Lorsqu'un utilisateur recherche un terme culinaire spécifique (par exemple "salade", "bowls", "bio" ou "sushi") dans la barre de recherche principale, aucun résultat n'est retourné alors que plusieurs restaurants décrivent explicitement ces plats dans leur description.

Le filtre SQL ne porte en effet que sur la colonne `Restaurant.name`.

---

## 2. Préconditions
* Être sur la page d'accueil ou utiliser l'endpoint `/api/restaurants?q=...`.
* Restaurant "Green Kitchen" ayant pour description : "Salades, wraps et options végétariennes."

---

## 3. Étapes de Reproduction
1. Sur `/`, saisir dans la barre de recherche le mot : `Salades`.
2. Appuyer sur Entrée.

---

## 4. Résultat Attendu
Le restaurant "Green Kitchen" doit apparaître dans les résultats.

---

## 5. Résultat Obtenu
La liste est vide : "Aucun restaurant trouvé."

---

## 6. Preuve Technique
Dans [app/routes/main.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/main.py#L20-L21) :
```python
# INTENTIONAL QA BUG: search only checks the restaurant name, not its description.
query = query.filter(Restaurant.name.ilike(f"%{q}%"))
```
Et dans l'API [app/routes/api.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/api.py#L72-L73) :
```python
# INTENTIONAL QA BUG: API search ignores restaurant description.
query = query.filter(Restaurant.name.ilike(f"%{q}%"))
```

---

## 7. Recommandation de Correction
Élargir la condition de recherche :
```python
from sqlalchemy import or_
query = query.filter(or_(
    Restaurant.name.ilike(f"%{q}%"),
    Restaurant.description.ilike(f"%{q}%")
))
```
