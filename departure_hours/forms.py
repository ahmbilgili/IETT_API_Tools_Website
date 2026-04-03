from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class DepartureHoursForm(FlaskForm):
    line_code = StringField(label="line_code_inp", description="Enter bus line code (Leave empty for all lines)", validators=[DataRequired("Line code cannot be left empty")])
    day = SelectField(label="day_inp", choices=[("I", "Weekday"), ("C", "Saturday"), ("P", "Sunday")], validators=[DataRequired("Day cannot be left empty")])
    direction = StringField(label="direction_inp")     
    captcha = StringField(label="captcha_input")