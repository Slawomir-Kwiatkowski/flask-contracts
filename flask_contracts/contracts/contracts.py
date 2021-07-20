from flask import Blueprint, render_template, redirect, flash, current_app
from flask.globals import request, session
from flask.helpers import send_file, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from .models import Contract, User, Booking
from .forms import BookingForm, ContractForm, FindContractForm
from flask_contracts import db
from sqlalchemy import desc
from .utils.utils import create_pdf


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


@bp.route('/find-contract', methods=['GET', 'POST'])
@login_required
def find_contract():
    form = FindContractForm()
    customers_group = User.query.filter_by(role='customer')
    customers_list = [(i.id, i.username) for i in customers_group]
    form.customers.choices = customers_list
    if form.validate_on_submit():
        contract = Contract.query.filter_by(
                              contract_number=form.contract_number.data).filter_by(
                                  customer_id=form.customers.data).first()
        if contract is not None:
            return redirect(url_for('contracts.get_contract', id=contract.id))
        else:
            flash('No contract with the given criteria')
    return render_template('find_contract.html', title='Find contract', form=form)

@bp.route('/contract', methods=['GET'])
@login_required
def contracts(page=1, per_page=5):
    if request.args.get('page'):
        page = int(request.args.get("page"))
        session['page'] = page
    if request.args.get('per_page'):
        per_page = int(request.args.get('per_page'))
        session['per_page'] = per_page
    columns = [m.key for m in Contract.__table__.columns]
    if current_user.role == 'customer':
        result = Contract.query.filter_by(
            customer_id=current_user.id).filter(
                Contract.status!='cancelled').order_by(
                    Contract.id.desc()).paginate(page=page, per_page=per_page)
    elif current_user.role == 'contractor':
        result = Contract.query.filter_by(
            contractor_id=current_user.id).filter(
                Contract.status!='cancelled').order_by(
                    Contract.id.desc()).paginate(page=page, per_page=per_page)
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
        if current_user.role == 'contractor':
            result.pallets_position = form.pallets_position.data
            result.pallets_actual = form.pallets_actual.data
        else:
            result.status = 'open'
            result.contract_number=form.contract_number.data
            result.contractor_id = form.contractors.data    # selected contractor
            result.date_of_delivery = form.date_of_delivery.data
            result.pallets_planned = form.pallets_planned.data
            result.warehouse = form.warehouse.data
        db.session.commit()
        if current_user.role=='contractor':
            return redirect(url_for('contracts.new_booking', id=id))
        return redirect(url_for('contracts.contracts'))
    form.contract_number.data = result.contract_number
    contractors_group = User.query.filter_by(role='contractor')
    contractors_list = [(i.id, i.username) for i in contractors_group]
    form.contractors.choices = contractors_list     # all available contractors
    form.contractors.data = result.contractor_id    # selected contractor
    form.date_of_delivery.data = result.date_of_delivery
    form.pallets_position.data = result.pallets_position
    form.pallets_planned.data = result.pallets_planned
    form.pallets_actual.data = result.pallets_actual
    form.warehouse.data = result.warehouse
    return render_template('contract.html', title='Contract', form=form)
    

@bp.route('/contract/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_contract(id):
    result = Contract.query.get(id)
    if current_user.id != result.customer_id: 
        abort(403)
    result.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('contracts.contracts'))

@bp.route('/booking/<int:id>', methods=['GET', 'POST'])
@login_required
def new_booking(id):
    form = BookingForm()
    result = Booking.query.filter_by(contract_id=id).first()
    current_contract = Contract.query.get(id) # Returns contract for current booking
    # Filtering by one column gives a list of tuple(s) so I converted it to a list of values
    contracts = [ids[0] for ids in Contract.query.with_entities(Contract.id).filter_by(
        date_of_delivery=current_contract.date_of_delivery).filter_by(
        warehouse=current_contract.warehouse).all()]
    if form.validate_on_submit():
        if result:
            result.booking_time = form.booking_time.data
            result.driver_full_name = form.driver_full_name.data
            result.driver_phone_number = form.driver_phone_number.data
            result.truck_reg_number = form.truck_reg_number.data
            db.session.commit()
        else:
            booking = Booking(booking_time=form.booking_time.data, 
                            contract_id = id,
                            driver_full_name=form.driver_full_name.data,
                            driver_phone_number=form.driver_phone_number.data,
                            truck_reg_number=form.truck_reg_number.data)
            db.session.add(booking)
            db.session.commit()
        contract = Contract.query.get(id)
        contract.status = 'accepted'
        db.session.commit()
        page = session.get('page')
        per_page = session.get('per_page')
        return redirect(url_for('contracts.contracts', page=page, per_page=per_page))
    if result is not None:
        reserved_booking_time = [times[0] for times in 
            Booking.query.with_entities(Booking.booking_time).filter(
            Booking.contract_id.in_(contracts)).all() if times[0]!=result.booking_time]   
        form.booking_time.data = result.booking_time
        form.driver_full_name.data = result.driver_full_name
        form.driver_phone_number.data = result.driver_phone_number
        form.truck_reg_number.data = result.truck_reg_number   
    else:
        reserved_booking_time = [times[0] for times in 
            Booking.query.with_entities(Booking.booking_time).filter(
            Booking.contract_id.in_(contracts)).all()] 
    return render_template('booking.html', form=form, reserved_booking_time=reserved_booking_time)

@bp.route('/get-pdf/<int:id>', methods=['GET'])
@login_required
def get_pdf(id):
    contract = Contract.query.get(id)
    contractor = User.query.get(contract.contractor_id)
    booking = Booking.query.filter_by(contract_id=contract.id).first()
    pdf = create_pdf(booking_no=booking.id,
                        contractor=contractor.username,
                        contractor_no=contractor.id,
                        truck_plate=booking.truck_reg_number,
                        warehouse=contract.warehouse,
                        date=contract.date_of_delivery,
                        time=booking.booking_time,
                        pallets_pos=contract.pallets_position,
                        pallets=contract.pallets_actual)
    pdf.seek(0)
    return send_file(pdf, as_attachment=True, mimetype='application/pdf',
        attachment_filename='booking.pdf', cache_timeout=0)