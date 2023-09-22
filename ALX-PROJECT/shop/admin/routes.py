from flask import render_template, redirect, session, request, url_for, flash
from flask_login import logout_user, login_required
from shop import app, db, bcrypt
from .forms import RegisterationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
import os

# Admin dashboard route
@app.route('/admin')
def admin():
    # Check if 'email' is not in the session (user is not logged in)
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Fetch all products
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

# Brands management route
@app.route('/brands')
def brands():
    # Check if 'email' is not in the session (user is not logged in)
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Fetch all brands
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', brands=brands)

# Categories management route
@app.route('/category')
def category():
    # Check if 'email' is not in the session (user is not logged in)
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Fetch all categories
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', categories=categories)

# Admin registration route
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    form = RegisterationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Hash the user's password
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password
        )
        
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        
        flash(f'Welcome {form.name.data}, Thank you for registering.', 'success')
        return redirect(url_for('login'))
    
    return render_template('admin/register.html', form=form, title="Registration page")

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}, You are now logged In', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong password, please try again', 'danger')
    
    return render_template('admin/login.html', form=form, title="Login page")

# Admin logout route
@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash('Logged Out ', 'success')
    return redirect(url_for('admin_login'))
