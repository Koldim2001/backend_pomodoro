from settings import Settings
import psycopg2

settings = Settings()


class DataBase:

    def __init__(self):
        # Параметры подключения к базе данных
        conn_params = {
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME,
        }

        # Подключение к базе данных
        try:
            self.connection = psycopg2.connect(**conn_params)
            print("Connected to PostgreSQL")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        # Создание курсора для выполнения SQL-запросов
        self.cursor = self.connection.cursor()

    def drop_table(self, table_name):
        self.table_name = table_name
        # SQL-запрос для удаления таблицы, если она уже существует
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"

        # Удаление таблицы, если она уже существует
        try:
            self.cursor.execute(drop_table_query)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при удалении бд")

    def create_table_tasks(self, table_name):
        # SQL-запрос для создания таблицы
        create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            pomodoro_count INTEGER,
            category_id INTEGER,
            user_id INTEGER
        );
        """

        # Создание таблицы
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully")
        except (Exception, psycopg2.Error) as error:
            print(f"Error while creating table: {error}")

    def create_table_users(self, table_name):
        # SQL-запрос для создания таблицы
        create_table_query = f"""
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            username VARCHAR,
            password VARCHAR
        );
        """

        # Создание таблицы
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully")
        except (Exception, psycopg2.Error) as error:
            print(f"Error while creating table: {error}")
