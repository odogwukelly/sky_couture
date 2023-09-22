# Import necessary modules and classes
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Customer  # Assuming the Customer model is in the same directory

# Define the registration form for user sign-up
class RegistrationForm(FlaskForm):
    # Define form fields and associated validators
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date Of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    submit = SubmitField('Sign Up')
    
    # Custom validation for username uniqueness
    def validate_username(self, username):
        # Check if the username is already in use
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already in use!")
        
    # Custom validation for email uniqueness
    def validate_email(self, email):
        # Check if the email is already in use
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already in use!")

# Define the login form for user authentication
class LoginForm(FlaskForm):
    # Define form fields for email and password
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
# Define the form for requesting a password reset
class RequestResetForm(FlaskForm):
    # Define form field for email
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # Custom validation to check if the email corresponds to an existing account
    def validate_email(self, email):
        # Check if there is an account with the provided email
        user = Customer.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email')
        
# Define the form for resetting the password
class ResetPasswordForm(FlaskForm):
    # Define form fields for password and password confirmation
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
