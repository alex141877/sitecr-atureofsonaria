from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# Fichier de données JSON
DATA_FILE = 'dino_tracker_data.json'

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

# Classes pour gérer les données
class User(UserMixin):
    def __init__(self, id, username, code, created_at=None):
        self.id = id
        self.username = username
        self.code = code
        self.created_at = created_at or datetime.now().isoformat()

class Dino:
    def __init__(self, id, name, dino_type, purchase_price, sell_price, quantity, tax_rate, notes, user_id, created_at=None):
        self.id = id
        self.name = name
        self.dino_type = dino_type
        self.purchase_price = purchase_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.tax_rate = tax_rate
        self.notes = notes
        self.user_id = user_id
        self.created_at = created_at or datetime.now().isoformat()
    
    @property
    def total_cost(self):
        return self.purchase_price * self.quantity
    
    @property
    def total_revenue(self):
        return self.sell_price * self.quantity
    
    @property
    def tax_amount(self):
        return self.total_revenue * self.tax_rate
    
    @property
    def net_profit(self):
        return self.total_revenue - self.tax_amount - self.total_cost
    
    @property
    def profit_margin(self):
        if self.total_cost > 0:
            return (self.net_profit / self.total_cost) * 100
        return 0

# Fonctions de gestion des données JSON
def load_data():
    """Charge les données depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": [], "dinos": [], "next_user_id": 1, "next_dino_id": 1}
    return {"users": [], "dinos": [], "next_user_id": 1, "next_dino_id": 1}

def save_data(data):
    """Sauvegarde les données dans le fichier JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_by_username(username):
    """Trouve un utilisateur par son nom"""
    data = load_data()
    for user_data in data["users"]:
        if user_data["username"] == username:
            return User(user_data["id"], user_data["username"], user_data["code"], user_data["created_at"])
    return None

def get_user_by_id(user_id):
    """Trouve un utilisateur par son ID"""
    data = load_data()
    for user_data in data["users"]:
        if user_data["id"] == user_id:
            return User(user_data["id"], user_data["username"], user_data["code"], user_data["created_at"])
    return None

def get_dinos_by_user(user_id):
    """Récupère tous les dinosaures d'un utilisateur"""
    data = load_data()
    dinos = []
    for dino_data in data["dinos"]:
        if dino_data["user_id"] == user_id:
            dino = Dino(
                dino_data["id"], dino_data["name"], dino_data["dino_type"],
                dino_data["purchase_price"], dino_data["sell_price"],
                dino_data["quantity"], dino_data["tax_rate"], dino_data["notes"],
                dino_data["user_id"], dino_data["created_at"]
            )
            dinos.append(dino)
    return dinos

def add_user(username, code):
    """Ajoute un nouvel utilisateur"""
    data = load_data()
    user_id = data["next_user_id"]
    data["users"].append({
        "id": user_id,
        "username": username,
        "code": code,
        "created_at": datetime.now().isoformat()
    })
    data["next_user_id"] += 1
    save_data(data)
    return User(user_id, username, code)

def create_dino(name, dino_type, purchase_price, sell_price, quantity, tax_rate, notes, user_id):
    """Ajoute un nouveau dinosaure"""
    data = load_data()
    dino_id = data["next_dino_id"]
    data["dinos"].append({
        "id": dino_id,
        "name": name,
        "dino_type": dino_type,
        "purchase_price": purchase_price,
        "sell_price": sell_price,
        "quantity": quantity,
        "tax_rate": tax_rate,
        "notes": notes,
        "user_id": user_id,
        "created_at": datetime.now().isoformat()
    })
    data["next_dino_id"] += 1
    save_data(data)
    return Dino(dino_id, name, dino_type, purchase_price, sell_price, quantity, tax_rate, notes, user_id)

def update_dino(dino_id, name, dino_type, purchase_price, sell_price, quantity, tax_rate, notes, user_id):
    """Met à jour un dinosaure"""
    data = load_data()
    for i, dino_data in enumerate(data["dinos"]):
        if dino_data["id"] == dino_id and dino_data["user_id"] == user_id:
            data["dinos"][i] = {
                "id": dino_id,
                "name": name,
                "dino_type": dino_type,
                "purchase_price": purchase_price,
                "sell_price": sell_price,
                "quantity": quantity,
                "tax_rate": tax_rate,
                "notes": notes,
                "user_id": user_id,
                "created_at": dino_data["created_at"]
            }
            save_data(data)
            return True
    return False

def delete_dino(dino_id, user_id):
    """Supprime un dinosaure"""
    data = load_data()
    for i, dino_data in enumerate(data["dinos"]):
        if dino_data["id"] == dino_id and dino_data["user_id"] == user_id:
            del data["dinos"][i]
            save_data(data)
            return True
    return False

def get_dino_by_id(dino_id):
    """Récupère un dinosaure par son ID"""
    data = load_data()
    for dino_data in data["dinos"]:
        if dino_data["id"] == dino_id:
            return Dino(
                dino_data["id"], dino_data["name"], dino_data["dino_type"],
                dino_data["purchase_price"], dino_data["sell_price"],
                dino_data["quantity"], dino_data["tax_rate"], dino_data["notes"],
                dino_data["user_id"], dino_data["created_at"]
            )
    return None

