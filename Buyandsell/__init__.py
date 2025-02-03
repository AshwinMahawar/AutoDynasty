import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# create the extension

# create the app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///AutoDynasty.db"

app.config['SECRET_KEY']='ahfusffosfdjusfdjgbs'
#db.init(app)
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

from Buyandsell import Route