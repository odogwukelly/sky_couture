# Import necessary modules and classes from Flask and other dependencies
from flask import request, render_template, flash, redirect, url_for, session, current_app
from shop import db, app, photos, search
from PIL import Image
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os

# Define a route for the homepage
@app.route('/all_product')
def home():     
    # Get the 'page' query parameter or default to 1
    page = request.args.get('page', 1, type=int)
    
    # Query for products with available stock and paginate the results
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    
    # Query for brands and categories associated with products
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    
    # Render the homepage template with the obtained data
    return render_template('products/index.html', products=products, brands=brands, categories=categories)

# Define a route for search results
@app.route('/result')
def result():
    # Get the search query parameter 'q'
    searchword = request.args.get('q')
    
    # Query for products matching the search query
    products = Addproduct.query.msearch(searchword, fields=['name', 'colors', 'price'], limit=8)
    
    # Render the search results template with the obtained products
    return render_template('products/result.html', products=products)

# Define a route for a single product page
@app.route('/product/<int:id>')
def single_page(id):
    # Query for a specific product by ID
    product = Addproduct.query.get_or_404(id)
    
    # Query for brands and categories associated with products
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    
    # Render the single product page with the obtained data
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)

# Define a route to filter products by brand
@app.route('/brand/<int:id>')
def get_brand(id):
    # Query for a specific brand by ID
    get_b = Brand.query.filter_by(id=id).first_or_404()
    
    # Get the 'page' query parameter or default to 1
    page = request.args.get('page', 1, type=int)
    
    # Query for products associated with the selected brand and paginate the results
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=4)
    
    # Query for brands and categories associated with products
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    
    # Render the filtered products template with the obtained data
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories, get_b=get_b)

# Define a route to filter products by category
@app.route('/categories/<int:id>')
def get_category(id):
    # Get the 'page' query parameter or default to 1
    page = request.args.get('page', 1, type=int)
    
    # Query for a specific category by ID
    get_cat = Category.query.filter_by(id=id).first_or_404()
    
    # Query for products associated with the selected category and paginate the results
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=4)
    
    # Query for brands and categories associated with products
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    
    # Render the filtered products template with the obtained data
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands, get_cat=get_cat)

# Define a route to add a new brand
@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    # Check if the user is logged in
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    if request.method=='POST':
        # Get the brand name from the form
        getbrand = request.form.get('brand')
        
        # Create a new brand instance and add it to the database
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        
        flash(f'The Brand {getbrand} was added to your database', 'success')
        return redirect(url_for('addbrand'))
    
    return  render_template('products/addbrand.html', brands='brands')

# Define a route to update an existing brand
@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    # Check if the user is logged in
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    
    # Query for the brand to be updated
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    
    if request.method == 'POST':
        # Update the brand name
        updatebrand.name = brand
        db.session.commit()
        flash(f'Your brand has been updated', 'success')
        return redirect(url_for('brands'))
    
    return render_template('products/updatebrand.html', title='Update brand page', updatebrand=updatebrand)

# Define a route to delete a brand
@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f"The brand {brand.name} can't be deleted", 'warning')
    return redirect(url_for('admin'))

# Define a route to add a new category
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    # Check if the user is logged in
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    if request.method=='POST':
        # Get the category name from the form
        getbrand = request.form.get('category')
        
        # Create a new category instance and add it to the database
        cat = Category(name=getbrand)
        db.session.add(cat)
        db.session.commit()
        
        flash(f'The Category {getbrand} was added to your database', 'success')
        return redirect(url_for('addcat'))
    
    return render_template('products/addbrand.html')

# Define a route to update an existing category
@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    # Check if the user is logged in
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    
    # Query for the category to be updated
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    
    if request.method == 'POST':
        # Update the category name
        updatecat.name = category
        db.session.commit()
        flash(f'Your category has been updated', 'success')
        return redirect(url_for('category'))
    
    return render_template('products/updatebrand.html', title='Update category page', updatecat=updatecat)

# Define a route to delete a category
@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f"The category {category.name} can't be deleted", 'warning')
    return redirect(url_for('admin'))

# Define a route to add a new product
@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    # Check if the user is logged in
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    # Query all brands and categories for form choices
    brands = Brand.query.all()
    categories = Category.query.all()
    
    # Create a form for adding products
    form = Addproducts(request.form)
    
    if request.method == 'POST':
        # Get product information from the form
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        
        # Check if the selected brand is valid
        if not brand.isdigit() or not Brand.query.get(brand):
            flash(f'Invalid brand selected', 'danger')
            return redirect(url_for('addproduct'))
        
        # Define a function to resize images
        def resize_image(img, max_size):
            img = Image.open(img)
            img.thumbnail((max_size, max_size))
            return img
        
        # Check and resize images if needed
        max_image_size = 800  # Set your desired maximum image size
        image_1_tmp = request.files.get('image_1')
        image_2_tmp = request.files.get('image_2')
        image_3_tmp = request.files.get('image_3')
        
        if image_1_tmp and image_1_tmp.content_length > max_image_size:
            image_1_tmp = resize_image(image_1_tmp, max_image_size)
        if image_2_tmp and image_2_tmp.content_length > max_image_size:
            image_2_tmp = resize_image(image_2_tmp, max_image_size)
        if image_3_tmp and image_3_tmp.content_length > max_image_size:
            image_3_tmp = resize_image(image_3_tmp, max_image_size)
        
        # Save the resized or original images with unique names
        image_1 = photos.save(image_1_tmp, name=secrets.token_hex(10) + ".")
        image_2 = photos.save(image_2_tmp, name=secrets.token_hex(10) + ".")
        image_3 = photos.save(image_3_tmp, name=secrets.token_hex(10) + ".")
        
        # Create a new product instance and add it to the database
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, 
                            brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        
        flash(f'The product {name} has been added to your database', 'success')
        return redirect(url_for('admin'))
    
    return render_template('products/addproduct.html', form=form, brands=brands, categories=categories, title='Add product page')

# Define a route to update an existing product
@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    # Query all brands and categories for form choices
    brands = Brand.query.all()
    categories = Category.query.all()
    
    # Query for the product to be updated
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    
    # Create a form for updating products
    form = Addproducts(request.form)
    
    if request.method == 'POST':
        # Update product information from the form
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.desc = form.discription.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.brand_id = brand
        product.category_id = category
        
        # Check if new images are provided and update them
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin'))

    # Populate the form fields with existing product data
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.discription.data = product.desc
    form.stock.data = product.stock
    form.colors.data = product.colors

    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

# Define a route to delete a product
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('image_1_tmp'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted from your record', 'success')
        return redirect(url_for('admin'))
    flash(f'Cannot delete this product', 'danger')
    return redirect(url_for('admin'))
