"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)



# create the jackson family object
jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    try:
        members = jackson_family.get_all_members()

        if members == []:
            return jsonify({'error': 'No hay miembros', 'code_status': 404}), 404

        return jsonify(members), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({'error': 'Miembro no encontrado'}), 404
        return jsonify(member), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    if request.content_type != 'application/json':
        return jsonify({'error': 'content-type tiene que ser application/json'}), 400

    try:
        member = request.get_json()
        mandatorys = ['first_name', 'age', 'lucky_numbers']
        for require in mandatorys:
            if require not in member:
                return jsonify({'error': f'Falta este dato: {require}'}), 400
        
        if not isinstance(member['age'], int) or member['age'] <= 0:
            return jsonify({'error': 'Edad tiene que ser mayor a 0'}), 400
            

        jackson_family.add_member(member)
        return jsonify(member), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    try:
        jackson_family.delete_member(member_id)
        return jsonify({'done': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)