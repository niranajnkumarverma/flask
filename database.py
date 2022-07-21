from flask import Flask, render_template, redirect, url_for, request, flash
import os
from flask_mysqldb import MySQL
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sms@123'
app.config['MYSQL_DATABASE_DB'] = 'flask_login'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    username = 'username'
    email = 'email'
       
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user(username, email) VALUES (%s, %s)", (username, email))
    mysql.connection.commit()
    cur.close()
    return 'success'
   


if __name__ == '__main__':
    app.run()