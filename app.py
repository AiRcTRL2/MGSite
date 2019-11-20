from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' +
                                         str(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
                                         .replace("\\", "\\\\") + "\\\\localdb.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'feainefai2££'

login = LoginManager(app)
login.session_protection = 'strong'
login.login_view = 'login'
login.init_app(app)

db = SQLAlchemy(app)


