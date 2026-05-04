from datetime import datetime
import pymysql
import random
from persistence.db import get_connection
from entities.transaction import Transaction

class Account():

    def __init__(self, id: int, creation_date: datetime, number: str, id_user: int, transaction: list):
        self.id = id
        self.creation_date = creation_date
        self.number = number
        self.id_user = id_user 
        self.transaction = transaction

    @staticmethod
    def get_account_by_user(id_user: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, number, creation_date, id_user FROM account WHERE id_user = %s"
            cursor.execute(sql, (id_user,))
            rs = cursor.fetchone()

            if rs is None:
                cursor.close()
                connection.close()
                return None
            
            transaction = Transaction.get_transaction_by_account(rs["id"])
            
            account = Account(
                 rs["id"],
                 rs["creation_date"],
                 rs["number"],
                 rs["id_user"], 
                 transaction
            )
            
            cursor.close()
            connection.close()
            return account
        except Exception as ex:
            print(f"Error retrieving account: {ex}")
            return False

    @staticmethod
    def create_account(cursor, id_user: int):
        numero_cuenta = "".join([str(random.randint(0, 9)) for _ in range(10)])
        fecha_ahora = datetime.now()
        sql = "INSERT INTO account (number, creation_date, id_user) VALUES (%s, %s, %s)"
        cursor.execute(sql, (numero_cuenta, fecha_ahora, id_user))