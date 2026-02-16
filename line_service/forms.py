from wtforms import Form, StringField

class LineServiceForm(Form):
    line_code = StringField(label="line_code_inp", description="Enter bus line code (Leave empty for all lines)")