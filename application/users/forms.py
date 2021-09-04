from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email
from application.models import User
from flask import session


class RegistrationForm(FlaskForm):
    username        = StringField("Username *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=2, max=20, message="Username must be between 2 and 20 characters long")
                                ])
    email           = EmailField("Email *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=30, message="Email must be between 10 and 30 characters long"),
                                    Email("You did not enter a valid email!")
                                ])
    password        = PasswordField("Password *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=5, max=30, message="Password must be between 5 and 30 characters long")
                                ])
    password_confirm = PasswordField("Confirm Password *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    EqualTo("password", message="Passwords must match")
                                ])
    location        = StringField("Location *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=3, max=40, message="Location must be between 3 and 40 characters long")
                                ])
    role	        = SelectField("",
								choices=[
                                    ("         ", "         "),
									("Developer", "Developer"), 
									("Recruiter", "Recruiter")],
                                validators=[
                                    InputRequired("Please select an option"),
                                    DataRequired("Please select an option")
                                ])
    submit          = SubmitField("Register")


    def validate_username(self, username):
        user = User.find_user_by_username(username.data)
        if user:
            raise ValidationError("This username already exists.")


    def validate_email(self, email):
        user = User.find_user_by_email(email.data)
        if user:
            raise ValidationError("This email already exists.")


class LoginForm(FlaskForm):
    email           = EmailField("Email",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=30, message="Email must be between 10 and 30 characters long"),
                                    Email("You did not enter a valid email!")
                                ])
    password        = PasswordField("Password",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=5, max=30, message="Password must be between 5 and 30 characters long")
                                ])
    submit          = SubmitField("Sign in")


    def validate_email(self, email):
        user = User.find_user_by_email(email.data)
        if not user:
            raise ValidationError("There is no registered account with that email.")


class UpdateProfileForm(FlaskForm):
    username        = StringField("Username *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=2, max=20, message="Username must be between 2 and 20 characters long")
                                ])
    email           = EmailField("Email *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=30, message="Email must be between 10 and 30 characters long"),
                                    Email("You did not enter a valid email!")
                                ])
    location        = StringField("Location *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=3, max=40, message="Location must be between 3 and 40 characters long")
                                ])
    picture			= URLField("Profile Picture URL")
    submit          = SubmitField("Update")

    def validate_username(self, username):
        if username.data != session["username"]:
            user = User.find_user_by_username(username.data)
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != session["email"]:
            user = User.find_user_by_email(email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

