from shop import db  # Import the database instance (Assuming 'shop' is your Flask application)

# User model representing user data in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # User ID (Primary Key)
    name = db.Column(db.String(30), unique=False, nullable=False)  # User's full name
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username for identification
    email = db.Column(db.String(180), unique=True, nullable=False)  # Unique email address for login
    password = db.Column(db.String(180), unique=False, nullable=False)  # Hashed password for security
    profile = db.Column(db.String(180), unique=False, nullable=False, default='profile.jpg')  # Profile picture filename

    # Method to represent a User object when printing
    def __repr__(self):
        return '<User %r>' % self.username
