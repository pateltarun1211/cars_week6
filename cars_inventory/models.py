from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import uuid 

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash

# Import for Secrets - created a user token
import secrets

# timestamp for user creation
from datetime import datetime

# flask login to check for an authenticated user
from flask_login import UserMixin, LoginManager

db = SQLAlchemy() # don't forget parantheses
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default ='')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)
    car = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash


    def __repr__(self):
        return f"User {self.email} has been added to the database!"
    
    
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(200))
    year = db.Column(db.Numeric(precision=4, scale=0))
    category = db.Column(db.String(150), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable = True)
    max_speed = db.Column(db.String(20), nullable = True)
    zero_sixty = db.Column(db.String(20), nullable = True)
    weight = db.Column(db.String(15), nullable = True)
    color = db.Column(db.String(20), nullable = True)
    fuel_type = db.Column(db.String(20), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, make, model, year, category, price, max_speed, zero_sixty, weight, color, fuel_type, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.category = category
        self.price = price
        self.max_speed = max_speed
        self.zero_sixty = zero_sixty
        self.weight = weight
        self.color = color
        self.fuel_type = fuel_type
        self.user_token = user_token
        
    def __repr__(self):
        return f"The following Car has been added: {self.name}"
    
    def set_id(self):
        return secrets.token_urlsafe()

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'category', 'price', 'max_speed', 'zero_sixty', 'weight', 'color', 'fuel_type']

car_schema = CarSchema()
cars_schema = CarSchema(many = True)