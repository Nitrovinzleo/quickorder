# Cahier de Recette & Cas de Test — QuickOrder

| Métadonnée | Valeur |
| :--- | :--- |
| **Projet** | QuickOrder QA Audit |
| **Document** | Suite de Tests Fonctionnels, Limites, Erreurs & Métier |
| **Auteur** | Équipe QA — Vincent Hoebler (Nitrovinzleo) |
| **Volume de tests** | **28 cas de test exécutés** (7 Nominaux, 7 Limites, 7 Erreurs, 7 Métier) |
| **Statut global** | **15 PASS / 13 FAIL** |

---

## 1. Synthèse par Catégorie

* **Cas Nominaux (TC-NOM) :** 7 cas — 6 PASS / 1 FAIL
* **Cas aux Limites (TC-LIM) :** 7 cas — 3 PASS / 4 FAIL
* **Cas d'Erreur (TC-ERR) :** 7 cas — 4 PASS / 3 FAIL
* **Règles Métier (TC-BUS) :** 7 cas — 2 PASS / 5 FAIL

---

## 2. Cas Nominaux (TC-NOM)

### TC-NOM-01 : Connexion utilisateur avec identifiants valides
* **Objectif :** Vérifier qu'un utilisateur enregistré peut s'authentifier avec succès.
* **Préconditions :** Base initialisée avec `seed.py`.
* **Données :** Email : `alice@example.com` | Mot de passe : `Password123!`
* **Étapes :**
  1. Accéder à `http://127.0.0.1:5000/login`.
  2. Renseigner l'email et le mot de passe.
  3. Cliquer sur "Se connecter".
* **Résultat attendu :** Connexion réussie, redirection vers l'accueil ou le profil, affichage de "Mon profil" et "Déconnexion".
* **Résultat obtenu :** Conforme. Redirection avec session active.
* **Statut :** **PASS**

### TC-NOM-02 : Consultation du catalogue et affichage des restaurants
* **Objectif :** Vérifier que la page d'accueil affiche les restaurants partenaires avec leurs informations.
* **Préconditions :** Serveur actif.
* **Données :** URL `/`
* **Étapes :**
  1. Ouvrir la page d'accueil.
  2. Vérifier les fiches restaurant (Burger Factory, Tokyo Bowl, etc.).
* **Résultat attendu :** Les 4 restaurants sont listés avec note, délai de livraison et spécialité.
* **Résultat obtenu :** Conforme. Les restaurants sont correctement affichés.
* **Statut :** **PASS**

### TC-NOM-03 : Ajout d'un plat au panier
* **Objectif :** Vérifier l'ajout d'un produit disponible au panier.
* **Préconditions :** Panier vide.
* **Données :** Produit "Classic Burger" (11.90 €) du restaurant "Burger Factory".
* **Étapes :**
  1. Aller sur `/restaurant/1`.
  2. Cliquer sur "Ajouter au panier" pour le Classic Burger.
  3. Ouvrir `/cart`.
* **Résultat attendu :** Le produit apparaît dans le panier avec la quantité 1 et le sous-total de 11.90 €.
* **Résultat obtenu :** Conforme. Notification de succès et panier à jour.
* **Statut :** **PASS**

### TC-NOM-04 : Application d'un coupon promotionnel valide (WELCOME10)
* **Objectif :** Vérifier l'application d'une réduction de 10% sur un panier éligible.
* **Préconditions :** Connecté en tant qu'Alice, panier d'un montant supérieur au minimum de 20 €.
* **Données :** 2 x "Classic Burger" (23.80 €) | Code coupon : `WELCOME10`.
* **Étapes :**
  1. Accéder au checkout `/checkout`.
  2. Saisir `WELCOME10` dans le champ coupon et valider.
* **Résultat attendu :** Réduction de 10% (2.38 €) appliquée, total recalculé.
* **Résultat obtenu :** Conforme. 2.38 € déduits du total.
* **Statut :** **PASS**

### TC-NOM-05 : Validation d'une commande par carte bancaire
* **Objectif :** Passer une commande complète payée par carte bancaire.
* **Préconditions :** Utilisateur connecté avec adresse enregistrée, panier valide.
* **Données :** Mode de paiement : "Carte bancaire".
* **Étapes :**
  1. Sur `/checkout`, sélectionner l'adresse de livraison et le mode "Carte".
  2. Cliquer sur "Confirmer la commande".
