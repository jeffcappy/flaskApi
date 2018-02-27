from marshmallow import fields

class Friend(fields.Field):
    def __init__(self,_id,name):
        self._id = _id
        self.name = name

class Name(fields.Field):
    def __init__(self,first,last):
        self.first = first
        self.last = last

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

    def __eq__(self,o):
        if self._id != o._id:
            print "id mismatch"
            return False
	if self.balance != o.balance:
            print "balance mismatch"
            return False
	if self.age != o.age:
            print "age mismatch"
            return False
	if self.name['last'] != o.name['last']:
            print "last name mismatch"
            return False
        if self.name['first'] != o.name['first']:
            print "first name mismatch"
            return False
	if self.phone != o.phone:
            print "phone mismatch"
            return False
	if self.address != o.address:
            print "address mismatch"
            return False
	##TODO add remaining fields
        return True
