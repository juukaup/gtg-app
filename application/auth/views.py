from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db, bcrypt, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm, ChangePasswordForm

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)
    
    username = User.query.filter_by(username=form.username.data).first()
    if username:
        return render_template("auth/registerform.html", form=form, error="Username already exists")
    print(form.name.data, form.username.data, form.password.data)
    if not form.validate():
        return render_template("auth/registerform.html", form=form)
    
    pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(form.name.data, form.username.data, pw_hash)

    db.session().add(new_user)
    db.session().commit()
    flash("Registration successful!")

    new_user_login = User.query.filter_by(username=form.username.data).first()
    login_user(new_user_login)
    return redirect(url_for("index"))


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
                                
    wrong_credentials_msg = "Invalid username or password"
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error=wrong_credentials_msg)

    if not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form, 
        error=wrong_credentials_msg)

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 