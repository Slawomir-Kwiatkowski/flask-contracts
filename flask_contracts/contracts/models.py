from flask_contracts import db
from ..auth.models import User
from datetime import datetime

class Contract(db.Model):
    '''Model of contract between a contractor and a customer'''

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='open')
    conctract_number = db.Column(db.String(20), nullable=False)
    contractor_number = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_number = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_order = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_of_delivery = db.Column(db.DateTime, nullable=False)
    pallets = db.Column(db.Integer, nullable=False)
    pallet_position = db.Column(db.Integer, nullable=False)
    warehouse = db.Column(db.String(10), nullable=False)
