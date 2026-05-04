from enums.value_permissions import ValuePermission
from persistence.db import get_connection
import pymysql


class Permission():
    def __init__(self, id: int, value: ValuePermission):
        self.id= id
        self.value = value

    @staticmethod
    def get_by_user(id_user : int):
            try:
                connection = get_connection()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                sql = "SELECT id, value FROM permission WHERE id_user = %s"
                cursor.execute(sql, (id_user,))

                rs = cursor.fetchall()
                
                cursor.close()
                connection.close()
                permissions = []

                for r in rs:
                    permissions.append(
                        Permission(id=r['id'], value=ValuePermission(r['value']))
                )            
                return permissions
            except Exception as ex:
                print(f"Error getting permission:{ex}")
                return False
        
    @staticmethod
    def add_permission(id_user: int, permission_value: int):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            sql_check = "SELECT id FROM permission WHERE id_user = %s AND value = %s"
            cursor.execute(sql_check, (id_user, permission_value))
            
            if cursor.fetchone():
                print("El usuario ya cuenta con este permiso.")
                return False

            sql_insert = "INSERT INTO permission (id_user, value) VALUES (%s, %s)"
            cursor.execute(sql_insert, (id_user, permission_value))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error al agregar permiso: {ex}")
            return False