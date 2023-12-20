from datetime import datetime
import os

class User:
    new_id = 1
    def __init__(self,username, password):
        self.username = username
        self.password = password
        self.user_id = User.new_id
        self.role = "user"
        new_id += 1



        
