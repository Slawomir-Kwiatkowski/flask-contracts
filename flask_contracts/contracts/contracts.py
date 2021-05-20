from flask import Blueprint, render_template, redirect
from .models import Contract, User
from .forms import ContractForm, CustomersForm

bp = Blueprint('contracts', __name__,
        template_folder='templates/contracts', static_folder='static')


@bp.route('/contract/new', methods=['GET', 'POST'])
def new_contract():
    form = ContractForm()
    if form.validate_on_submit():
        return redirect('main.news')
    return render_template('contract.html', title='Contract', form=form)


@bp.route('/customers', methods=['GET', 'POST'])
def get_customer():
    form = CustomersForm()
    # customers_group = User.query.all()
    customers_group = User.query.filter_by(role='customer')
    customers_list = [(i.id, i.username) for i in customers_group]
    form.customersID.choices = customers_list
    return render_template('customers.html', title='Customers', form=form)