from application import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User():
    """
    Class representing a user
    """
    
    def __init__(self, username="", email="", password="", location="", experience="", _id=None):
        """
        initialize user attributes
        """
        self._id              = _id
        self.username         = username
        self.email            = email
        self.password         = generate_password_hash(password)
        self.location         = location
        self.experience       = experience

    def __repr__(self):
        return '<User %r>' % self.username


    def get_user_info(self):
        info = {"username": self.username.lower(),
                "email": self.email.lower(),
                "password": self.password,
                "location": self.location,
                "experience": self.experience}
        return info

    
    def insert_into_database(self):
        """
        Add a user in the database
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
    def get_user_id(email):
        """
        Return a user Id in MongoDB using the user's email
        """
        user_id = mongo.db.users.find_one({"email": email.lower()})["_id"]
        return user_id


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

