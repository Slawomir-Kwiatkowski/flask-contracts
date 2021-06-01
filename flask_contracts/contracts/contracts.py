from flask import Blueprint, render_template, redirect, flash
from flask.globals import request
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from .models import Contract, User
from .forms import ContractForm, CustomersForm
from flask_contracts import db
from sqlalchemy import desc

bp = Blueprint('contracts', __name__,
        template_folder='templates/contracts', static_folder='static')


@bp.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html')

@bp.route('/contract/new', methods=['GET', 'POST'])
@login_required
def new_contract():
    if current_user.role != 'customer': # only customers can add a contract
        abort(403)
    form = ContractForm()
    contractors_group = User.query.filter_by(role='contractor')
    contractors_list = [(i.id, i.username) for i in contractors_group]
    form.contractors.choices = contractors_list
    if form.validate_on_submit():
        contractor_str = form.contractors.choices[0][1]
        contractor = User.query.filter_by(username=contractor_str).first().id

        contract = Contract(contract_number=form.contract_number.data,
                            contractor_id=contractor,
                            customer_id=current_user.id,
                            date_of_delivery=form.date_of_delivery.data,
                            pallets_position=form.pallets_position.data,
                            pallets_planned=form.pallets_planned.data,
                            pallets_actual=form.pallets_actual.data,
                            warehouse=form.warehouse.data)
        db.session.add(contract)
        db.session.commit()
        flash('Contract created')
        return redirect(url_for('main.index'))
    return render_template('contract.html', title='Contract', form=form)


@bp.route('/customers', methods=['GET', 'POST'])
@login_required
def get_customer():
    form = CustomersForm()
    customers_group = User.query.filter_by(role='customer')
    customers_list = [(i.id, i.username) for i in customers_group]
    form.customers.choices = customers_list
    return render_template('customers.html', title='Customers', form=form)

@bp.route('/contract')
@login_required
def contracts():
    columns = [m.key for m in Contract.__table__.columns]
    if current_user.role == 'customer':
        result = Contract.query.filter_by(customer_id=current_user.id).all()
    elif current_user.role == 'contractor':
        result = Contract.query.filter_by(contractor_id=current_user.id).all()
    result = sorted(result, key=lambda x: x.id, reverse=True)
    return render_template('contracts.html', title='Contracts', header=columns, contracts=result)

@bp.route('/contract/<int:id>', methods=['GET', 'POST'])
@login_required
def get_contract(id):
    form = ContractForm()
    result = Contract.query.get(id)
    contractors_group = User.query.filter_by(role='contractor')
    contractors_list = [(i.id, i.username) for i in contractors_group]
    form.contractors.choices = contractors_list     # all available contractors
    if form.validate_on_submit():
        result.contract_number=form.contract_number.data
        result.contractor_id = form.contractors.data    # selected contractor
        result.date_of_delivery = form.date_of_delivery.data
        result.pallets_position = form.pallets_position.data
        result.pallets_planned = form.pallets_planned.data
        result.pallets_actual = form.pallets_actual.data
        result.warehouse = form.warehouse.data
        db.session.commit()
        return redirect(url_for('contracts.contracts'))
    form.contract_number.data = result.contract_number
    contractors_group = User.query.filter_by(role='contractor')
    contractors_list = [(i.id, i.username) for i in contractors_group]
    form.contractors.choices = contractors_list     # all available contractors
    form.contractors.data = result.contractor_id    # selected contractor
    form.date_of_delivery.data = result.date_of_delivery
    form.pallets_position.data = result.pallets_position
    form.pallets_planned.data = result.pallets_planned
    form.pallets_actual.data = result.pallets_planned
    form.warehouse.data = result.warehouse
    return render_template('contract.html', title='Contract', form=form)
    