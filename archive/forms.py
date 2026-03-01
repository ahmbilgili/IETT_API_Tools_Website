from wtforms import StringField, DateField
from flask_wtf import FlaskForm

class ArchiveForm(FlaskForm):
    date = DateField(label="date_inp", description="Enter date")
    line_code = StringField(label="line_code_inp", description="Enter line code (leave empty for all lines)")