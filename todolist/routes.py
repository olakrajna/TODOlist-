from todolist import app, db
from flask import render_template, request, redirect, url_for, flash
from todolist.models import Todo, User
from todolist.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

@app.route('/')
def home_page():    
    return render_template('home.html')

@app.route('/mytasks')
@login_required
def mytasks_page():
    todo_list = Todo.query.all()
    return render_template('mytasks.html', todo_list=todo_list) 

@app.route("/add", methods=["POST"])
def add():
    #add new item
    date = request.form.get("date")
    title = request.form.get("title")
    new_todo = Todo(title=title, date=date, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("mytasks_page")) 

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #update item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete 
    db.session.commit()
    return redirect(url_for("mytasks_page"))     

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #update item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo) 
    db.session.commit()
    return redirect(url_for("mytasks_page"))      

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address = form.email_address.data, password=form.password1.data )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('mytasks_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')  

    return render_template('register.html', form=form)

@app.route('/login',  methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('mytasks_page'))
        else:
            flash('Username and password are not match! Please try again.', category='danger')        
    return render_template('login.html', form=form)    

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))