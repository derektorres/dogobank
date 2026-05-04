from datetime import datetime
from entities import user
from enums import log_type
from persistence.db import get_connection
class Log:

    def __init__(self, id: int, date: datetime, user: user, description: str, type: log_type ):
        self.id = id
        self.date = date
        self.user = user
        self.description = description
        self.type = type

    @staticmethod
    def save_log(id_user: int, description: str, type: str):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            

            sql = "INSERT INTO log (id_user, description, type) VALUES (%s, %s, %s)" #
            cursor.execute(sql, (id_user, description, type)) 
            connection.commit() 

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving log:{ex}")
            return False
        
