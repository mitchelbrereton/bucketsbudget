from flask import current_app
from buckets import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Setup the relationship to the User table
    budget = db.relationship('Budget', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(140))
    expense = db.Column(db.String(140))
    amount = db.Column(db.Float)
    last_paid = db.Column(db.DateTime, index=True)
    next_due = db.Column(db.DateTime)
    expense_cycle = db.Column(db.String)
    in_flows = db.Column(db.Float)
    out_flows = db.Column(db.Float)
    available = db.Column(db.Float)
    est_min = db.Column(db.Float)
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    # Setup the relationship to the Transaction table
    transactions = db.relationship('Transactions', lazy='dynamic')

    def __repr__(self):
        return '<Budget {}>'.format(self.id)
class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(140))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, index=True)
    note = db.Column(db.String(240))
    username = db.Column(db.String(64), db.ForeignKey('user.username'))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))

    def __repr__(self):
        return '<Transactions {}>'.format(self.id)