from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
from flask import session


app = Flask(__name__)
app.secret_key = 'voiturecestbien'


# Configuration de la base de données
DATABASE = {
    'dbname': 'concession_client',
    'user': 'postgres',
    'password': '20030701Ae.',
    'host': 'localhost'
}

def authenticate_user(username, password):
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE username = %s AND mot_de_passe = %s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, email, password):
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utilisateurs (username, email, mot_de_passe) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate_user(username, password)
        if user:
            # Utilisateur authentifié, rediriger vers la page d'estimation
            return redirect(url_for('estimate'))
        else:
            return jsonify({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Traitement de l'inscription
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username and email and password:
            add_user(username, email, password)
            return redirect(url_for('login'))
        else:
            return jsonify({'error': 'Les champs username, email et password sont requis'}), 400
    else:
        # Rendre le formulaire d'inscription
        return render_template('register.html')

@app.route('/estimate', methods=['GET', 'POST'])
def estimate():
    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        location = request.form['location']
        year = request.form['year']
        kilometers_driven = request.form['kilometers_driven']
        fuel_type = request.form['fuel_type']
        transmission = request.form['transmission']
        owner_type = request.form['owner_type']
        mileage = request.form['mileage']
        seats = request.form['seats']
        brand = request.form['brand']
        model = request.form['model']
        engine_numeric = request.form['engine_numeric']
        power_numeric = request.form['power_numeric']
        is_sold_new = request.form['is_sold_new']

        # Effectuer l'estimation (vous devrez écrire cette logique)
        estimated_price = perform_estimation(location, year, kilometers_driven, fuel_type, transmission, owner_type, mileage, seats, brand, model, engine_numeric, power_numeric, is_sold_new)

        # Rendre un template avec le résultat de l'estimation
        return render_template('estimate_result', estimated_price=estimated_price)

    # Si la méthode est GET, afficher simplement le formulaire
    return render_template('estimate.html')

# Fonction pour effectuer l'estimation (à compléter selon vos besoins)
def perform_estimation(location, year, kilometers_driven, fuel_type, transmission, owner_type, mileage, seats, brand, model, engine_numeric, power_numeric, is_sold_new):
    # Ici, vous pouvez implémenter la logique pour effectuer l'estimation
    # Par exemple, vous pouvez utiliser un modèle de machine learning pour prédire le prix

    # Pour cet exemple, retournons simplement une valeur fixe
    return 10000

@app.route('/logout')
def logout():
    # Effacez les informations de session de l'utilisateur
    session.pop('username', None)
    # Redirigez l'utilisateur vers la page de connexion
    return redirect(url_for('login'))

def get_car_data():
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT brand, model, price_in_euro, kilometers_driven, location, year, fuel_type, owner_type, power_numeric, engine_numeric, seats, mileage, is_sold_new FROM vehicules")
    cars = cursor.fetchall()
    conn.close()
    return cars

@app.route('/dashboard')
def dashboard():
    cars = get_car_data()
    return render_template('dashboard.html', cars=cars)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT brand, model, price_in_euro, kilometers_driven, location, year, fuel_type, owner_type, power_numeric, engine_numeric, seats, mileage, is_sold_new FROM vehicules WHERE brand ILIKE %s OR model ILIKE %s", ('%' + search_query + '%', '%' + search_query + '%'))
    search_results = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', cars=search_results)

if __name__ == '__main__':
    app.run(debug=True)
