from database.connection import DataBase


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



