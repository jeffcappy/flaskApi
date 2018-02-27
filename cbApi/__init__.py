from flask import Flask
from flask.ext.zodb import ZODB
from pyspark.sql import SparkSession

# from flask_sqlalchemy import SQLAlchemy
# import peewee

#### config ####
app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('flask.cfg')
app.url_map.strict_slashes = False


app.config['ZODB_STORAGE'] = 'file:///Users/jeffreycapobianco/coding/cbInsights/data/users.fs'
db = ZODB(app)
# db = peewee.SqliteDatabase('/tmp/cb.db')


apiSpark = SparkSession.builder \
    .master('local') \
    .appName('cbApi') \
    .getOrCreate()

#### blueprints ####
from cbApi.users.views import users_blueprint
from cbApi.hello.views import hello_blueprint

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(hello_blueprint, url_prefix='/hello')
