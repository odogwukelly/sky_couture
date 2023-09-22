# Import necessary modules and classes
from flask import request, render_template, flash, redirect, url_for, session, current_app
from shop import db, app
from shop.products.models import Addproduct

# Define a function to merge two dictionaries (used for shopping cart)
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

# Route to add items to the shopping cart
@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        # Get product details from the form
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        # Check if all required data is available and the request method is POST
        if product_id and quantity and color and request.method == "POST":
            # Create a dictionary for the added item
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount,
                                      'color': color, 'quantity': quantity, 'image': product.image_1, 'colors': product.colors}}
            
            # Check if 'Shoppingcart' session variable exists
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                # If the product is already in the cart, increment its quantity
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    # Merge the current cart with the new item
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                # If the cart doesn't exist, create it with the new item
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

# Route to display the shopping cart
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    # Calculate subtotal, tax, and grand total for the cart
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        sum = ("%0.2f" % subtotal)
        tax = ("%0.2f" % (0.06 * float(subtotal)))
        grandtotal = float("%0.2f" % (1.06 * subtotal))
    
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, sum=sum)

# Route to update item details in the shopping cart
@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash(f'Item is updated!', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

# Route to delete an item from the shopping cart
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                flash('Item removed!', 'success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

# Route to clear the entire shopping cart
@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        flash(f'Your cart has been cleared!', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
