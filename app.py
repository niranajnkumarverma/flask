
from crypt import methods
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Regexp, DataRequired
import sqlite3




app = Flask(__name__, static_url_path='/static')


app.config['SECRET_KEY'] = 'dont look at me im a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
@app.before_first_request
def create_tables():
    db.create_all()





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    # phone = db.Column(db.String(16),nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}', '{self.email}')"

    def two_factor_enabled(self):
        return self.phone is not None    




class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Please Enter your Username"})
    email = EmailField(validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Please Enter your email"})
    # phone = StringField(validators=[DataRequired(),Length( max=10)], render_kw={"placeholder": "Please Enter your Phone"})
    password = PasswordField(validators=[DataRequired(), Length(min=3, max=20, message='Enter password with difined condition'), EqualTo('confpass', message="Passwords doesn't match"),
    Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,12}$', flags=0, message="Enter password with difined way")], render_kw={"placeholder": "Passowrd"})
    confpass = PasswordField(validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Confirm Passowrd"})
    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("Email Already Registered..Try Different One!!")
   

class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Please Enter your email"})
    password = PasswordField(validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Please Enter your Passowrd"})
    submit = SubmitField("Login")


class AdminForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Please Enter your Email & Username"})
    password = PasswordField(validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Please Enter your Password"})
    submit = SubmitField("Login")





@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        #hash_password = form.password.data
        new_user = User(username=form.username.data,email=form.email.data ,password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        con = sqlite3.connect("flask.db")
        cur = con.cursor()
        cur.execute("select * from user")
        cur = cur.fetchall(); 
        TWILIO_ACCOUNT_SID='AC60080740b62ffb0f41ba034a3c113c68'
        TWILIO_AUTH_TOKEN='0bd91b5fd10f3dd2430d61a2a38f21b6'
        user = User(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    user = User.query.filter_by(username=current_user.username, email=current_user.email).first()
    # data = User.query.filter_by(id=id).first()
    return render_template('profile.html', user=user)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # if user.password == user.password.data:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
               
                return redirect(url_for('profile'))
    return render_template('login.html', form=form)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    user = User.query.filter_by(id=id).first()
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user.username = form.username.data
        user.email = form.email.data
        user.password = hash_password
        db.session.add(user)
        db.session.commit()
        flash('Your profile is successfully updated')
        return redirect(url_for('profile', user=user))
    return render_template('update.html', form=form, user=user)


################# Admin login part ###############################################


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data, password= form.password.data).first()
        if admin:
            # if admin.password == form.password.data:
            # if bcrypt.check_password_hash(admin.password, form.password.data):
                # login_user(admin)
            return redirect(url_for('adminprofile'))
        # else:
        #     return render_template('adminlogin.html')
    return render_template('adminlogin.html', form = form)


@app.route('/adminprofile', methods=['GET', 'POST'])
def adminprofile():

    users = User.query.all()
    for i in users:
        
        name = i.username
        print(name)
        # mail = users.email
    return render_template('adminprofile.html', users=users)


@app.route('/adupdate/<int:id>', methods=['GET', 'POST'])
def adupdate(id):
    user = User.query.filter_by(id=id).first()
    form = RegisterForm()
    if form.validate_on_submit():    
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user.username = form.username.data
        user.email = form.email.data
        user.password = hash_password
        db.session.add(user)
        db.session.commit()
        flash('Your profile is successfully updated')
        return redirect(url_for('adminprofile'))
    return render_template('adminupdate.html', form=form, user=user)
       
@app.route('/addelete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    #get task
    user = User.query.get(id)
    #delete task
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('adminprofile'))
    
if __name__ == '__main__':
    app.run(debug=True, port=9000)