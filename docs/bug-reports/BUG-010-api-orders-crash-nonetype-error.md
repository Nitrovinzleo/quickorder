# Rapport d'Anomalie — BUG-010

| Champ | Valeur |
| :--- | :--- |
| **Identifiant** | **BUG-010** |
| **Titre** | Crash serveur HTTP 500 sur l'endpoint API `GET /api/orders` suite à un `AttributeError` |
| **Module** | API REST v1 (`app/routes/api.py`) |
| **Sévérité** | 🟠 **Majeure (P1 - Major)** |
| **Priorité** | 🔥 **Haute (P1)** |
| **Statut** | Ouvert / Reproductible (détecté par pytest) |
| **Auteur** | Vincent Hoebler (Nitrovinzleo) |

---

## 1. Contexte & Description
Lorsqu'un client technique ou un script externe interroge l'endpoint `GET /api/orders` en fournissant la clé d'API valide (`X-API-Key: quickorder-demo-key`), le serveur Flask plante avec une erreur interne **HTTP 500 Internal Server Error** : `AttributeError: 'NoneType' object has no attribute 'id'`.

Ce bug a été initialement révélé lors de l'exécution de la suite de tests automatisés `pytest tests/test_smoke.py`.

---

## 2. Préconditions
* Application QuickOrder lancée.
* Clé API valide : `quickorder-demo-key`.
* Appel effectué sans session cookie de navigateur active (appel API REST pur).

---

## 3. Étapes de Reproduction
Exécuter la requête suivante avec curl ou PowerShell :
```powershell
curl -X GET "http://127.0.0.1:5000/api/orders" -H "X-API-Key: quickorder-demo-key"
```
Ou exécuter :
```powershell
python -m pytest tests/test_smoke.py -k test_api_orders_with_key
```

---

## 4. Résultat Attendu
Le serveur doit répondre avec le statut **HTTP 200 OK** et retourner un objet JSON contenant la liste des commandes du compte de démonstration (`alice@example.com`).

---

## 5. Résultat Obtenu
Le serveur retourne **HTTP 500 Internal Server Error**.

Traceback d'erreur :
```text
File "app/routes/api.py", line 219, in list_orders
    query = Order.query.filter_by(user_id=api_customer().id)
                                          ^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'id'
```

---

## 6. Preuve Technique
Dans [app/routes/api.py](file:///c:/Users/vhoeb/Desktop/Ecole/B3/test/projet/app/routes/api.py#L27-L31) :
```python
def api_customer():
    if current_user.is_authenticated:
        return current_user
    user = User.query.filter_by(email="alice@example.com").first()
    return user
```
Si la base de données n'a pas encore de session liée ou si l'utilisateur Alice n'est pas trouvé sous cette forme exacte, `api_customer()` retourne `None`, et l'accès à `.id` provoque l'exception `AttributeError` non interceptée.

---

## 7. Recommandation de Correction
Sécuriser la résolution du client API :
```python
customer = api_customer()
if not customer:
    return jsonify({"error": "No API customer found. Please run seed.py."}), 404
query = Order.query.filter_by(user_id=customer.id)
```
