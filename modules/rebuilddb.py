from modules.db_handler import create_extra_db
from modules.models import db, User

create_extra_db("localdb")

db.create_all()
m = User(name='Megan', password_hash="default", authenticated=True)
m.set_password("hello")
print(m.check_password("hello"))
db.session.add(m)
db.session.commit()

