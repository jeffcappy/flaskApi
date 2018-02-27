#!/Users/jeffreycapobianco/anaconda2/bin/python

from flask import Flask, request, url_for
from flask_jsonpify import jsonify
#from datetime import date
from marshmallow import Schema, fields, pprint,pre_load,ValidationError,post_load

app = Flask(__name__)
app.url_map.strict_slashes = False

allUsers = dict()

#Processsors
def cleanInt(string):
    string = str(string)
    clean = ''
    for digit in string:
        if digit.isdigit():
            clean = clean + digit
    return clean

def parsePhone(phone):
    clean = cleanInt(phone)
    if len(clean) == 11 and clean[0] is "1":
        clean = clean[1:]
    if len(clean) != 10:
        raise ValidationError('Phone number must be 10 digits including area code')
    return int(clean)

def parseBalance(balance):
    return cleanInt(balance)

#MODELS
class User(object):
    def __init__(self,_id,balance,picture,age,name,phone,address,tags,_range,friends):
        self._id = _id
        self.balance = balance
        self.picture = picture
        self.age = age
        self.name = name
        self.phone = phone
        self.address = address
        self.tags = tags
        self._range = _range
        self.friends = friends
         
class Friend(fields.Field):
    def __init__(self,_id,name):
        self._id = _id
        self.name = name

class Name(fields.Field):
    def __init__(self,first,last):
        self.first = first
        self.last = last

#SCHEMAS
class FriendSchema(Schema):
    _id = fields.Integer()
    name = fields.Str()

class NameSchema(Schema):
    first = fields.Str()
    last = fields.Str()

class UserSchema(Schema):
    _id = fields.Integer()
    balance = fields.Integer()
    picture = fields.Str()
    age = fields.Integer()
    name = fields.Nested(NameSchema)
    phone = fields.Integer()
    address = fields.Str()
    tags = fields.List(fields.Str())
    _range = fields.List(fields.Integer())
    friends = fields.List(fields.Nested(FriendSchema))

    @pre_load
    def clean_input(self,in_data):
        try:
            in_data['phone'] = parsePhone(in_data['phone'])
        except ValidationError as err:
            raise err 
        try:
            in_data['balance'] = parseBalance(in_data['balance'])
        except ValidationError as err:
            raise err
        return in_data

    @post_load
    def make_user(self, data):
        out = User(**data)
        return out

user_schema=UserSchema()
users_schema=UserSchema(many=True)

'''
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    print error
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response
'''


@app.route('/api/user/add', methods=["POST"])
def addUser():
    #    def __init__(self,_id,balance,picture,age,name,phone,address,tags,_range,friends):
    json_data = request.get_json()
    #print json_data
    if not json_data:
    	return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    try:
       	u = user_schema.load(json_data)
        print u
        allUsers[u._id] = u
        return jsonify(user_schema.dump(u)),200
    except ValidationError as err:
       	print err
       	print err.valid_data
       	return jsonify(err.messages), 422
        #raise InvalidUsage(str(err.messages["_schema"]),400)

@app.route('/api/users/add',methods=['POST'])
def addUsers():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        u = users_schema.load(json_data)
        print u
        for user in u:
            allUsers[user._id] = user
        return jsonify(users_schema.dump(u))
    except ValidationError as err:
        print err
        print err.valid_data
        return jsonify(err.messages), 422

    

@app.route('/api/user/<int:_id>', methods=["GET"])
def getUser(_id):
    if _id in allUsers:
        u = user_schema.dump(allUsers[_id])
        return jsonify(u),200
    else:
        return None,404
    
@app.route('/api/users',methods=["GET"])
def getUsers():
    users = users_schema.dump(allUsers.values())
    return jsonify(users)
    
@app.route('/api/help')
def siteMap():
    links = list()
    for rule in app.url_map.iter_rules():
        print rule
        links.append((str(rule),str(rule.methods)))
    return jsonify(links)


if __name__ == '__main__':
   app.run(port='5002')
   #app.run(debug=True)  
