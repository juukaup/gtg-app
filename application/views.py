from flask import render_template
from application import app, login_required

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<user_username>")
@login_required
def user_index(user_username):
    user = User.query.filter_by(username=user_username).first()

    if not user:
        flash("Something went wrong")
        return redirect(url_for("index"))
    
    return