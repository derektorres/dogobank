from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_login import UserMixin
from enums.profiles import Profile
from entities.permissions import Permission
from enums.profiles import Profile
from enums.value_permissions import ValuePermission
from entities.account import Account


class User (UserMixin):
    def __init__(self, id: int, name:str, email:str, password:str, profile: Profile, permission: list, is_active: bool):
        self.id= id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.permission = permission
        self._is_active = is_active
        
    @property
    def is_active(self):
        """Sobrescribe la propiedad de UserMixin para usar el valor de la DB"""
        return bool(self._is_active)
    
    
    def check_email_exists(email) -> bool:
        """
            Verifica si la cuenta de correo electrónico ya se encuentra registrada.

            Parameters:
                email (str): Correo electrónico a validar.

            Returns:
                bool: True si el correo ya se encunetra registrado; de lo contrario, False.
        """
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email from user WHERE email = %s"
        cursor.execute(sql, (email,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None
    
    @staticmethod   
    def save(name: str, email:str, password:str):
        """
            Guarda un registro de usuario en la base de datos

            Parameters:
                name (str): Nombre del usuario.
                email (str): Correo electrónico del usuario.
                password (str): Contraseña del usuario en texto plano.

            Returns:
                bool: True si la cuenta se guardó correctamente; de lo contrario, False.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor()
            hash_password = generate_password_hash(password)

            sql = """
                INSERT INTO user (name, email, password, profile, is_active) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, hash_password, 2, 1))
            nuevo_id = cursor.lastrowid 
            sql_perm = "INSERT INTO permission (id_user, value) VALUES (%s, %s)"
            cursor.execute(sql_perm, (nuevo_id, 4)) 

            Account.create_account(cursor, nuevo_id)

            connection.commit()

            cursor.close()
            connection.close()
            return nuevo_id
        except Exception as ex:
            print(f"Error saving user:{ex}")
            return False
        
    @staticmethod
    def check_login(email, password):
        try:
            connection = get_connection()
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT id, name, email, password, profile, is_active FROM user WHERE email = %s"
                cursor.execute(sql, (email,))
                user_data = cursor.fetchone()

            if user_data and check_password_hash(user_data["password"], password):
                permissions = Permission.get_by_user(user_data["id"])
                
                return User(
                    user_data["id"],
                    user_data["name"],
                    user_data["email"],
                    user_data["password"],
                    Profile(user_data["profile"]), 
                    permissions,
                    bool(user_data["is_active"])
                )

            return None
        except Exception as ex:
            print(f"Error login user:{ex}")
            return False
        
    def get_by_id(id):
            try:
                connection = get_connection()
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                
                sql = "SELECT id, name, email, password, profile, is_active FROM user WHERE id = %s"
                cursor.execute(sql, (id,))

                user = cursor.fetchone()
                
                cursor.close()
                connection.close()

                if user:
                    permissions = Permission.get_by_user(user["id"])

                    return User(
                        user["id"],
                        user["name"],
                        user["email"],
                        user["password"],
                        user["profile"],
                        permissions,
                        user["is_active"]
                    )

                return None
            except Exception as ex:
                print(f"Error login user:{ex}")
                return False
    
          
    