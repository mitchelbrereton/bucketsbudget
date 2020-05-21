from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from buckets.models import User, Budget
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ExpenseForm(FlaskForm):
    group = StringField('group', validators=[DataRequired()])
    expense = StringField('expense', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[DataRequired()])
    last_paid = DateField('Last Paid', validators=[DataRequired()])
    cycle = SelectField('Expense Cycle', choices=[('Weekly', 'Weekly'),('Fortnightly','Fortnightly'),('Monthly','Monthly'),('Yearly','Yearly')])
    nxtlst_select = SelectField('Next/Last Date Select', choices=[('lp', 'Last Paid'),('nd','Next Due')])
    submit = SubmitField('Add Expense')

def getExpenseCat():
    return Budget.query.filter_by(username=current_user.username).all()

class TransactForm(FlaskForm):
    expense = QuerySelectField('expense', get_label='expense', query_factory=getExpenseCat, validators=[DataRequired()]) #this should be a select field which is filled from the expenses in the Budget table
    amount = IntegerField('amount', validators=[DataRequired()])
    date = DateField('Last Paid', validators=[DataRequired()]) #this should be a calender picker
    note = StringField('note')
    submit = SubmitField('Add Transaction')