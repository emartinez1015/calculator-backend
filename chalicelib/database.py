import os
from peewee import PostgresqlDatabase

class DatabaseConnection:
    def __init__(self):
        POSTGRES_HOST = os.environ['POSTGRES_HOST']
        POSTGRES_PORT = os.environ['POSTGRES_PORT']
        POSTGRES_DB = os.environ['POSTGRES_DB']
        POSTGRES_USER = os.environ['POSTGRES_USER']
        POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
        self.database = PostgresqlDatabase(
            POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        
        self.database.connect()
    
    def get_connection(self):
        return self.database
