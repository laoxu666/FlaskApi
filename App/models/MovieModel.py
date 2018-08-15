from App.ext import db
from App.models.ModelUtil import BaseModel


class Movie(BaseModel, db.Model):
    m_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    m_name = db.Column(db.String(32))


