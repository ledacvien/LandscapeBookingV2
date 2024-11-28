from .. import db
from sqlalchemy.dialects.postgresql import ARRAY 

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)