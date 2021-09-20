from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError


class JobForm(FlaskForm):
    company = StringField(
        "Company *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=5,
                max=50,
                message="Company must be between 5 and 50 characters long")])
    company_logo = URLField("Company Logo URL")
    position = StringField(
        "Position *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=5,
                max=50,
                message="Position must be between 5 and 50 characters long")])
    location = StringField(
        "Location *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=3,
                max=40,
                message="Location must be between 3 and 40 characters long")])
    salary = StringField("Salary")
    level = SelectField("",
                        choices=[
                            ("Senior", "Senior"),
                            ("Midweight", "Midweigth"),
                            ("Junior", "Junior")])
    stack = SelectField("",
                        choices=[
                            ("Front End", "Front End"),
                            ("Back End", "Back End"),
                            ("Full Stack", "Full Stack")])
    contract = SelectField("",
                           choices=[
                               ("Full Time", "Full Time"),
                               ("Part Time", "Part Time"),
                               ("Freelance", "Freelance")])
    description = TextAreaField("Description *",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!")
                                ])

    def validate_company_logo(self, company_logo):
        if company_logo.data:
            if "jpg" not in company_logo.data:
                if "jpeg" not in company_logo.data:
                    if "png" not in company_logo.data:
                        if "svg" not in company_logo.data:
                            if "tiff" not in company_logo.data:
                                raise ValidationError(
                                    'Please add a valid image URL.')


class CreateJobForm(JobForm):
    submit = SubmitField("Create job")


class UpdateJobForm(JobForm):
    submit = SubmitField("Update job")


class ApplicationForm(FlaskForm):
    notice_period = StringField(
        "Notice Period *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=3,
                max=20,
                message="Notice period must be between 3 and 20 characters long")])
    current_salary = StringField(
        "Current Salary *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=3,
                max=20,
                message="Salary must be between 3 and 20 characters long")])
    desired_salary = StringField(
        "Desired Salary *",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(
                min=3,
                max=20,
                message="Salary must be between 3 and 20 characters long")])
    resume = URLField("Resume URL *",
                      validators=[
                          InputRequired("Input is required!"),
                          DataRequired("Data is required!")
                      ])
    cover_letter = URLField("Cover Letter URL")
    submit = SubmitField("Apply")

    def validate_resume(self, resume):
        if resume.data:
            if "pdf" not in resume.data:
                if "jpg" not in resume.data:
                    if "jpeg" not in resume.data:
                        if "png" not in resume.data:
                            if "svg" not in resume.data:
                                if "tiff" not in resume.data:
                                    raise ValidationError(
                                        'Please add a valid image URL.')

    def validate_cover_letter(self, cover_letter):
        if cover_letter.data:
            if "pdf" not in cover_letter.data:
                if "jpg" not in cover_letter.data:
                    if "jpeg" not in cover_letter.data:
                        if "png" not in cover_letter.data:
                            if "svg" not in cover_letter.data:
                                if "tiff" not in cover_letter.data:
                                    raise ValidationError(
                                        'Please add a valid image URL.')
