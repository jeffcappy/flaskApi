from marshmallow import Schema, fields, pre_load, ValidationError, post_load

from userModels import User


# Processsors
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


# SCHEMAS
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
    def clean_input(self, in_data):
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
