from flask import render_template, Blueprint
 
#### config ####
hello_blueprint = Blueprint('hello', __name__) 
 
#### routes ####
@hello_blueprint.route('/')
def hello():
    return "hello"

