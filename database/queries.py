from database.connection import DataBase
from Crypto.Hash import SHA256
import os
import random
import string


class SQLQueriesTasks():
    
    def __init__(self, table_name, drop_table=True):
        self.database = DataBase()
        self.table_name = table_name
        self.cursor = self.database.cursor
        self.connection = self.database.connection

        if drop_table:
            self.database.drop_table(self.table_name)

        self.database.create_table_tasks(self.table_name)

    def create_new_row(self, name, pomodoro_count, category_id):
        query = "INSERT INTO {table_name} (name, pomodoro_count, category_id) VALUES (%s, %s, %s) RETURNING id"
        self.cursor.execute(query.format(table_name=self.table_name), (name, pomodoro_count, category_id))
        self.connection.commit()
        new_row_id = self.cursor.fetchone()[0]
        return new_row_id

    def update_task_name(self, task_id, new_name):
        query = "UPDATE {table_name} SET name = %s WHERE id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (new_name, task_id))
        self.connection.commit()
        query = "SELECT * FROM {table_name} WHERE id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (task_id,))
        rows = self.cursor.fetchall()
        return rows

    def delete_row_by_id(self, task_id):
        query = "DELETE FROM {table_name} WHERE id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (task_id,))
        deleted_count = self.cursor.rowcount
        self.connection.commit()
        return deleted_count > 0

    def select_all_rows(self):
        query = "SELECT * FROM {table_name}"
        self.cursor.execute(query.format(table_name=self.table_name))
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.cursor.close()
        self.connection.close()


class SQLQueriesUsers():
    
    def __init__(self, table_name, drop_table=True):
        self.database = DataBase()
        self.table_name = table_name
        self.cursor = self.database.cursor
        self.connection = self.database.connection

        if drop_table:
            self.database.drop_table(self.table_name)

        self.database.create_table_users(self.table_name)

    def create_new_user(self, username, password):
        password_hash = self.get_hash(password)
        access_token = self.generate_access_token()

        query = "INSERT INTO {table_name} (username, password, access_token) VALUES (%s, %s, %s) RETURNING id"
        self.cursor.execute(query.format(table_name=self.table_name), (username, password_hash, access_token))
        self.connection.commit()
        new_row_id = self.cursor.fetchone()[0]
        return new_row_id, access_token
    
    def check_user(self, username, password):
        # Получаем хэш пароля
        password_hash = self.get_hash(password)

        # Проверяем наличие пользователя в базе данных
        query = "SELECT id, password, access_token FROM {table_name} WHERE username = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (username,))
        user_data = self.cursor.fetchone()

        if user_data is None:
            # Пользователь не найден
            return "Пользователь не найден"
        else:
            user_id, stored_password_hash, access_token = user_data
            if password_hash != stored_password_hash:
                # Пароль неверный
                return "Неверный пароль"
            else:
                # Пароль верный, возвращаем id и access_token
                return user_id, access_token

    @staticmethod
    def get_hash(input_string):
        # Создаем объект хэша SHA-256
        sha256_hash = SHA256.new()
        
        # Обновляем хэш с использованием байтового представления строки
        sha256_hash.update(input_string.encode('utf-8'))
        
        # Возвращаем хэш в виде шестнадцатеричной строки
        return sha256_hash.hexdigest()
    
    @staticmethod
    def generate_access_token():
        # Определяем символы, которые могут быть использованы в токене
        characters = string.ascii_letters + string.digits + string.punctuation
        
        # Генерируем случайное начальное число (seed) на основе системного времени
        random.seed(os.urandom(32))
        
        # Генерируем 10-символьный токен
        token = ''.join(random.choice(characters) for _ in range(10))
        
        return token

    def close(self):
        self.cursor.close()
        self.connection.close()


