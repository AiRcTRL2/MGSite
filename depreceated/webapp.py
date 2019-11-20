from flask import Flask,render_template, jsonify, send_from_directory, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import os
from flask_admin.contrib.sqla import ModelView
from modules.models import Products, Images
from modules.extensions import db


app = Flask(__name__)
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:////' +
                                         str(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
                                         .replace("\\", "\\\\") + "\\\\localdb")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.get_app(app)



admin = Admin(app, name='Megan McGuigan', template_mode='bootstrap3')
admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Images, db.session))

@app.route('/')
def root():
    return render_template('index.html')

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

@app.route('/addproduct/', methods=['GET'])
def create_user():
    """Create a product."""
    product_id = request.args.get('product_id')
    product_name = request.args.get('product_name')
    product_description = request.args.get('product_description')
    product_link = request.args.get('payment_link')

    if product_id and product_description and product_name and product_link:
        new_product = Products(product_id=product_id,
                        product_name=product_name,
                        product_description=product_description,
                        payment_link=product_link)  # Create an instance of the User class
        db.session.add(new_product)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    return make_response(f"{new_product} successfully created!")

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)