import os
import ssl
import smtplib
from flask import render_template, url_for, flash, redirect, request
from shop import app, db, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .models import Customer
from flask_login import login_user, current_user, logout_user, login_required
from email.message import EmailMessage

# Landing page route
@app.route('/', methods=['GET', 'POST'])
def landing_page():
    return render_template('customer/home.html')

# Account page route
@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('customer/account.html')

# About page route
@app.route('/about')
def about():
    return render_template('products/about.html')

# Registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, 
                        date_of_birth=form.date_of_birth.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now Log In', 'success')
        return redirect(url_for('login'))
    return render_template('customer/register.html', title='Registration Page', form=form)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome! {form.email.data} You are now logged In', 'success')
            return redirect(next_page) if next_page else redirect(url_for('landing_page'))
        else:
            flash('Login unsuccessful. Please check Email and Password', 'danger')
    return render_template('customer/login.html', title='Login Page', form=form)

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged Out', 'success')
    return redirect(url_for('landing_page'))

# Function to send a password reset email
def send_reset_email(user):
    token = user.get_reset_token()
    # Add your email here
    email_sender = "skycouture82@gmail.com"

    email_password = "gjokaecxaqcpfmes"#os.environ.get("EMAIL_PASSWORD")
    # Email of the person you're sending the report to
    email_receiver = user.email

    with open('token.txt', 'r') as fp:
        content = fp.read()

    subject = "Reset your password"
    body = content

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# Request password reset route
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('customer/reset_request.html', title='Reset Password Page', form=form)

# Password reset route with token
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Customer.verify_reset_token(token)
    if user is None:
        flash('Expired Token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now Log In', 'success')
        return redirect(url_for('login'))
    
    return render_template('customer/reset_token.html', title='Reset Password Page', form=form)
