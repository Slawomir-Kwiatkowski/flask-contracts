from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_contracts.contracts.models import Contract

class ContractForm(FlaskForm):
    contract_number = StringField('Contract Number', 
        validators=[DataRequired(), Length(max=20)], render_kw={'autofocus': True})
    contractors = SelectField('Contractors', coerce=int)
    date_of_delivery = DateField('Date of delivery', validators=[DataRequired()])
    pallets_position = IntegerField('Pallets position', validators=[DataRequired()])
    pallets_planned = IntegerField('Planned no. of pallets', validators=[DataRequired()])
    pallets_actual = IntegerField('Actual no. of pallets', validators=[DataRequired()])
    warehouse = StringField('Warehouse',
             validators=[DataRequired(), Length(min=3, max=15)])
    submit = SubmitField('Send')

    def validate_contract_number(self, contract_number):
        ''' Throws ValidationError if user has created contracts with the same number'''
        contract = Contract.query.filter_by(
            customer_id=current_user.id).filter_by(
                contract_number=contract_number.data).first()
        if contract: raise ValidationError('This contract number is already in database')

    def validate_date_of_delivery(self, date_of_delivery):
        ''' Throws ValidationError if date_of_delivery is less than tomorrow'''
        if date_of_delivery.data <= datetime.utcnow().date():
            raise ValidationError('Wrong date')

class CustomersForm(FlaskForm):
    # date_reg = DateField('Date', validators=[DataRequired()])
    customers = SelectField('Customers', coerce=int)
    submit = SubmitField('Choose')