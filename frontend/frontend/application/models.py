from application import db
import datetime

class Usa_stock(db.Document):
    ref_id      = db.IntField(unique=True)
    short       = db.StringField()
    name        = db.StringField()
