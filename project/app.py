from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# API Keys and URLs for flood prediction
ELEVATION_API_URL = "https://api.open-elevation.com/api/v1/lookup"
WEATHER_API_KEY = "your_openweathermap_api_key"  # Replace with your API key

# Home route (Login required)
@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html')  # Show flood prediction page if logged in
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')
        else:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Flood prediction route (called from the homepage)
@app.route('/flood_prediction', methods=['POST'])
def flood_prediction():
    if 'user' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in
    
    city = request.form['city']
    results = {}

    # Step 1: Get latitude and longitude of the city
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if not geocode_data:
        results['error'] = f"City '{city}' not found."
        return jsonify(results)

    lat, lon = geocode_data[0]['lat'], geocode_data[0]['lon']

    # Step 2: Get elevation data
    elevation_response = requests.get(f"{ELEVATION_API_URL}?locations={lat},{lon}")
    elevation_data = elevation_response.json()
    city_elevation = elevation_data['results'][0]['elevation']

    # Step 3: Fetch weather data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    description = weather_data['weather'][0]['description']

    # Step 4: Predict flood risk based on elevation
    flood_risk = "Low"
    if city_elevation < 50:
        flood_risk = "High"
    elif city_elevation < 100:
        flood_risk = "Moderate"

    # Step 5: Return the results
    results['city'] = city
    results['elevation'] = city_elevation
    results['weather'] = description
    results['flood_risk'] = flood_risk
    results['lat'] = lat
    results['lon'] = lon

    return jsonify(results)  # Returning data as JSON to be used on the frontend

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
