from application import app, db
from flask import redirect, render_template, request, url_for
from application.exercises.models import Exercise

@app.route("/exercises", methods=["GET"])
def exercises_index():
    return render_template("exercises/list.html", exercises = Exercise.query.all())

@app.route("/exercises/update/<exercise_id>", methods=["POST"])
def exercise_update(exercise_id):
    return render_template("exercises/update.html", exercise= Exercise.query.get(exercise_id))

@app.route("/exercises/update/make/<exercise_id>", methods=["POST"])
def exercise_change_description(exercise_id):
    ex = Exercise.query.get(exercise_id)
    ex.change_description(request.form.get("description"))
    db.session().commit()

    return redirect(url_for("exercises_index"))

@app.route("/exercises/new/")
def exercises_form():
    return render_template("exercises/new.html")

@app.route("/exercises/", methods=["POST"])
def exercises_create():
    ex = Exercise(request.form.get("name"), request.form.get("description"))

    db.session().add(ex)
    db.session().commit()

    return redirect(url_for("exercises_index"))

