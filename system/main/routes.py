from flask import Blueprint,request,render_template,flash, redirect, url_for
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import check_password_hash, generate_password_hash
from system.extenstions import db 
from system.models import User ,Project ,Bug
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



from collections import Counter
import matplotlib.pyplot as plt
import pandas
from io import BytesIO
import base64

@auth.route('/dashboard',methods = ['GET','POST'])
@login_required
def dashboard():
    
    img = BytesIO()
    typelist = [bug.Type for bug in Bug.query.all()]
    count = Counter(typelist)
    df=pandas.DataFrame.from_dict(count,orient='index')
    
    gph=df.plot(kind='bar')
    plt.xticks(rotation=360, horizontalalignment="center")
    plt.title("Type of Issues Raised")
    plt.xlabel("Types of Issues")
    plt.ylabel("Number of Issues")
    gph.get_figure().savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_type = base64.b64encode(img.getvalue()).decode('utf8')
    

    img = BytesIO()
    prioritylist = [bug.Priority for bug in Bug.query.all()]
    count = Counter(prioritylist)
    df=pandas.DataFrame.from_dict(count,orient='index')
    
    gph=df.plot(kind='bar')
    plt.xticks(rotation=360, horizontalalignment="center")
    plt.title("Priority of Issues Raised")
    plt.xlabel("Priority of Issues")
    plt.ylabel("Number of Issues")
    gph.get_figure().savefig(img,format='png')
    plt.close()
    img.seek(0)
    plot_priority = base64.b64encode(img.getvalue()).decode('utf8')

 



    projects = Project.query.all()
    return render_template('dashboard.html', projects = projects,plot_type=plot_type,plot_priority=plot_priority)
 


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
    prjname=request.args.get('prjname')
    return render_template('BugTracker.html',prjname=prjname)


@auth.route('/buglist', methods=['GET', 'POST'])
@login_required
def buglist():
    buglist = Bug.query.all()
    prjname=request.args.get('prjname')
    return render_template('buglist.html',buglist=buglist,prjname=prjname)



@auth.route('/bugtracker/create', methods=['GET', 'POST'])
@login_required
def postissue():
    title = request.form.get('title')
    issuedetails = request.form.get('issuedetails')
    issuepriority = request.form.get('issuepriority')
    issuestatus = request.form.get('issuestatus')
    issuetype = request.form.get('issuetype')
    if request.method == "POST":
            post = Bug(title =title, Description = issuedetails, Status = issuestatus,Type = issuetype,Priority = issuepriority)
            db.session.add(post)
            db.session.commit()
            flash('You post has been created !', 'success')
            return redirect(url_for('auth.dashboard'))
    else:
            flash('Something went wrong .... Please try again.', 'danger')   
            return redirect(url_for('auth.dashboard'))





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))




if __name__ == "__main__":
    auth.run(debug=True)