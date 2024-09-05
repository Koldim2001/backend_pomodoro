from database.connection import DataBase
from Crypto.Hash import SHA256
from utils.jwt import JWTUtils


class SQLQueriesTasks:

    def __init__(self, table_name, drop_table=True):
        self.database = DataBase()
        self.table_name = table_name
        self.cursor = self.database.cursor
        self.connection = self.database.connection

        if drop_table:
            self.database.drop_table(self.table_name)

        self.database.create_table_tasks(self.table_name)

    def create_new_row(self, name, pomodoro_count, category_id, user_id):
        query = "INSERT INTO {table_name} (name, pomodoro_count, category_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id"
        self.cursor.execute(
            query.format(table_name=self.table_name), (name, pomodoro_count, category_id, user_id)
        )
        self.connection.commit()
        new_row_id = self.cursor.fetchone()[0]
        return new_row_id

    def update_task_name(self, task_id, new_name, user_id):
        query = "UPDATE {table_name} SET name = %s WHERE (id = %s and user_id = %s)"
        self.cursor.execute(query.format(table_name=self.table_name), (new_name, task_id, user_id))
        self.connection.commit()
        query = "SELECT * FROM {table_name} WHERE (id = %s and user_id = %s)"
        self.cursor.execute(query.format(table_name=self.table_name), (task_id, user_id))
        rows = self.cursor.fetchall()
        return rows

    def delete_row_by_id(self, task_id, user_id):
        query = "DELETE FROM {table_name} WHERE (id = %s and user_id = %s)"
        self.cursor.execute(query.format(table_name=self.table_name), (task_id, user_id))
        deleted_count = self.cursor.rowcount
        self.connection.commit()
        return deleted_count > 0

    def select_all_rows(self, user_id):
        query = "SELECT * FROM {table_name} WHERE user_id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (user_id,))
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        self.cursor.close()
        self.connection.close()


class SQLQueriesUsers:

    def __init__(self, table_name, drop_table=True):
        self.database = DataBase()
        self.table_name = table_name
        self.cursor = self.database.cursor
        self.connection = self.database.connection

        if drop_table:
            self.database.drop_table(self.table_name)

        self.database.create_table_users(self.table_name)

    def create_new_user(self, username, password):
        # Проверяем, существует ли уже пользователь с таким username
        query = "SELECT id FROM {table_name} WHERE username = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (username,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            # Пользователь с таким username уже существует
            return "Пользователь с таким именем уже существует"

        # Получаем хэш пароля и генерируем access_token
        password_hash = self.get_hash(password)

        # Вставляем нового пользователя в базу данных
        query = "INSERT INTO {table_name} (username, password) VALUES (%s, %s) RETURNING id"
        self.cursor.execute(query.format(table_name=self.table_name), (username, password_hash))
        self.connection.commit()
        new_row_id = self.cursor.fetchone()[0]

        access_token = JWTUtils.generate_access_token(user_id=new_row_id)

        return new_row_id, access_token

    def check_user(self, username, password):
        # Получаем хэш пароля
        password_hash = self.get_hash(password)

        # Проверяем наличие пользователя в базе данных
        query = "SELECT id, password FROM {table_name} WHERE username = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (username,))
        user_data = self.cursor.fetchone()

        if user_data is None:
            # Пользователь не найден
            return "Пользователь не найден"
        else:
            user_id, stored_password_hash = user_data
            if password_hash != stored_password_hash:
                # Пароль неверный
                return "Неверный пароль"
            else:
                # Пароль верный, возвращаем id и access_token
                access_token = JWTUtils.generate_access_token(user_id=user_id)
                return user_id, access_token

    def get_user_name(self, id):
        # Получаем имя пользователя по его id
        query = "SELECT username FROM {table_name} WHERE id = %s"
        self.cursor.execute(query.format(table_name=self.table_name), (id,))
        user_data = self.cursor.fetchone()
        if user_data is None:
            # Пользователь не найден
            return "Пользователь не найден"
        else:
            return user_data[0]

    @staticmethod
    def get_hash(input_string):
        # Создаем объект хэша SHA-256
        sha256_hash = SHA256.new()

        # Обновляем хэш с использованием байтового представления строки
        sha256_hash.update(input_string.encode("utf-8"))

        # Возвращаем хэш в виде шестнадцатеричной строки
        return sha256_hash.hexdigest()

    def close(self):
        self.cursor.close()
        self.connection.close()
