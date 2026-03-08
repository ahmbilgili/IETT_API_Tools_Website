from wtforms import DateField
from flask_wtf import FlaskForm

class PassengerCountForm(FlaskForm):
    date = DateField(label="date_inp", description="Enter date (YYY-MM-DD)")
