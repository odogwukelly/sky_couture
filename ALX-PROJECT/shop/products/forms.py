from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

# Form for adding products
class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])  # Product name field
    price = DecimalField('Price', [validators.DataRequired()])  # Product price field
    discount = IntegerField('Discount', default=0)  # Product discount field (default is 0)
    stock = IntegerField('Stock', [validators.DataRequired()])  # Product stock (quantity) field
    discription = TextAreaField('Description', [validators.DataRequired()])  # Product description field
    colors = TextAreaField('Colors', [validators.DataRequired()])  # Product colors field

    # Fields for product images
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please.')])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please.')])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only, please.')])
