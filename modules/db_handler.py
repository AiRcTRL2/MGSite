import sqlite3
import os

# get path to the data folder
dirpath = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))).replace("\\", "\\\\") + "\\\\"


def create_extra_db(db_name, db_path=dirpath):
    """ Only execute if more than 1 DB is required initialise database.
        Requires a db filename to access again in the future and requires a path to the
        directory in which you want to save the database.
     """
    new_db = sqlite3.connect(db_path + '{}.db'.format(db_name))
    return new_db


def connect_and_do_something(db_name, db_path=dirpath):
    try:
        # db location + name
        file_string = db_path + '{}.db'.format(db_name)

        if os.path.exists(file_string) and os.path.isfile(file_string):
            db = sqlite3.connect(db_path + '{}'.format(db_name))

        else:
            raise ValueError("The specified folder location {} or {} database file does not exist."
                             .format(dirpath, db_name))
    except ValueError as error:
        return error

    finally:
        db.close()