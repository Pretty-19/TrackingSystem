from flask import  Blueprint, request ,render_template,flash,url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user ,login_required, current_user
from .models import db,User
from . import db

#export FLASK_APP=system  bash flask run
auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
     return render_template('hello.html')


@auth.route('/login')
def login():
     return render_template('login.html')


@auth.route('/login',methods=['POST'])
def  login_post():
     email=request.form.get('email')
     password=request.form.get('password')
     remember=True if request.form.get('remember') else False
     user=User.query.filter_by(email=email).first()
     if not user and not  check_password_hash(user.password,password):
                 flash('Please check your login details and Try again.')
                 return redirect(url_for('auth.login'))
     
     login_user(user)

     return redirect(url_for('auth.profile'))

@auth.route('/signup')
def signup():
     return render_template('signup.html')


@auth.route('/signup',methods=['POST'])
def  signup_post():   #Sign Up to the site  by storing password and username
          name=request.form.get('name')
          email=request.form.get('email')
          password=request.form.get('password')
          
          user= User.query.filter_by(email=email).first()
          if user:
               flash('Email  already registred exists.','danger')
               return redirect(url_for('auth.signup'))
          new_user= User(name=name,email=email,password=generate_password_hash(password,method='sha256'))
          db.session.add(new_user)
          db.session.commit()
          flash('Account has been  created!!','success')
          return redirect(url_for('auth.signup'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)