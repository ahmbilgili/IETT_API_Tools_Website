from wtforms import Form, StringField, DateField

class ArchiveForm(Form):
    date = DateField(label="date_inp", description="Enter date")
    line_code = StringField(label="line_code_inp", description="Enter line code (leave empty for all lines)")