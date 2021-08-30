from application import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


class Contact():
    """
    Class representing a job post
    """

    def __init__(self, name, email, description):
        self.name          = name
        self.email         = email
        self.description   = description


    def get_contact_info(self):
        info = {"name"     : self.name.lower(),
                "email"    : self.email.lower(),
                "password" : self.description}
        return info


    def insert_into_database(self):
        """
        Add a user in the database
        """
        mongo.db.contact.insert_one(self.get_contact_info())


class Job():
    """
    Class representing a job post
    """

    def __init__(self, company, position, description, salary, 
                location, contract, level, employer_id):
        self.company       = company
        self.position      = position
        self.description   = description
        self.salary        = salary
        self.location      = location
        self.contract      = contract
        self.level         = level
        self.employer_id   = employer_id
    

    def __repr__(self):
        return '<Job %r>' % self.position


    def get_job_info(self):
        info = {"username"    : self.company.lower(),
                "email"       : self.position.lower(),
                "password"    : self.description,
                "salary"      : self.salary,
                "location"    : self.location,
                "contract"    : self.contract,
                "level"       : self.level,
                "employer_id" : self.employer_id}
        return info

    
    def insert_into_database(self):
        """
        Add a user in the database
        """
        mongo.db.jobs.insert_one(self.get_job_info())


    @staticmethod
    def find_all_jobs():
        """
        Find and return all users in MongoDB
        """
        jobs = list(mongo.db.jobs.find())
        return jobs


class User():
    """
    Class representing a user
    """
    
    def __init__(self, username, email, password, location, role):
        """
        initialize user attributes
        """
        self.username      = username
        self.email         = email
        self.password      = generate_password_hash(password)
        self.location      = location
        self.role          = role

    def __repr__(self):
        return '<User %r>' % self.username


    def get_user_info(self):
        info = {"username" : self.username.lower(),
                "email"    : self.email.lower(),
                "password" : self.password,
                "location" : self.location,
                "role"     : self.role}
        return info

    
    def insert_into_database(self):
        """
        Add a user in the database
        """
        mongo.db.users.insert_one(self.get_user_info())


    def is_authenticated(self):
        return not "" == self.username


    def is_anonymous(self):
        return "" == self.username


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
    def get_user_id(email):
        """
        Return a user Id in MongoDB using the user's email
        """
        user_id = mongo.db.users.find_one({"email": email.lower()})["_id"]
        return user_id


    @staticmethod
    def get_user_role(email):
        """
        Return a user Id in MongoDB using the user's email
        """
        user_role = mongo.db.users.find_one({"email": email.lower()})["role"]
        return user_role


    @staticmethod
    def find_user_by_id(user_id):
        """
        Find and return a user in MongoDB by their id
        """
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return user


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
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})


