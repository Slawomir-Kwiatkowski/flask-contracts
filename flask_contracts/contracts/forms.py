from datetime import datetime, timedelta
from operator import indexOf
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField, widgets
from wtforms.fields.core import RadioField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from flask_contracts.contracts.models import Contract

class ContractForm(FlaskForm):
    contract_number = StringField('Contract Number', 
        validators=[Optional(), Length(max=20)], render_kw={'autofocus': True})
    contractors = SelectField('Contractors', coerce=int, validators=[Optional()])
    date_of_delivery = DateField('Date of delivery', validators=[Optional()])
    pallets_position = IntegerField('Pallets position', validators=[Optional()])
    pallets_planned = IntegerField('Planned no. of pallets', validators=[Optional()])
    pallets_actual = IntegerField('Actual no. of pallets', validators=[Optional()])
    warehouse = StringField('Warehouse',
             validators=[Optional(), Length(min=3, max=15)])
    submit = SubmitField('Send')

    def validate_date_of_delivery(self, date_of_delivery):
        ''' Throws ValidationError if date_of_delivery is less than today'''
        if date_of_delivery.data < datetime.utcnow().date():
            raise ValidationError('Wrong date')


class FindContractForm(FlaskForm):
    contract_number = StringField('Contract Number', 
        validators=[Optional(), Length(max=20)], render_kw={'autofocus': True})
    customers = SelectField('Customers', coerce=int)
    submit = SubmitField('Choose')


class BookingForm(FlaskForm):
    choices = [str(i*timedelta(minutes=15))[:-3] for i in range(24*60//15)]
    booking_time = RadioField(choices=choices)
    driver_full_name = StringField('Driver full name', 
        validators=[DataRequired(), Length(max=20)], render_kw={'autofocus': True})
    driver_phone_number = IntegerField('Driver phone no.', validators=[DataRequired()])
    truck_reg_number = StringField('Licence plate no. ', 
        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Send')


