from wtforms import Form, DateField

class DepartureCountForm(Form):
    date = DateField(label="date_inp", description="Enter date (YYY-MM-DD)")
