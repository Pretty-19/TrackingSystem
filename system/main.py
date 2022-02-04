from flask import Blueprint,request,render_template,flash, redirect, url_for
from flask_login import login_required, current_user
from .models import ProjectData 
from . import db ,create_app

main = Blueprint('main', __name__)
db.create_all(app=create_app())

@main.route('/')
def index():
   return render_template('hello.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)





#this route is for inserting data to mysql database via html forms
@main.route('/insert', methods = ['GET','POST'])
def insert():
    if request.method == 'POST':
        prjname = request.form.get('prjname')
        details = request.form.get('details')
        
        oneproject = ProjectData(prjname=prjname, details=details)

        db.session.add(oneproject)
        db.session.commit()
        flash("Project Added Successfully")
        return redirect('/dashboard')


#this is our update route where we are going to update our employee
@main.route('/update', methods = ['POST'])
def update():
    if request.method == 'POST':
        my_data = ProjectData.query.get(request.form.get('id'))
        my_data.prjname = request.form['prjname']
        my_data.details = request.form['details']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('dashboard'))




#This route is for deleting our employee
@main.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = ProjectData.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    main.run(debug=True)