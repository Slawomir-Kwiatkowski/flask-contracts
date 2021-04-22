from flask import Blueprint, render_template, redirect
from .models import Contract
from .forms import ContractForm

bp = Blueprint('contracts', __name__,
        template_folder='templates/contracts', static_folder='static')


@bp.route('/contract', methods=['GET', 'POST'])
def contract():
    form = ContractForm()
    if form.validate_on_submit():
        return redirect('main.news')
    return render_template('contract.html', title='Contract', form=form)



    # # contractors_group = User.query.all()
    # contractors_group = User.query.filter_by(role='contractor')
    # contractors_list = [(i.id, i.username) for i in contractors_group]
    # form.contractorsID.choices = contractors_list