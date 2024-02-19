from flask_app.config.mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash, check_password_hash

db = 'login_registration'

class User:
    def __init__(self, id, first_name, last_name, email, password, created_at, updated_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password
        self.created_at = created_at
        self.updated_at = updated_at


    @classmethod
    def create(cls, first_name, last_name, email, password):
        password_hash = generate_password_hash(password)
        query = """
        INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s)
                """
        data = {
            'first_name' : first_name,
            'last_name' : last_name,
            'email' : email,
            'password_hash' : password_hash
        }
        mysql = connectToMySQL(db)
        user_id = mysql.query_db(query, data)
        return cls.find_by_id(user_id)
    @classmethod
    def find_by_email(cls, email):
        query = """
            SELECT * FROM users WHERE email = %(email)s
            """
        data = {'email': email}
        mysql = connectToMySQL(db)
        result = mysql.query_db(query, data)
        return cls(**result[0]) if result else None
    @classmethod
    def find_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id': user_id}
        mysql = connectToMySQL(db)
        result = mysql.query_db(query, data)
        return cls(**result[0]) if result else None