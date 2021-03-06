from flask_contracts import db
from ..auth.models import User
from datetime import datetime

class Contract(db.Model):
    '''Model of contract between a contractor and a customer'''

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='open')
    contract_number = db.Column(db.String(20), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_of_order = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_of_delivery = db.Column(db.Date, nullable=False)
    pallets_position = db.Column(db.Integer)
    pallets_planned = db.Column(db.Integer, nullable=False)
    pallets_actual = db.Column(db.Integer)    
    warehouse = db.Column(db.String(10), nullable=False)
    

class Booking(db.Model):
    '''Model of booking for a conctract'''
    id = db.Column(db.Integer, primary_key=True)
    booking_time = db.Column(db.String(5), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey(Contract.id), nullable=False)
    driver_full_name = db.Column(db.String(20), nullable=False)
    driver_phone_number = db.Column(db.Integer, nullable=False)
    truck_reg_number = db.Column(db.String(10))

