from datetime import datetime
from entities.user import User
from persistence.db import get_connection
import pymysql
from entities.transaction import Transaction

class Account():
    def __init__(self, id: int, creation_date: datetime, number: str, user: User, transaction:list):
        self.id = id
        self.creation_date = creation_date
        self.number = number
        self.user = user
        self.transaction = transaction


    def get_account_by_user(id_user: int):
            try:
                connection = get_connection()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                    
                sql = "SELECT id, number, creation_date, id_user FROM account WHERE id_user = %s"
                cursor.execute(sql, (id_user,))
                rs = cursor.fetchone()
                user_obj = User.get_by_id(rs["id_user"])
                transaction = Transaction.get_transaction_by_account(rs["id"])
                account = Account(
                     rs["id"],
                     rs["creation_date"],
                     rs["number"],
                     user_obj,
                     transaction
                )
                return account
            except Exception as ex:
                print(f"Error login user:{ex}")
                return False
            
    