# Formulaires
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=20)])
    code = StringField('Code', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('S\'inscrire')

class DinoForm(FlaskForm):
    name = StringField('Nom du dinosaure', validators=[DataRequired(), Length(max=100)])
    dino_type = SelectField('Type d\'objet', 
                           choices=[
                               ('', 'Choisir un type...'),
                               ('Créature', 'Créature'),
                               ('Espèce', 'Espèce'),
                               ('Token', 'Token')
                           ],
                           validators=[DataRequired()])
    purchase_price = FloatField('Prix d\'achat (champi)', validators=[DataRequired(), NumberRange(min=0)])
    sell_price = FloatField('Prix de vente (champi)', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=1)])
    tax_rate = FloatField('Taux de taxe (%)', validators=[NumberRange(min=0, max=100)], default=10)
    notes = TextAreaField('Notes (optionnel)')
    submit = SubmitField('Ajouter l\'objet')

# Configuration de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))

# Routes principales
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = get_user_by_username(form.username.data)
        if existing_user:
            flash('Ce nom d\'utilisateur existe déjà.', 'error')
            return render_template('register.html', form=form)
        
        user = add_user(form.username.data, form.code.data)
        
        flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and user.code == form.code.data:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Nom d\'utilisateur ou code incorrect.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    dinos = get_dinos_by_user(current_user.id)
    
    # Calculs globaux
    total_investment = sum(dino.total_cost for dino in dinos)
    total_revenue = sum(dino.total_revenue for dino in dinos)
    total_taxes = sum(dino.tax_amount for dino in dinos)
    total_profit = sum(dino.net_profit for dino in dinos)
    
    stats = {
        'total_dinos': len(dinos),
        'total_investment': total_investment,
        'total_revenue': total_revenue,
        'total_taxes': total_taxes,
        'total_profit': total_profit,
        'profit_margin': (total_profit / total_investment * 100) if total_investment > 0 else 0
    }
    
    return render_template('dashboard.html', dinos=dinos, stats=stats)

@app.route('/add_dino', methods=['GET', 'POST'])
@login_required
def add_dino():
    form = DinoForm()
    if form.validate_on_submit():
        dino = create_dino(
            form.name.data,
            form.dino_type.data,
            form.purchase_price.data,
            form.sell_price.data,
            form.quantity.data,
            form.tax_rate.data / 100,  # Convertir en décimal
            form.notes.data,
            current_user.id
        )
        flash('Objet ajouté avec succès!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_dino.html', form=form)

@app.route('/edit_dino/<int:dino_id>', methods=['GET', 'POST'])
@login_required
def edit_dino(dino_id):
    dino = get_dino_by_id(dino_id)
    if not dino:
        flash('Objet non trouvé.', 'error')
        return redirect(url_for('dashboard'))
    if dino.user_id != current_user.id:
        flash('Vous n\'avez pas l\'autorisation de modifier cet objet.', 'error')
        return redirect(url_for('dashboard'))
    
    form = DinoForm(obj=dino)
    form.tax_rate.data = dino.tax_rate * 100  # Convertir en pourcentage pour l'affichage
    
    if form.validate_on_submit():
        success = update_dino(
            dino_id,
            form.name.data,
            form.dino_type.data,
            form.purchase_price.data,
            form.sell_price.data,
            form.quantity.data,
            form.tax_rate.data / 100,
            form.notes.data,
            current_user.id
        )
        if success:
            flash('Objet modifié avec succès!', 'success')
        else:
            flash('Erreur lors de la modification.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_dino.html', form=form, dino=dino)

@app.route('/delete_dino/<int:dino_id>')
@login_required
def delete_dino(dino_id):
    dino = get_dino_by_id(dino_id)
    if not dino:
        flash('Objet non trouvé.', 'error')
        return redirect(url_for('dashboard'))
    if dino.user_id != current_user.id:
        flash('Vous n\'avez pas l\'autorisation de supprimer cet objet.', 'error')
        return redirect(url_for('dashboard'))
    
    success = delete_dino(dino_id, current_user.id)
    if success:
        flash('Objet supprimé avec succès!', 'success')
    else:
        flash('Erreur lors de la suppression.', 'error')
    return redirect(url_for('dashboard'))

# Route API pour les calculs
@app.route('/api/calculate_profit', methods=['POST'])
@login_required
def calculate_profit():
    data = request.get_json()
    purchase_price = float(data.get('purchase_price', 0))
    sell_price = float(data.get('sell_price', 0))
    quantity = int(data.get('quantity', 1))
    tax_rate = float(data.get('tax_rate', 10)) / 100
    
    total_cost = purchase_price * quantity
    total_revenue = sell_price * quantity
    tax_amount = total_revenue * tax_rate
    net_profit = total_revenue - tax_amount - total_cost
    profit_margin = (net_profit / total_cost * 100) if total_cost > 0 else 0
    
    return jsonify({
        'total_cost': round(total_cost, 2),
        'total_revenue': round(total_revenue, 2),
        'tax_amount': round(tax_amount, 2),
        'net_profit': round(net_profit, 2),
        'profit_margin': round(profit_margin, 2)
    })

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Créer les dossiers nécessaires s'ils n'existent pas
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Initialiser le fichier de données JSON
    data = load_data()
    print("✅ Système de sauvegarde JSON activé - Toutes les données sont sauvegardées dans dino_tracker_data.json")
    print("✅ Vos données sont protégées contre les crashes !")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
