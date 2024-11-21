from .. import db
from sqlalchemy.dialects.postgresql import ARRAY  # Since you're using PostgreSQL arrays

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)