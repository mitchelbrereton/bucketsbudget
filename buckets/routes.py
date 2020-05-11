from datetime import date
from buckets import db
from buckets.forms import ExpenseForm, LoginForm
from buckets.models import Budget, User
from flask import (
    Blueprint, flash, redirect, render_template, request,
    session, url_for, json)
from flask_login import current_user, login_required

bp = Blueprint("routes", __name__)

@bp.route("/")
@bp.route("/index") #this will be used for the home page

def index():

    return render_template('index.html', title='Home')
# the below routes are all dealing with the main budget display and creating and editing the budget expenses to track

@bp.route("/budget/", defaults={'continue_flag': 'No' }, methods=['GET', 'POST'])
@bp.route("/budget/<string:continue_flag>", methods=['GET', 'POST'])
@login_required
def disp_budget(continue_flag):
    form = ExpenseForm()
    expenses = Budget.query.filter_by(username=current_user.username).all()

    displayfields = ['group', 'expense', 'amount', 'last_paid', 'expense_cycle', 'available']
    buttonName = 'Add New Budget Expense'
    columns = [
        {'name':'Group','sortable':"true"},
        {'name':'Expense','sortable':"true"},
        {'name':'Amount','sortable':"true"},
        {'name':'Last Paid','sortable':"true"},
        {'name':'Expense Cycle','sortable':"false"},
        {'name':'Available','sortable':"false"},
        {'name':'Edit','sortable':"false"},
        {'name':'Delete','sortable':"false"}]
    rows = []
    for expense in expenses:
        expensedict = {'id':expense.id, 'username':expense.username, 'group':expense.group, 'expense':expense.expense,
        'amount':"{:.2f}".format(expense.amount), 'last_paid':expense.last_paid.strftime('%Y-%m-%d'), 'expense_cycle':expense.expense_cycle,
        'available':expense.available
        }
        rows.append(expensedict)
    #dont forget to update routes below when making new ones!
    return render_template('/budget/index.html', title='Budget', form=form, columns=columns, rows=rows, fields=displayfields,
        create_route='bp.create_expense', update_route='bp.update_expense', payday_route='bp.pay_day', self_route='bp.disp_budget', buttonName=buttonName, continue_flag=continue_flag)

@login_required
@bp.route("/budget/payday/", methods=['GET', 'POST'])
def pay_day():
        # initial 
        # set pay_day = userset date
        # if payday-today >=7 then Add expense/expensecycle to available
        # payday=today write a new last paid date
    expenses = Budget.query.filter_by(username=current_user.username).all()

    for expense in expenses:
        expense.available = expense.available + expense.amount
        expense.in_flows = expense.in_flows + expense.amount
    db.session.commit()
    flash('You got paid!')
    return redirect(url_for('routes.disp_budget'))

@login_required
@bp.route("/budget/cancel/", methods=['GET', 'POST'])
def cancel_pay():
        # initial 
        # set pay_day = userset date
        # if payday-today >=7 then Add expense/expensecycle to available
        # payday=today write a new last paid date
    expenses = Budget.query.filter_by(username=current_user.username).all()

    for expense in expenses:
        expense.available = expense.available - expense.amount
        expense.inflows = expense.in_flows - expense.amount
    db.session.commit()
    flash('Reversed Pay Week')
    return redirect(url_for('routes.disp_budget'))

@login_required
def delete_expense(expense_id):
    expense = Budget.query.get_or_404(expense_id)
    if expense.username != current_user.username:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('routes.disp_budget'))

@bp.route("/budget/create/<string:continue_flag>", methods=['GET', 'POST'])
@login_required
def create_expense(continue_flag):
    form = ExpenseForm()
    today = date.today()
    print(today)
    if form.validate_on_submit():
        #the next block is to determine the variables for the total amount required in the available bucket 
        testcycle = form.cycle.data
        amountx = form.amount.data
        last_paid = form.last_paid.data
        datedif = today-last_paid
        print(testcycle)
        if testcycle == 'Weekly':
            value = 1
        elif testcycle == 'Fortnightly':
            value = 2
        elif testcycle == 'Monthly':
            value = 4
        elif testcycle == 'Yearly':
            value = 52
        available = amountx/value*int((datedif.days)/7)
        #write form data to database
        #set starting values for inflows, outflows
        in_flows = 0
        out_flows = 0
        Expense = Budget(group=form.group.data, expense=form.expense.data, amount=form.amount.data, last_paid=form.last_paid.data, 
        username=current_user.username, expense_cycle=form.cycle.data, available=available, in_flows=in_flows, out_flows=out_flows)
        db.session.add(Expense)
        db.session.commit() 
        flash('Your expense has been created!', 'success')
        return redirect(url_for('routes.disp_budget', username=current_user.username, continue_flag=continue_flag))
    flash('FUCK!', 'Fail')
    return redirect(url_for('routes.disp_budget', username=current_user.username, continue_flag=continue_flag))

@bp.route("/budget/update/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    expense = Budget.query.get_or_404(expense_id)
    if expense.username != current_user.username:
        abort(403)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.group = form.group.data
        expense.expense = form.expense.data
        expense.amount = form.amount.data
        expense.last_paid = form.last_paid.data
        expense.expense_cycle = form.cycle.data
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('routes.disp_budget'))
    return redirect(url_for('routes.disp_budget', expense_id=expense_id))

@bp.route("/budget/delete/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def delete_expense(expense_id):
    expense = Budget.query.get_or_404(expense_id)
    if expense.username != current_user.username:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('routes.disp_budget'))

@bp.route("/budget/deleteall/", methods=['GET', 'POST'])
@login_required
def deleteall():
    Budget.query.filter_by(username=current_user.username).delete()
    db.session.commit()
    flash('Expenses Reset', 'success')
    return redirect(url_for('routes.disp_budget'))



