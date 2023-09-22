from shop import db
from datetime import datetime

# Class representing a product in the online store
class Addproduct(db.Model):
    # Fields to be indexed for full-text search
    __searchable__ = ['name', 'colors', 'price']

    # Columns in the 'Addproduct' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # Name of the product (up to 80 characters)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price of the product
    discount = db.Column(db.Integer, default=0)  # Discount for the product (default is 0)
    stock = db.Column(db.Integer, nullable=False)  # Quantity in stock
    colors = db.Column(db.String(100), nullable=False)  # Description of product colors
    desc = db.Column(db.Text, nullable=False)  # Description of the product
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Publication date and time

    # Foreign key to link with the 'Brand' table
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))  # Relationship with the 'Brand' table

    # Foreign key to link with the 'Category' table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('post', lazy=True))  # Relationship with the 'Category' table

    # File paths to product images
    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name

# Class representing a brand
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)  # Name of the brand

    def __repr__(self):
        return '<Brand %r>' % self.name

# Class representing a category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)  # Name of the category

    def __repr__(self):
        return '<Category %r>' % self.name
