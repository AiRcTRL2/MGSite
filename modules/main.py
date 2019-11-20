from app import app, db
from modules.models import *
from modules.views import *

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)

