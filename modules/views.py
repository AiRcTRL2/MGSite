from flask import request,render_template, jsonify, send_from_directory, request, make_response, flash, redirect, url_for
from flask import escape
import os
from modules.models import Products, AdminView, User
from app import app, db, login
from modules.models import LoginForm, MyAdminIndexView
from flask_login import login_user, login_required, logout_user
from flask_admin import Admin
import paypalrestsdk


admin = Admin(app, name='Megan McGuigan', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(AdminView(Products, db.session))

paypalrestsdk.configure({
  "mode": "sandbox",  # sandbox or live
  "client_id": "AZd_jlK7ufOW1rQ06NhSvdTXfdnsZ-MKyGxMYETJNxTSXWtCO_l9EbteYUxMEPoVz6VXUrwDND33jM_W",
  "client_secret": "EF6q0qATxwvQSbMmtSA3boSNMll4vMj7ikp2qa5jUyBSU7xCM9qgD04fmsKbYX76oA5Qd0XRb2HMv5QF"})

@login.user_loader
def load_user(username):
    return db.session.query(User).get(username)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/payment/<product_id>', methods=['GET','POST'])
def payment(product_id):
    product = Products.query.get(product_id)
    product = product.serialize
    print(product['name'])
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "{}".format(product['name']),
                    "sku": "{}".format(product_id),
                    "price": "{}".format(product['price']),
                    "currency": "EUR",
                    "quantity": 1}]},
            "amount": {
                "total": "{}".format(product['price']),
                "currency": "EUR"},
            "description": "{}".format(product['desc'])}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print("Payment execution success.")
        success = True
    else:
        print(payment.error)
    return jsonify({'success': success})

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/lookbook')
def lookbook():
    return render_template('lookbook.html')

@app.route('/diary')
def diary():
    return render_template('diary.html')

@app.route('/diary/imgs')
def get_diary_images():

    path = str(app.root_path) + "\\static\\img\\diary"
    files = []

    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.JPG'):
            files.append(file)

    return jsonify(files)

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/getproducts/')
def get_products():
    products = Products.query.all()
    return jsonify(data=[products.serialize for products in products])

@app.route('/getproduct/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.query.get(product_id)
    return jsonify(data=product.serialize)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.name == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or Pass')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login successful')
        return redirect('/admin')
    return render_template('login.html', title='Sign In', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
