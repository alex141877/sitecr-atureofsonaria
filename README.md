# 🦕 Dino Tracker - Version Déploiement

## 🚀 Prêt pour le déploiement sur Render

### 📁 Structure du projet
```
projet2/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── Procfile              # Configuration pour le déploiement
├── render.yaml           # Configuration Render
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Tableau de bord
│   ├── add_dino.html     # Ajout d'objet
│   ├── edit_dino.html    # Modification d'objet
│   ├── 404.html          # Page d'erreur 404
│   └── 500.html          # Page d'erreur 500
└── static/               # Fichiers statiques
    ├── css/
    │   └── style.css     # CSS personnalisé
    ├── js/
    │   └── main.js       # JavaScript principal
    └── images/           # Images
```

## 🌐 Déploiement sur Render

### Étape 1 : Créer un compte Render
1. Allez sur [render.com](https://render.com)
2. Créez un compte gratuit (pas de carte de crédit requise)

### Étape 2 : Connecter GitHub
1. Connectez votre compte GitHub
2. Sélectionnez ce repository

### Étape 3 : Créer un nouveau Web Service
1. "New" → "Web Service"
2. Connectez votre repository
3. Configurez :
   - **Name** : `dino-tracker`
   - **Runtime** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`

### Étape 4 : Variables d'environnement
Ajoutez ces variables :
- `FLASK_ENV` : `production`
- `SECRET_KEY` : (généré automatiquement)

### Étape 5 : Déployer
1. Cliquez "Create Web Service"
2. Render déploie automatiquement
3. Votre site sera disponible à : `https://dino-tracker.onrender.com`

## ✅ Fonctionnalités

- **Système de comptes** simplifié (nom + code)
- **Gestion des objets** (Créature, Espèce, Token)
- **Calcul automatique** des profits avec taxes
- **Sauvegarde JSON** persistante
- **Interface responsive** et moderne
- **HTTPS automatique** sur Render

## 💰 Coût

- **Gratuit** : 750 heures/mois
- **Pas de carte de crédit** requise
- **Redémarrage automatique** toutes les 15 minutes (plan gratuit)

## 🔄 Mises à jour

Chaque push sur GitHub déclenche un redéploiement automatique.

---

**🎉 Votre Dino Tracker est prêt pour le déploiement !**
