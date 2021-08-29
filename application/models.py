from application import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


class Job():
    """
    Class representing a user
    """

    def __init__(self, company, position, description, salary, location, contract, level):
        self.company       = company
        self.position      = position
        self.description   = description
        self.salary        = salary
        self.location      = location
        self.contract      = contract
        self.level         = level
    

    def __repr__(self):
        return '<Job %r>' % self.position


    def get_job_info(self):
        info = {"username": self.company.lower(),
                "email":    self.position.lower(),
                "password": self.description,
                "salary":   self.salary,
                "location": self.location,
                "contract": self.contract,
                "level":    self.level}
        return info

    
    def insert_into_database(self):
        """
        Add a user in the database
        """
        mongo.db.jobs.insert_one(self.get_job_info())


class User():
    """
    Class representing a user
    """
    
    def __init__(self, username, email, password, location, role, _id=None):
        """
        initialize user attributes
        """
        self._id              = _id
        self.username         = username
        self.email            = email
        self.password         = generate_password_hash(password)
        self.location         = location
        self.role             = role


    def __repr__(self):
        return '<User %r>' % self.username


    def get_user_info(self):
        info = {"username": self.username.lower(),
                "email"   : self.email.lower(),
                "password": self.password,
                "location": self.location,
                "role"    : self.role}
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
