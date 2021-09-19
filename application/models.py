from application import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


class Job():
    """
    Class representing a job post
    """

    def __init__(self, company, company_logo, position,
                 location, salary, level, stack, contract,
                 description, posted_by, email, date_posted):
        """
        Initialize job attributes
        """
        self.company = company
        self.company_logo = company_logo
        self.position = position
        self.location = location
        self.salary = salary
        self.level = level
        self.stack = stack
        self.contract = contract
        self.description = description
        self.posted_by = posted_by
        self.email = email
        self.date_posted = date_posted

    def __repr__(self):
        return '<Job %r>' % self.position

    def get_job_info(self):
        """
        Creates dictionary with the job information
        """
        info = {"company": self.company,
                "company_logo": self.company_logo,
                "position": self.position,
                "location": self.location,
                "salary": self.salary,
                "level": self.level,
                "stack": self.stack,
                "contract": self.contract,
                "description": self.description,
                "posted_by": self.posted_by,
                "email": self.email,
                "date_posted": self.date_posted}
        return info

    def insert_into_database(self):
        """
        Add a job in MongoDB
        """
        mongo.db.jobs.insert_one(self.get_job_info())

    @staticmethod
    def find_all_jobs():
        """
        Find and return all jobs in MongoDB
        """
        jobs = list(mongo.db.jobs.find())
        return jobs

    @staticmethod
    def find_applied_jobs(username):
        """
        Find and return jobs that a user has applied to in MongoDB
        """
        applications = list(mongo.db.applications.find())
        jobs = list(mongo.db.jobs.find())
        applied_jobs = []
        for application in applications:
            if application["applicant"] == username:
                for job in jobs:
                    if str(job["_id"]) == str(application["job_id"]):
                        applied_jobs.append(job)
        return applied_jobs

    @staticmethod
    def find_posted_jobs(username):
        """
        Find and return jobs that a user has posted in MongoDB
        """
        jobs = list(mongo.db.jobs.find())
        posted_jobs = []
        for job in jobs:
            if username == job["posted_by"]:
                posted_jobs.append(job)
        return posted_jobs

    @staticmethod
    def find_job_by_id(job_id):
        """
        Find and return a job in MongoDB by its id
        """
        job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)})
        return job

    @staticmethod
    def filter_jobs(query):
        """
        Search index for events in MongoDB by query
        """
        jobs = list(mongo.db.jobs.find({"$text": {"$search": query}}))
        return jobs

    @staticmethod
    def edit_job(job_id, info):
        """
        Update a job in MongoDB
        """
        mongo.db.jobs.update_one({"_id": ObjectId(job_id)},
                                 {"$set": info})

    @staticmethod
    def delete_job(job_id):
        """
        Delete a job in MongoDB
        """
        mongo.db.jobs.remove({"_id": ObjectId(job_id)})


class Application():
    """
    Class representing a job application
    """

    def __init__(self, notice_period, current_salary, desired_salary,
                 resume, cover_letter, job_id, applicant, email, date_applied):
        """
        Initialize application attributes
        """
        self.notice_period = notice_period
        self.current_salary = current_salary
        self.desired_salary = desired_salary
        self.resume = resume
        self.cover_letter = cover_letter
        self.job_id = job_id
        self.applicant = applicant
        self.email = email
        self.date_applied = date_applied

    def get_application_info(self):
        """
        Creates dictionary with the application information
        """
        info = {"notice_period": self.notice_period,
                "current_salary": self.current_salary,
                "desired_salary": self.desired_salary,
                "resume": self.resume,
                "cover_letter": self.cover_letter,
                "job_id": self.job_id,
                "applicant": self.applicant,
                "email": self.email,
                "date_applied": self.date_applied}
        return info

    def insert_into_database(self):
        """
        Add the application in MongoDB
        """
        mongo.db.applications.insert_one(self.get_application_info())

    @staticmethod
    def find_all_applications():
        """
        Find and return all applications in MongoDB
        """
        applications = list(mongo.db.applications.find())
        return applications

    @staticmethod
    def find_applications_by_job(job_id):
        """
        Find and return all applicants for a job in MongoDB
        """
        all_applications = list(mongo.db.applications.find())
        applications = []
        for application in all_applications:
            if str(application["job_id"]) == str(job_id):
                applications.append(application)
        return applications


class User():
    """
    Class representing a user
    """

    def __init__(self, username, email, password, location, role, picture):
        """
        Initialize user attributes
        """
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.location = location
        self.role = role
        self.picture = picture

    def __repr__(self):
        return '<User %r>' % self.username

    def get_user_info(self):
        """
        Creates dictionary with the user information
        """
        info = {"username": self.username,
                "email": self.email,
                "password": self.password,
                "location": self.location,
                "role": self.role,
                "picture": self.picture}
        return info

    def insert_into_database(self):
        """
        Add a user in MongoDB
        """
        mongo.db.users.insert_one(self.get_user_info())

    @staticmethod
    def find_user_by_username(username):
        """
        Find and return a user in MongoDB by their username
        """
        user = mongo.db.users.find_one({"username": username})
        return user

    @staticmethod
    def find_user_by_email(email):
        """
        Find and return a user in MongoDB by their email
        """
        user = mongo.db.users.find_one({"email": email})
        return user

    @staticmethod
    def find_all_users():
        """
        Find and return all users in MongoDB
        """
        users = list(mongo.db.users.find())
        return users

    @staticmethod
    def edit_user(_id, info):
        """
        Update a user in MongoDB
        """
        mongo.db.users.update_one({"_id": ObjectId(_id)},
                                  {"$set": info})

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user in MongoDB
        """
        mongo.db.users.remove({"_id": ObjectId(user_id)})
