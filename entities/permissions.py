from enums.value_permissions import ValuePermission
from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_login import UserMixin
from enums.profiles import Profile


class Permission():
    def __init__(self, id: int, value: ValuePermission):
        self.id= id
        self.value = value

    def get_by_user(id_user):
            try:
                connection = get_connection()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                sql = "SELECT id, value FROM user WHERE id_user = %s"
                cursor.execute(sql, (id_user,))

                permission = cursor.fetchall()
                
                cursor.close()
                connection.close()
                permissions = []

                for r in rs:
                    r
                    permissions.append(Permission(r["value"]))

                

                return None
            except Exception as ex:
                print(f"Error getting permission:{ex}")
                return False
        