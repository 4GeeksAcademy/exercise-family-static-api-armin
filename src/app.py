"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200



# 2) Recupera solo un miembro
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": "Member not found"}), 404
    return jsonify(member), 200



# 3) Añadir (POST) un miembro
@app.route('/members', methods=['POST'])
def add_member():
    # Verificar si la solicitud tiene datos JSON
    if not request.json:
        return jsonify({"message": "Missing JSON in request"}), 400
    
    # Obtener los datos del miembro del cuerpo de la solicitud
    member_data = request.json
    
    # Validar que los datos requeridos estén presentes
    required_fields = ['first_name', 'age', 'lucky_numbers']
    for field in required_fields:
        if field not in member_data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    # Añadir el miembro a la familia
    jackson_family.add_member(member_data)
    
    # No necesitamos devolver el miembro, solo un código de éxito
    return jsonify({}), 200



# 4) ELIMINA un miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # Intentar eliminar el miembro
    success = jackson_family.delete_member(member_id)
    
    if not success:
        return jsonify({"message": "Member not found"}), 404
    
    return jsonify({"done": True}), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
