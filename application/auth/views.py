from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, bcrypt
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

    if not form.validate():
        return render_template("auth/registerform.html", form=form, error="problems")

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    new_user = User(form.name.data, form.username.data, pw_hash)

    db.session().add(new_user)
    db.session().commit()

    new_user_login = User.query.filter_by(username=form.username.data).first()
    login_user(new_user_login)
    return redirect(url_for("index"))


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
                                
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")

    if not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form, 
        error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 