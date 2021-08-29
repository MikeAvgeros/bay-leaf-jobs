from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, DecimalField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length


class JobForm(FlaskForm):
    company		= StringField("Company *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=5, max=50, message="Company must be between 5 and 50 characters long")
								])
    position		= StringField("Position *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=5, max=50, message="Position must be between 5 and 50 characters long")
								])
    description = TextAreaField("Description *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=10, max=200, message="Description must be between 10 and 200 characters long")
								])
    salary		= DecimalField("Salary *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!")
								])
    location	= StringField("Location *",
								validators=[
									InputRequired("Input is required!"),
									DataRequired("Data is required!"),
									Length(min=3, max=40, message="Location must be between 3 and 40 characters long")
								])
    contract	= SelectField("",
								choices=[
									("Full Time", "Full Time"), 
									("Part Time", "Part Time"), 
									("Freelance", "Freelance")])
    level		= SelectField("",
								choices=[
									("Senior", "Senior"), 
									("Midweight", "Midweigth"), 
									("Associate", "Associate")])


class CreateJobForm(JobForm):
	submit 		= SubmitField("Create job")


class UpdateJobForm(JobForm):
	submit 		= SubmitField("Update job")


class DeleteJob(JobForm):
	submit 		= SubmitField("Delete job")
