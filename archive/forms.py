from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class ArchiveForm(FlaskForm):
    date = DateField(label="date_inp", description="Enter date", validators=[DataRequired("Date cannot be left empty")])
    line_code = StringField(label="line_code_inp", description="Enter line code (leave empty for all lines)", validators=[DataRequired("Line code cannot be left empty")])
    captcha = StringField(label="captcha_input", validators=[DataRequired("Captcha cannot be left empty")])