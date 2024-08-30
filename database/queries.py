from database.connection import DataBase


class SQLQueries():
    
    def __init__(self, table_name, drop_table=True):
        self.database = DataBase()

        if drop_table:
            self.database.drop_table(table_name)

        self.database.create_table(table_name)



