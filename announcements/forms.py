from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

# Inherits from FlaskForm so that we can use the CSRF functionality

class AnnouncementsForm(FlaskForm):
    line_code = StringField(label="line_code_inp", description="Enter line code (leave empty for all lines)")
    captcha = StringField(label="captcha_input", validators=[DataRequired("Captcha cannot be left empty")])