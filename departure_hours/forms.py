from wtforms import Form, StringField, SelectField

class DepartureHoursForm(Form):
    line_code = StringField(label="line_code_inp", description="Enter bus line code (Leave empty for all lines)")
    day = SelectField(label="day_inp", choices=[("I", "Weekday"), ("C", "Saturday"), ("G", "Sunday")])
    direction = StringField(label="direction_inp")            