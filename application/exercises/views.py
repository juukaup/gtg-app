from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user

from application import app, db, login_required, login_manager
from application.exercises.models import Exercise
from application.exercises.forms import ExerciseForm

@app.route("/exercises/new/")
def exercises_form():
    return render_template("exercises/new.html", form = ExerciseForm())

@app.route("/exercises", methods=["GET"])
def exercises_index():
    return render_template("exercises/list.html", exercises = Exercise.query.all())

@app.route("/exercises/update/<exercise_id>", methods=["POST"])
@login_required
def exercise_update(exercise_id):
    return render_template("exercises/update.html", exercise= Exercise.query.get(exercise_id), form = ExerciseForm())

@app.route("/exercises/update/make/<exercise_id>", methods=["POST"])
@login_required
def exercise_change_description(exercise_id):
    form = ExerciseForm(request.form)
    ex = Exercise.query.get(exercise_id)
    ex.change_description(form.description.data)
    db.session().commit()

    return redirect(url_for("exercises_index"))

@app.route("/exercises/delete/<exercise_id>", methods=["POST"])
@login_required
def exercise_delete(exercise_id):
    ex = Exercise.query.get(exercise_id)

    db.session().delete(ex)
    db.session().commit()

    return redirect(url_for("exercises_index"))

@app.route("/exercises/", methods=["POST"])
@login_required(role="ADMIN")
def exercises_create():
    form = ExerciseForm(request.form)

    if not form.validate():
        return render_template("exercises/new.html", form = form)

    ex = Exercise(form.name.data, form.description.data)
    ex.account_id = current_user.id

    db.session().add(ex)
    db.session().commit()

    return redirect(url_for("exercises_index"))

@app.route("/exercises/search/", methods=["GET", "POST"])
def exercises_search():
    if not request.form:
        return render_template("exercises/search.html", exercises=Exercise.query.all())

    account_id = ""
    if current_user.is_authenticated:
        account_id = current_user.id

    if request.method == 'POST':
        results = Exercise.search_by_term(
            exercise=request.form.get("exercise"),
            description=request.form.get("description"),
            term=request.form.get("search"))

        return render_template("exercises/search.html",
                               results=results)

    else:
        return render_template("exercises/search.html",
                               exercises=Exercise.query.all(),
                               account_id=account_id)
