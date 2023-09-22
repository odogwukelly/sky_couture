from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as TimedSerializer
from shop import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(int(user_id))

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6))

    def get_reset_token(self, expires_in=3600):
        # Generate a time-limited reset token
        s = TimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps({'user_id': self.id})
        
        # Store the token in a file (you may want to change this to use a database)
        with open('token.txt', 'w') as token_file:
            token_file.write(token)
        
        return token

    @staticmethod
    def verify_reset_token(token):
        # Verify and extract data from the reset token
        s = TimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=3600)  # Set max_age as needed
            user_id = data['user_id']
            return Customer.query.get(user_id)
        except:
            return None
        
    def __repr__(self):
        return f"Customer('{self.username}', '{self.email}', '{self.image_file}', '{self.date_of_birth}', '{self.gender}', '{self.date_created}')"
