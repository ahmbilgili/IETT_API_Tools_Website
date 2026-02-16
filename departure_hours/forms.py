from wtforms import Form, StringField

class DepartureHoursForm(Form):
    line_code = StringField(label="line_code_inp", description="Enter bus line code (Leave empty for all lines)")
    day = StringField(label="day_inp")
    direction = StringField(label="direction_inp")