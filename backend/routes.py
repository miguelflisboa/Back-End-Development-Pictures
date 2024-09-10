from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return data"""
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return data by id"""
    for person in data:
        if person["id"] == id:
            return jsonify(person), 200
        
    return {"message": "Person not found!"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()

    # Verify if the ID already exists
    for person in data:
        if str(person["id"]) == str(picture["id"]):
            return {"message": f"Picture with id {picture['id']} already present"}, 302

    try:
        data.append(picture)
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}, 500

    return jsonify({"message": f"Picture with id {picture['id']} created successfully", "id": picture['id']}), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.get_json()
    
    # Find the picture by ID
    for picture in data:
        if picture["id"] == id:
            # Update the picture with the incoming data
            picture.update(picture_data)
            return jsonify({"message": f"Picture with id {id} updated successfully"}), 200
    
    # If picture is not found
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture by ID
    for index, picture in enumerate(data):
        if picture["id"] == id:
            # Delete the picture
            del data[index]
            return '', 204
    
    # If picture is not found
    return jsonify({"message": "Picture not found"}), 404
