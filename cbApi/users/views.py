from flask import Blueprint, request
from flask_jsonpify import jsonify
from marshmallow import ValidationError

from cbApi import db
from userSchemas import UserSchema
from sparkHelper import UserTools

users_blueprint = Blueprint('users', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
sparkTools = UserTools()
'''
@users_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    print error
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response
'''


@users_blueprint.before_request
def set_db_defaults():
    if 'users' not in db:
        db['users'] = dict()


@users_blueprint.route('/api/user/add', methods=["POST"])
def addUser():
    # print request
    json_data = request.get_json()
    # print json_data
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    try:
        u = user_schema.load(json_data)
        print "User Schema load return type"
        print type(u)
        print u
        db['users'][u._id] = u
        # u.save()
        return jsonify(user_schema.dump(u)), 200
    except ValidationError as err:
        print err
        print err.valid_data
        return jsonify(err.messages), 422
        # raise InvalidUsage(str(err.messages["_schema"]),400)


@users_blueprint.route('/api/users/add', methods=['POST'])
def addUsers():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        u = users_schema.load(json_data)
        print u
        for user in u:
            # print type(user)
            # user.save()
            db['users'][user._id] = user
        return jsonify(users_schema.dump(u))
    except ValidationError as err:
        print err
        print err.valid_data
        return jsonify(err.messages), 422


@users_blueprint.route('/api/user/<int:_id>', methods=["GET"])
def getUser(_id):
    if _id in db['users']:
        # u = user_schema.dump(db['users'][_id])
        u = db['users'][_id]
        return jsonify(user_schema.dump(u)), 200
    else:
        return None, 404

@users_blueprint.route('/api/user/dataframe', methods=["POST"])
def dataframeFun():
    json_data = request.get_json()
    print type(json_data)
    spark_data = sparkTools.dataFrameFromListOfDicts(json_data)
    return jsonify(spark_data)


@users_blueprint.route('/api/users', methods=["GET"])
def getUsers():
    # users = users_schema.dump(User.select())
    users = db['users'].values()
    return jsonify(users_schema.dump(users))

"""
@users_blueprint.route('/api/help')
def siteMap():
    links = list()
    for rule in users_blueprint.url_map.iter_rules():
        print rule
        links.append((str(rule), str(rule.methods)))
    return jsonify(links)
"""