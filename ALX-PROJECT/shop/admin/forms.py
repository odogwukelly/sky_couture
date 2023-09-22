from wtforms import Form, BooleanField, StringField, PasswordField, validators

# Registration form for user sign-up
class RegisterationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=30)])  # User's full name
    username = StringField('Username', [validators.Length(min=4, max=25)])  # Unique username for identification
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])  # User's email address
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Password must match')])  # User's chosen password
    confirm = PasswordField('Confirm Password')  # Confirm the password entered

# Login form for user authentication
class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])  # User's email address
    password = PasswordField('Password', [validators.DataRequired()])  # User's password for authentication
