from application import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


class Job():
    """
    Class representing a job post
    """
    def __init__(self, company, position, description, 
                responsibilities, requirements, salary, location, 
                level, stack, contract, posted_by, email, date_posted):
        """
        Initialize job attributes
        """
        self.company           = company
        self.position          = position
        self.description       = description
        self.responsibilities  = responsibilities
        self.requirements      = requirements
        self.salary            = salary
        self.location          = location
        self.level             = level
        self.stack             = stack
        self.contract          = contract
        self.posted_by         = posted_by
        self.email             = email
        self.date_posted       = date_posted
    

    def __repr__(self):
        return '<Job %r>' % self.position


    def get_job_info(self):
        """
        Creates dictionary with the job information
        """
        info = {"company"          : self.company.lower(),
                "position"         : self.position.lower(),
                "description"      : self.description,
                "responsibilities" : self.responsibilities,
                "requirements"     : self.requirements,
                "salary"           : self.salary,
                "location"         : self.location,
                "level"            : self.level,
                "stack"            : self.stack,
                "contract"         : self.contract,
                "posted_by"        : self.posted_by,
                "email"            : self.email,
                "date_posted"      : self.date_posted}
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
        self.notice_period  = notice_period
        self.current_salary = current_salary
        self.desired_salary = desired_salary
        self.resume         = resume
        self.cover_letter   = cover_letter
        self.job_id         = job_id
        self.applicant      = applicant
        self.email          = email
        self.date_applied   = date_applied


    def get_application_info(self):
        """
        Creates dictionary with the application information
        """
        info = {"notice_period"  : self.notice_period,
                "current_salary" : self.current_salary,
                "desired_salary" : self.desired_salary,
                "resume"         : self.resume,
                "cover_letter"   : self.cover_letter,
                "job_id"         : self.job_id,
                "applicant"      : self.applicant,
                "email"          : self.email,
                "date_applied"   : self.date_applied}
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


class User():
    """
    Class representing a user 
    """
    
    def __init__(self, username, email, password, location, role):
        """
        Initialize user attributes
        """
        self.username      = username
        self.email         = email
        self.password      = generate_password_hash(password)
        self.location      = location
        self.role          = role

    def __repr__(self):
        return '<User %r>' % self.username


    def get_user_info(self):
        """
        Creates dictionary with the user information
        """
        info = {"username" : self.username.lower(),
                "email"    : self.email.lower(),
                "password" : self.password,
                "location" : self.location,
                "role"     : self.role}
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
