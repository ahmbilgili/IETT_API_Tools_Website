from wtforms import DateField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class PassengerCountForm(FlaskForm):
    date = DateField(label="date_inp", description="Enter date (YYY-MM-DD)", validators=[DataRequired("Date cannot be left empty")])
    captcha = StringField(label="captcha_input", validators=[DataRequired("Captcha cannot be left empty")])