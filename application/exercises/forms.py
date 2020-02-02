from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ExerciseForm(FlaskForm):
    name = StringField("Exercise name", [validators.Length(min=2)])
    description = StringField("Description", [validators.Length(min=3)])

    class Meta:
        csrf = False
