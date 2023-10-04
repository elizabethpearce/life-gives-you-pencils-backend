from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from database import create_app
from database import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import base64
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}}) #enables cross-origin resource sharing
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ALGORITHM"] = os.getenv("JWT_ALGORITHM")

jwt = JWTManager(app)

from database.models import ForSaleImages, Users

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = Users.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({"message": "Login successful!", "access token": access_token}), 200


@app.route('/insert', methods=['POST'])
def insert_image():
    if request.method == 'POST':

        if 'image' not in request.files or 'name' not in request.form or 'description' not in request.form:
            return jsonify({'message': 'Image, name, and description are required'}), 400
        
        image_data = request.files['image']
        image_name = request.form['name']
        description = request.form['description']

        if image_data.filename =='':
            return jsonify({'message': 'No selected file'}), 400
 
        new_image = ForSaleImages(img=image_data.read(), name=image_name, description=description)
        
        db.session.add(new_image)

        db.session.commit()

        return jsonify({'message': 'Image inserted successfully'}), 201
    
    
@app.route('/images', methods=['GET'])
def get_all_images():
    images = ForSaleImages.query.all()
    image_list = []
    for image in images:
        encoded_img = base64.b64encode(image.img).decode('utf-8')
        image_info = {
            'id': image.id,
            'img': encoded_img,
            'name': image.name,
            'description': image.description,
            'toolTip': image.toolTip,
            'insertTimeStamp': image.insertTimeStamp,
            'isActive': image.isActive,
        }
        image_list.append(image_info)
    return jsonify(image_list)
    
    
@app.route('/update/<int:image_id>', methods=['PUT'])
def update_image(image_id):
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        image = ForSaleImages.query.get(image_id)

        if image:
            image.name = name
            image.description = description

            db.session.commit()

            return jsonify({'message': 'Image updated successfully'}), 200
        else:
            return jsonify({'message': 'Image not found'}), 404

    
@app.route('/delete_selected', methods=['DELETE'])
def delete_selected_images():
    if request.method == 'DELETE':
        selected_image_ids = request.get_json().get('imageIds')

        if not selected_image_ids:
            return jsonify({'message': 'No images selected'}), 400

        # Loop through the list of selected image IDs and delete them from the database
        for image_id in selected_image_ids:
            image = ForSaleImages.query.get(image_id)
            if image:
                db.session.delete(image)
                db.session.commit()

        return jsonify({'message': 'Selected images deleted successfully'}), 200
        
    return jsonify({'message': 'Image not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)