from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_admin import AdminIndexView, expose
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from flask import redirect, url_for
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class Products(db.Model):
    """Model for products."""

    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,
                   primary_key=True)

    product_name = db.Column(db.String(100),
                         index=True,
                         unique=True,
                         nullable=False)

    product_description = db.Column(db.String(400),
                      index=False,
                      unique=True,
                      nullable=True)

    payment_link = db.Column(db.String(300),
                        index=False,
                        unique=False,
                        nullable=True)

    product_images = db.Column(db.String(200),
                         index=False,
                         unique=True,
                         nullable=False)

    product_price = db.Column(db.Float,
                              index=False,
                              unique=False,
                              nullable=False)

    paypal_button = db.Column(db.String(1000),
                              index=False,
                              unique=True,
                              nullable=False)

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.product_name,
                'desc': self.product_description,
                'link': self.payment_link,
                'images': self.product_images,
                'price': self.product_price,
                'paypal': self.paypal_button}

    def __repr__(self):
        return '<Product details\n Name: {}\nID: {} \nDescription {}\nPayment Link: {}>'\
            .format(self.id, self.product_name, self.product_description, self.payment_link, self.product_images,
                    self.product_price, self.paypal_button)

class User(db.Model, UserMixin):

    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    password_hash = db.Column(db.String(200))
    authenticated = db.Column(db.Boolean, default=False)

    # def is_accessible(self):
        # return current_user.is_authenticated

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    def is_anonymous(self):
        return False

    def is_active(self):
        return True


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


    # def _handle_view(self, name, **kwargs):
    #     if not self.is_accessible():
    #         return redirect(url_for('login'))