* **Résultat attendu :** Commande validée, redirection vers le détail de la commande, statut "confirmed".
* **Résultat obtenu :** Conforme. Commande créée avec référence `PAY-...`.
* **Statut :** **PASS**

### TC-NOM-06 : Consultation de l'historique des commandes dans le profil
* **Objectif :** Vérifier que les commandes passées sont consultables dans l'espace client.
* **Préconditions :** Au moins 1 commande passée par l'utilisateur connecté.
* **Données :** URL `/profile`.
* **Étapes :**
  1. Aller sur le profil utilisateur.
  2. Vérifier la section "Mes commandes".
* **Résultat attendu :** La commande précédente apparaît avec son numéro, date, restaurant et montant.
* **Résultat obtenu :** Conforme.
* **Statut :** **PASS**

### TC-NOM-07 : Commande avec paiement PayPal
* **Objectif :** Vérifier le passage d'une commande réglée via PayPal.
* **Préconditions :** Panier avec 1 article, utilisateur connecté.
* **Données :** Mode de paiement : "PayPal".
* **Étapes :**
  1. Sur `/checkout`, sélectionner PayPal et soumettre.
  2. Consulter la base de données ou la liste des commandes.
* **Résultat attendu :** Une seule commande enregistrée pour l'utilisateur.
* **Résultat obtenu :** **ANOMALIE (BUG-001)** : Le système génère deux commandes identiques dans la base.
* **Statut :** **FAIL**

---

## 3. Cas aux Limites (TC-LIM)

### TC-LIM-01 : Mise à jour de la quantité à 0 dans le panier
* **Objectif :** Tester le comportement quand l'utilisateur définit la quantité à 0 dans le panier.
* **Préconditions :** 1 article dans le panier.
* **Données :** Quantité = 0.
* **Étapes :**
  1. Sur `/cart`, changer la quantité à 0 et cliquer sur "Mettre à jour".
* **Résultat attendu :** L'article est retiré du panier ou une erreur indique que la quantité doit être >= 1.
* **Résultat obtenu :** L'article reste ou le panier se met à jour sans suppression propre.
* **Statut :** **FAIL**

### TC-LIM-02 : Commande exactement au montant minimum d'un coupon
* **Objectif :** Tester le coupon WELCOME10 avec un sous-total exactement égal au seuil de 20.00 €.
* **Préconditions :** Panier avec sous-total = 20.00 €.
* **Données :** Code `WELCOME10` (seuil min = 20.00 €).
* **Étapes :**
  1. Renseigner le coupon au checkout.
* **Résultat attendu :** Le coupon est accepté (condition `>=`).
* **Résultat obtenu :** Conforme. Le coupon est accepté dès 20.00 €.
* **Statut :** **PASS**

### TC-LIM-03 : Commande à 19.99 € pour un coupon exigeant 20.00 €
* **Objectif :** Tester le coupon à 1 centime en dessous du seuil exigé.
* **Préconditions :** Panier = 19.99 €.
* **Données :** Code `WELCOME10`.
* **Étapes :**
  1. Appliquer le coupon sur `/checkout`.
* **Résultat attendu :** Rejet avec message "Montant minimum de 20.00 € requis."
* **Résultat obtenu :** Conforme. Coupon refusé.
* **Statut :** **PASS**

### TC-LIM-04 : Quantité demandée supérieure au stock disponible
* **Objectif :** Tester l'ajout d'une quantité supérieure au stock restant du plat.
* **Préconditions :** Plat "Salmon Bowl" (stock initial = 2 unités).
* **Données :** Quantité demandée = 10 unités.
* **Étapes :**
  1. Dans le panier, passer la quantité de Salmon Bowl à 10.
  2. Valider le checkout.
* **Résultat attendu :** Blocage : la quantité ne peut pas excéder le stock réel (2).
* **Résultat obtenu :** **ANOMALIE (BUG-004)** : La commande passe et le stock devient négatif (-8).
* **Statut :** **FAIL**

