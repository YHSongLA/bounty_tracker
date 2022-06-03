from operator import methodcaller
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint

DATABASE = 'bounty_tracker'

class Bounty:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.status = data['status']
        self.priority = data['priority']
        if 'first_name' in data:
            self.user = data['first_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO bounties (title,description,status,priority, user_id) VALUES (%(title)s,%(description)s,%(status)s,%(priority)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    @classmethod
    def ascending(cls, data:dict) -> int:
        query = "SELECT * FROM bounties ORDER BY status ASC;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def descending(cls, data:dict) -> int:
        query = "SELECT * FROM bounties ORDER BY status DESC;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM bounties;"
        results = connectToMySQL(DATABASE).query_db(query)
        bounties = []
        for u in results:
            bounties.append( cls(u) )
        return bounties

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_users(cls) -> list:
        query = "SELECT * FROM bounties JOIN users ON bounties.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        # pprint(results)
        bounties = []
        for u in results:
            bounties.append( cls(u) )
        return bounties
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM bounties WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_one_with_user(cls,data:dict) -> object:
        query  = "SELECT * FROM bounties LEFT JOIN users ON bounties.user_id = users.id  WHERE bounties.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE bounties SET title=%(title)s,description=%(description)s,status=%(status)s,priority=%(priority)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM bounties WHERE id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def search_form(cls, data):
        query = "SELECT * FROM bounties JOIN users ON bounties.user_id = users.id WHERE title LIKE %(title)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        if not result:
            return False
        return result

    @staticmethod
    def add_bounty(bounty:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(bounty['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False
        if len(bounty['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        # if not len(bounty['status']) > 0:
        #     flash("Status must be greater than 0 characters.")
        #     is_valid = False
        # if not len(bounty['priority']) > 0:
        #     flash("Priority must be greater than 0 characters.")
        #     is_valid = False
        return is_valid