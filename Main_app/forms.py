from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Recommend_movies_form(FlaskForm):
    input_movie = StringField(label='MovieName', validators=[DataRequired()])
    submit = SubmitField(label='Search')


class Discover_movies_form(FlaskForm):
    input_movie = StringField(label='MovieName', validators=[DataRequired()])
    submit = SubmitField(label='Search')