### TC-LIM-05 : Plafonnement de la réduction maximale d'un coupon
* **Objectif :** Tester le plafonnement (`max_discount`) d'un coupon sur une très grosse commande.
* **Données :** Commande de 200 € avec `WELCOME10` (10%, max discount = 8.00 €).
* **Étapes :**
  1. Appliquer le coupon sur la commande de 200 €.
* **Résultat attendu :** Réduction limitée à 8.00 € (et non 20.00 €).
* **Résultat obtenu :** Conforme. La réduction est bien plafonnée à 8.00 €.
* **Statut :** **PASS**

### TC-LIM-06 : Paiement en espèces avec montant exactement égal au total
* **Objectif :** Tester le paiement Cash avec montant exact.
* **Données :** Total commande = 15.49 €, Espèces remises = 15.49 €.
* **Étapes :**
  1. Soumettre avec mode espèces et montant exact.
* **Résultat attendu :** Commande acceptée, monnaie à rendre = 0.00 €.
* **Résultat obtenu :** Conforme. Monnaie due = 0.00 €.
* **Statut :** **PASS**

### TC-LIM-07 : Paiement en espèces avec montant inférieur au total (Sous-paiement)
* **Objectif :** Tester le paiement Cash avec montant insuffisant.
* **Données :** Total commande = 25.00 €, Espèces remises = 10.00 €.
* **Étapes :**
  1. Soumettre le checkout en saisissant 10 € en espèces.
* **Résultat attendu :** Rejet de la commande : le montant remis doit être supérieur ou égal au total.
* **Résultat obtenu :** **ANOMALIE (BUG-005)** : Commande acceptée avec monnaie à rendre négative (-15.00 €).
* **Statut :** **FAIL**

---

## 4. Cas d'Erreur (TC-ERR)

### TC-ERR-01 : Connexion avec mot de passe erroné
* **Objectif :** Vérifier le rejet d'une tentative de connexion avec mot de passe incorrect.
* **Données :** `alice@example.com` / `WrongPassword999`
* **Résultat attendu :** Message d'erreur "Identifiants invalides", accès refusé.
* **Résultat obtenu :** Conforme.
* **Statut :** **PASS**

### TC-ERR-02 : Inscription avec une adresse email déjà existante
* **Objectif :** Vérifier l'unicité de l'email à la création de compte.
* **Données :** Tentative de création avec `alice@example.com`.
* **Résultat attendu :** Message "Cet email est déjà utilisé".
* **Résultat obtenu :** Conforme.
* **Statut :** **PASS**

### TC-ERR-03 : Saisie d'un code coupon inexistant
* **Objectif :** Tester la saisie d'un code promo erroné.
* **Données :** Code : `PROMOINCONNUE99`
* **Résultat attendu :** Alerte "Coupon invalide ou inactif".
* **Résultat obtenu :** Conforme.
* **Statut :** **PASS**

### TC-ERR-04 : Saisie d'un coupon expiré (EXPIRED10)
* **Objectif :** Tester la tentative d'utilisation d'un coupon dont la date limite est dépassée.
* **Données :** Code : `EXPIRED10` (expiré depuis 1 jour).
* **Résultat attendu :** Coupon refusé avec mention "Coupon expiré".
* **Résultat obtenu :** Conforme. Le coupon expiré est bien rejeté.
* **Statut :** **PASS**

### TC-ERR-05 : Appel API sans clé d'authentification
* **Objectif :** Tester la protection de l'API REST contre les accès anonymes.
* **Données :** `GET /api/restaurants` sans en-tête `X-API-Key`.
* **Résultat attendu :** Code HTTP 401 Unauthorized.
* **Résultat obtenu :** Conforme (HTTP 401).
* **Statut :** **PASS**

### TC-ERR-06 : Crash de l'API sur consultation des commandes (GET /api/orders)
* **Objectif :** Consulter l'historique des commandes via l'API avec la clé valide.
* **Données :** `GET /api/orders` avec en-tête `X-API-Key: quickorder-demo-key`.
* **Résultat attendu :** Code HTTP 200 avec la liste JSON des commandes.
* **Résultat obtenu :** **ANOMALIE (BUG-010)** : Crash serveur HTTP 500 (`AttributeError: 'NoneType' object has no attribute 'id'`).
* **Statut :** **FAIL**

