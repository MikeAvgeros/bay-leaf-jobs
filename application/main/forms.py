from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length


class ContactForm(FlaskForm):
    name		= StringField("Name *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=5, max=50, message="Company must be between 5 and 50 characters long")
								])
    email		= StringField("Email *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=5, max=50, message="Position must be between 5 and 50 characters long")
								])
    body		= TextAreaField("Message *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=10, max=200, message="Message must be between 10 and 200 characters long")
								])
    submit          = SubmitField("Send")