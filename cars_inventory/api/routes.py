from flask import Blueprint, request, jsonify
from cars_inventory.helpers import token_required
from cars_inventory.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api') 

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value' }

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    category = request.json['category']
    price = request.json['price']
    max_speed = request.json['max_speed']
    zero_sixty = request.json['zero_sixty']
    weight = request.json['weight']
    color = request.json['color']
    fuel_type = request.json['fuel_type']
    user_token = current_user_token.token
    
    print(f"User Token: {current_user_token.token}")
    
    car = Car(make, model, year, category, price, max_speed, zero_sixty, weight, color, fuel_type, user_token=user_token)
    
    db.session.add(car)
    db.session.commit()
    
    response = car_schema.dump(car)
    
    return jsonify(response)

#retrieve ALL Cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)



# Retrieve One Car Endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'mesasge': 'Valid Token Required'}), 401
    
    
# Update Car endpoint
@api.route('cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.category = request.json['category']
    car.price = request.json['price']
    car.max_speed = request.json['max_speed']
    car.zero_sixty = request.json['zero_sixty']
    car.weight = request.json['weight']
    car.color = request.json['color']
    car.fuel_type = request.json['fuel_type']
    car.user_token = current_user_token.token
    
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)