from wtforms import DateField, StringField
from flask_wtf import FlaskForm

class PassengerCountForm(FlaskForm):
    date = DateField(label="date_inp", description="Enter date (YYY-MM-DD)")
    captcha = StringField(label="captcha_input")