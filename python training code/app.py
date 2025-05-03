from flask import Flask, request, render_template, redirect, url_for, session, flash
import pickle
import pandas as pd
import mysql.connector
import hashlib
import logging
import stripe

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
stripe.api_key = 'your_stripe_secret_key'  # Replace with your Stripe secret key

# Database configuration
def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="home")

# Load the pre-trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Home Route
@app.route('/')
def home():
    return render_template('index.html')  # Render the home page

# Payment Routes
@app.route('/payment')
def payment_page():
    return render_template('payment.html')  # Render the payment form page

@app.route('/charge', methods=['POST'])
def charge():
    amount = request.form['amount']  # Amount to be charged
    try:
        # Create a charge
        charge = stripe.Charge.create(
            amount=int(amount) * 100,  # Amount in cents
            currency='usd',
            source=request.form['stripeToken'],
            description='Payment for Home Purchase'
        )
        flash('Payment successful! Thank you for your purchase.', 'success')
        # You can store charge information in the database here
        store_payment_in_db(charge)
    except stripe.error.StripeError as e:
        flash(f'Payment failed: {str(e)}', 'danger')
        return redirect(url_for('payment_page'))
    return redirect(url_for('confirmation'))

def store_payment_in_db(charge):
    db = get_db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO payments (`amount`, `currency`, `description`, `payment_id`) VALUES (%s, %s, %s, %s)"
    val = (charge['amount'], charge['currency'], charge['description'], charge['id'])
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')  # Render the confirmation page

# Add other routes (e.g., prediction, buyer/seller registration, etc.)

# Prediction Routes
@app.route('/predict')
def predict_page():
    return render_template('predict.html')  # Render the prediction form page

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    # Get the input data from the form
    bhk = int(request.form['BHK'])
    build_area = int(request.form['Build_Area'])
    total_floors = int(request.form['Total_Floors'])
    parking = request.form['Parking']
    furnishing = request.form['Furnishing']
    location = request.form['Location']
    
    # Prepare input data for the model
    input_data = pd.DataFrame({
        'BHK': [bhk],
        'Build_Area': [build_area],
        'Total_Floors': [total_floors],
        'Parking': [parking],
        'Furnishing': [furnishing],
        'Location': [location]
    })

    # One-hot encode the input data
    input_data_encoded = pd.get_dummies(input_data)
    input_data_encoded = input_data_encoded.reindex(columns=model.feature_names_in_, fill_value=0)

    # Make prediction
    prediction = model.predict(input_data_encoded)
    
    # Return the prediction result to the prediction page
    return render_template('predict.html', prediction=prediction[0], bhk=bhk, build_area=build_area,
                           total_floors=total_floors, parking=parking, furnishing=furnishing, location=location)

# Buyer and Seller Routes
@app.route('/buyer')
def buyer():
    return render_template('buyer.html')

@app.route('/seller')
def seller():
    return render_template('seller.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# Registration Routes
@app.route('/buy_reg')
def buy_reg():
    return render_template('buyer_reg.html')

@app.route('/sell_reg')
def sell_reg():
    return render_template('seller_reg.html')

# Buyer Registration
@app.route('/buyerreg', methods=['POST'])
def buyerreg():
    if request.method == 'POST':
        name = request.form.get('username')
        gender = request.form.get('gender')
        mail = request.form.get('mail')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        
        sql = "INSERT INTO buyer (`name`, `gender`, `mail`, `phone`, `password`, `acc`) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, gender, mail, phone, hashed_password, 'no')

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, val)
            db.commit()
        except mysql.connector.Error as e:
            return render_template('buyer.html', msg=f'Database error: {str(e)}')
        finally:
            cursor.close()
            db.close()

        return render_template('buyer.html')

# Seller Registration
@app.route('/sellerreg', methods=['POST'])
def sellerreg():
    if request.method == 'POST':
        name = request.form.get('username')
        gender = request.form.get('gender')
        mail = request.form.get('mail')
        phone = request.form.get('phone')
        password = request.form.get('password')
        accno = request.form.get('accno')
        bran = request.form.get('bran')

        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        
        sql = "INSERT INTO seller (`name`, `gender`, `mail`, `phone`, `password`, `accno`, `branch`, `bal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, gender, mail, phone, hashed_password, accno, bran, '0')

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, val)
            db.commit()
        except mysql.connector.Error as e:
            return render_template('seller.html', msg=f'Database error: {str(e)}')
        finally:
            cursor.close()
            db.close()

        return render_template('seller.html')

# Buyer Login Validation
@app.route('/buyerval', methods=['POST'])
def buyerval():
    global uname
    if request.method == 'POST':
        uname = request.form.get('username')
        upass = request.form.get('password')
        hashed_password = hashlib.sha256(upass.encode()).hexdigest()  # Hash the password

        sql = 'SELECT * FROM `buyer` WHERE `name` = %s AND `password` = %s'
        val = (uname, hashed_password)

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, val)
            result = cursor.fetchone()
            if result:
                return redirect(url_for('buy_dash'))
            else:
                return render_template('buyer.html', msg='Invalid Data')
        except mysql.connector.Error as e:
            return render_template('buyer.html', msg=f'Database error: {str(e)}')
        finally:
            cursor.close()
            db.close()

# Seller Login Validation
@app.route('/sellerval', methods=['POST'])
def sellerval():
    global uname
    if request.method == 'POST':
        uname = request.form.get('username')
        upass = request.form.get('password')
        hashed_password = hashlib.sha256(upass.encode()).hexdigest()  # Hash the password

        sql = 'SELECT * FROM `seller` WHERE `name` = %s AND `password` = %s'
        val = (uname, hashed_password)

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, val)
            result = cursor.fetchone()
            if result:
                return redirect(url_for('sell_dash'))
            else:
                return render_template('seller.html', msg='Invalid Data')
        except mysql.connector.Error as e:
            return render_template('seller.html', msg=f'Database error: {str(e)}')
        finally:
            cursor.close()
            db.close()

# Admin Login Validation
@app.route('/adminval', methods=['POST'])
def adminval():
    if request.method == 'POST':
        uname = request.form.get('username')
        upass = request.form.get('password')
        if uname == 'admin' and upass == '1234':
            return redirect(url_for('admin_dash'))
        else:
            return render_template('admin.html', msg='Invalid Data')

# Buyer Dashboard
@app.route('/buy_dash')
def buy_dash():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        sql = 'SELECT * FROM `buyer` WHERE `name` = %s'
        val = (uname,)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        return render_template('buy_dashboard.html', data=data)
    except mysql.connector.Error as e:
        return render_template('buy_dashboard.html', error=str(e), data=[])
    finally:
        cursor.close()
        db.close()

# Seller Dashboard
@app.route('/sell_dash')
def sell_dash():
    try:
        db = get_db_connection()
        cursor = db.cursor()

        sql = 'SELECT * FROM `seller` WHERE `name` = %s'
        val = (uname,)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        return render_template('sell_dashboard.html', data=data)
    except mysql.connector.Error as e:
        return render_template('sell_dashboard.html', error=str(e), data=[])
    finally:
        cursor.close()
        db.close()

# Admin Dashboard
@app.route('/admin_dash')
def admin_dash():
    return render_template('admin_dashboard.html')
@app.route('/about')
def about():
    return render_template('about.html')
# Log out and redirect to home
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('home'))

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
