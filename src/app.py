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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    

    return jsonify(response_body), 200

#Add member to the family

@app.route('/member', methods=['POST'])
def handle_new_member():
    new_member = request.json
    return jsonify(jackson_family.add_member(new_member)), 200

#Get an speciffic member of the family

@app.route('/member/<int:id>', methods=['GET'])
def handle_single_member(id):
    member = jackson_family.get_member(id)
    if member is not None:
        return jsonify(jackson_family.get_member(id)), 200
    return jsonify({"message": "Member not found"}), 404

#Delete an speciffic member of the family

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    member = jackson_family.delete_member(id)
    if member is True:
        return jsonify({"done": member}), 200
    return jsonify({"message": "Member not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
