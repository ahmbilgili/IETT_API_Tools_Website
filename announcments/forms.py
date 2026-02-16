from wtforms import Form, StringField

class AnnouncmentsForm(Form):
    line_code = StringField(label="line_code_inp", description="Enter line code (leave empty for all lines)")