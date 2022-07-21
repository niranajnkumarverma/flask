from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

# {% extends 'layout.html' %}
# {% block title %}Profile{% endblock %}
# {% block content %}
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Profile</title>
# </head>
# <body style="background-color:powderblue;">
# <center>
#  <h1>Hello !!!{{user.username}} </h1><br><br>
 
#  <div>
#     <h2>Your account details are below:</h2>
#     <p>Your  username is: {{user.username}} </p>
#     <p>Your  email is: {{user.email}} </p>
    
# </div>

#  <!-- <a href="{{url_for('logout')}}">Logout</a><br><br> -->
#  <a href="/update/{{user.id}}">Update Profile</a>
#  </center>
# </body>
# </html>
# {% endblock %}

