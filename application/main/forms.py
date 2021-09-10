from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Length


class ContactForm(FlaskForm):
    name		= StringField("Name *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=2, max=30, message="Name must be between 2 and 30 characters long")
								])
    email		= EmailField("Email *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=5, max=50, message="Email must be between 5 and 50 characters long")
								])
    body		= TextAreaField("Message *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=10, max=200, message="Message must be between 10 and 200 characters long")
								])
    submit          = SubmitField("Send")
