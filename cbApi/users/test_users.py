import unittest
from cbApi import app
from cbApi import db
from userStubs import stubbedUser
from userSchemas import UserSchema
from userModels import *


class ProjectTests(unittest.TestCase):
 
    #### setup and teardown ####
    #for peewee 
    #def createTables(self):
    #    db.create_tables([User,Friend,Name,Tag,Range])
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEquals(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
    #### tests ####
    def testAddGetUsers(self):
        stub = stubbedUser()
        jsonStr = stub.userList()
        #print jsonStr
        response = self.addUsers(jsonStr)
        #print type(response)
        self.assertEqual(response.status_code,200)
        schema = UserSchema(many=True)
        userIn = schema.loads(jsonStr)
        userOut = schema.loads(response.data)
        self.assertTrue(userIn.__eq__(userOut))
        self.assertTrue(userIn.__eq__(self.getUsers()))    
 
    def testAddGetUser(self):
        #print type(app)
        stub = stubbedUser()
        jsonStr = stub.singleUser()
        #print jsonStr
        response = self.addUser(jsonStr)
        #print type(response)
        self.assertEqual(response.status_code,200)
        schema = UserSchema()
        userIn = schema.loads(jsonStr)
        userOut = schema.loads(response.data)
        self.assertTrue(userIn.__eq__(userOut))
        retrievedUser = schema.loads(self.getUser('1').data)
        self.assertTrue(userIn.__eq__(retrievedUser))

 
    ### helpers ###
    def getUser(self,userId):
        return self.app.get('/api/user/'+userId)
        

    def addUser(self,jsonStr):
       return self.app.post(
               '/api/user/add',
               data = jsonStr,
               headers = {'Content-Type':'application/json'}
               )

    def addUsers(self,jsonStr):
       return self.app.post(
               '/api/users/add',
               data = jsonStr,
               headers = {'Content-Type':'application/json'}
               )
 
    def getUsers(self):
        return self.app.get('/api/users')

if  __name__ == "__main__":
    unittest.main()
