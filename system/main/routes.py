from flask import Blueprint,request,render_template,flash, redirect, url_for
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import check_password_hash, generate_password_hash
from system.extenstions import db 
from system.models import User ,Project

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
    if user:
          login_user(user,remember=remember)
          return redirect(url_for('auth.dashboard'))
    
    if not user or not  check_password_hash(user.password,password):
          flash('Please check your login details and Try again.')
          return redirect(url_for('auth.login'))
    
@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first() 
    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/dashboard',methods = ['GET','POST'])
@login_required
def dashboard():
    project = Project.query.all()
    return render_template('dashboard.html', name=current_user.name,project = project)


@auth.route('/insert', methods = ['POST'])
def insert():
        prjname = request.form.get('prjname')
        description = request.form.get('description')
        my_data = Project(prjname=prjname, description=description)
        db.session.add(my_data)
        db.session.commit()
        flash('Employee Added successfully')
        return redirect(url_for('auth.dashboard'))
 
 

@auth.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Project.query.get(request.form.get('id'))
        my_data.prjname = request.form.get('prjname')
        my_data.description = request.form.get('description')
        db.session.commit()
        flash("Employee Updated Successfully")
 
        return redirect(url_for('auth.dashboard'))
 
 
@auth.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Project.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('auth.dashboard'))
 


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))



if __name__ == "__main__":
    auth.run(debug=True)