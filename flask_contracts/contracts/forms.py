from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from flask_contracts.contracts.models import Contract

class ContractForm(FlaskForm):
    contract_number = StringField('Contract Number', 
        validators=[DataRequired(), Length(max=20)])
    contractor = SelectField('Role',
     choices=[('contractor', 'contractor'), ('customer', 'customer')])
    date_of_delivery = DateField('Date of delivery', validators=[DataRequired()])
    pallets = IntegerField('No. of pallets', validators=[DataRequired()])
    pallets_position = IntegerField('Pallets position', validators=[DataRequired()])
    warehouse = StringField('Warehouse',
             validators=[DataRequired(), Length(min=3, max=15)])
    submit = SubmitField('Send')