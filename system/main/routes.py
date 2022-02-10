from flask import Blueprint,request,render_template,flash, redirect, url_for
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import check_password_hash, generate_password_hash
from system.extenstions import db 
from system.models import User ,Project
from system.main.forms import ProjectForm


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
    projects = Project.query.all()
    return render_template('dashboard.html',projects = projects)
 
@auth.route('/dashboard/add', methods = ['GET','POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        my_data = Project(prjname=form.prjname.data, description=form.description.data)
        db.session.add(my_data)
        db.session.commit()
        flash('You have successfully added a new project.')
        return redirect(url_for('auth.dashboard'))
    return render_template('project.html', action="Add",form=form,title="Add Project")


@auth.route('/dashboard/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):

    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.prjname = form.prjname.data
        project.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        return redirect(url_for('auth.dashboard'))

    form.description.data = project.description
    form.prjname.data = project.prjname
    return render_template('project.html', action="Edit",
                           add_project=add_project, form=form,
                           project=project, title="Edit Project")


@auth.route('/dashboard/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')
    return redirect(url_for('auth.dashboard'))



@auth.route('/bugtracker', methods=['GET', 'POST'])
@login_required
def bugtracker():
    return render_template('BugTracker.html')




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))



if __name__ == "__main__":
    auth.run(debug=True)