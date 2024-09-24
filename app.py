
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash('A confirmation email has been sent to your email address.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

def send_confirmation_email(user):
    token = 'dummy_token'  # Generate a real token in a real application
    msg = Message('Confirm Your Email', sender='your_email@gmail.com', recipients=[user.email])
    msg.body = f'Please click the link to confirm your email: {url_for("confirm_email", token=token, _external=True)}'
    mail.send(msg)

@app.route('/confirm/<token>')
def confirm_email(token):
    # Confirm the user's email in a real application
    flash('Your email has been confirmed!', 'success')
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return 'Login Page'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
