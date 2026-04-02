from wtforms import StringField
from flask_wtf import FlaskForm

class LineServiceForm(FlaskForm):
    line_code = StringField(label="line_code_inp", description="Enter bus line code (Leave empty for all lines)")
    captcha = StringField(label="captcha_input")