### TC-ERR-07 : Falsification du montant sous-total envoyé à l'API de coupon
* **Objectif :** Tester l'injection d'un sous-total artificiellement élevé dans l'API.
* **Données :** `POST /api/coupons/validate` avec payload `{"code": "SAVE20", "subtotal": 1000.00}`.
* **Résultat attendu :** L'API doit recalculer le panier réel ou rejeter la valeur cliente non vérifiée.
* **Résultat obtenu :** **ANOMALIE (BUG-012)** : L'API valide aveuglément le sous-total fourni par le client.
* **Statut :** **FAIL**

---

## 5. Cas de Règles Métier (TC-BUS)

### TC-BUS-01 : Refus des produits issus de plusieurs restaurants dans un même panier
* **Objectif :** Vérifier qu'un panier ne peut contenir que les produits d'un seul restaurant.
* **Données :** 1 plat de Burger Factory + tentative d'ajout d'1 plat de Tokyo Bowl.
* **Résultat attendu :** Message d'avertissement et rejet de l'ajout du second restaurant.
* **Résultat obtenu :** Conforme. "Un panier ne peut contenir que des produits du même restaurant".
* **Statut :** **PASS**

### TC-BUS-02 : Commande dans un restaurant actuellement fermé
* **Objectif :** Tester le passage de commande auprès d'un établissement dont `is_open = False`.
* **Données :** Restaurant fermé.
* **Résultat attendu :** Impossible de commander, panier verrouillé ou message bloquant.
* **Résultat obtenu :** **ANOMALIE (BUG-002)** : La commande est validée sans vérifier si le restaurant est ouvert.
* **Statut :** **FAIL**

### TC-BUS-03 : Respect du montant minimum de commande du restaurant
* **Objectif :** Vérifier que la commande respecte le `minimum_order` imposé par le restaurant.
* **Données :** Restaurant avec minimum de 20.00 €, panier de 11.90 €.
* **Résultat attendu :** Checkout bloqué avec alerte invitant à compléter le panier.
* **Résultat obtenu :** **ANOMALIE (BUG-003)** : La commande est confirmée malgré le non-respect du minimum.
* **Statut :** **FAIL**

### TC-BUS-04 : Ajout au panier d'un produit en rupture de stock (stock = 0)
* **Objectif :** Vérifier qu'un produit dont le stock est épuisé ne peut être commandé.
* **Données :** Produit "Veggie Burger" (stock = 0).
* **Résultat attendu :** Bouton "Ajouter" désactivé ou message "Produit épuisé".
* **Résultat obtenu :** **ANOMALIE (BUG-004)** : Le produit peut être ajouté au panier et commandé.
* **Statut :** **FAIL**

### TC-BUS-05 : Conformité du taux de réduction du coupon ATLAS15
* **Objectif :** Vérifier que la promotion ATLAS annoncée à 15% applique bien 15%.
* **Données :** Code `ATLAS15`.
* **Résultat attendu :** Réduction de 15%.
* **Résultat obtenu :** **ANOMALIE (BUG-006)** : Seuls 10% sont appliqués en base de données.
* **Statut :** **FAIL**

### TC-BUS-06 : Filtrage des restaurants par frais de livraison économiques
* **Objectif :** Filtrer les restaurants ayant des frais de livraison <= 2.50 €.
* **Données :** Filtre "Frais <= 2.50 €".
* **Résultat attendu :** Seuls les restaurants à frais réduits s'affichent.
* **Résultat obtenu :** **ANOMALIE (BUG-007)** : Le filtre est inversé et affiche les restaurants à frais élevés.
* **Statut :** **FAIL**

### TC-BUS-07 : Dépôt d'un avis client sans avoir commandé
* **Objectif :** Vérifier qu'un client ne peut pas noter un restaurant sans commande confirmée.
* **Données :** Client nouvellement inscrit laissant un commentaire sur Tokyo Bowl.
* **Résultat attendu :** Message "Vous devez avoir commandé dans ce restaurant pour déposer un avis".
* **Résultat obtenu :** **ANOMALIE (BUG-009)** : L'avis est publié immédiatement sans aucun contrôle d'achat.
* **Statut :** **FAIL**
