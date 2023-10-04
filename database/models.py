from database import db
from sqlalchemy.sql import func

class ForSaleImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary)
    name = db.Column(db.String(150))
    description = db.Column(db.String(2000))   
    toolTip = db.Column(db.String(150)) 
    insertTimeStamp = db.Column(db.DateTime(timezone=True), default=func.now())
    isActive = db.Column(db.Boolean)

def __init__(self, img, name, description, toolTip, insertTimeStamp, isActive):
    self.img = img
    self.name = name
    self.description = description
    self.toolTip = toolTip
    self.insertTimeStamp = insertTimeStamp
    self.isActive = isActive

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(20))

def __init__(self, id, username, password_hash):
    self.id = id
    self.username = username
    self.password_hash = password_hash