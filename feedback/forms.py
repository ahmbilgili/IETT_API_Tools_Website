from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
    email = StringField(label="email_field", description="email")
    feedback = StringField(label="feedback_field", validators=[DataRequired("Feedback cannot be left empty")])
    captcha = StringField(label="captcha_input", validators=[DataRequired("Captcha cannot be left empty")])