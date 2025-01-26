import pyodbc

from django.core.management import BaseCommand
from config.settings import DATABASE, USER, PASSWORD, HOST


class Command(BaseCommand):
    def handle(self, *args, **options):
        ConnectionString = f'''DRIVER={{ODBC Driver 18 for SQL Server}};
                               SERVER={HOST};
                               DATABASE=DjangoDB;
                               UID={USER};
                               PWD={PASSWORD}'''
        try:
            conn = pyodbc.connect(ConnectionString)
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            conn.autocommit = True
            try:
                conn.execute(fr"CREATE DATABASE {DATABASE}")
            except pyodbc.ProgrammingError as ex:
                print(ex)
            else:
                print(f"База данных {DATABASE} успешно создана")

# def handle(self, *args, **options):
#     ConnectionString = f'''DRIVER={{SQL Server}};
#                                    SERVER={HOST};
#                                    DATABASE={DATABASE};
#                                    UID={USER};
#                                    PWD={PASSWORD}'''
#     conn = pyodbc.connect(ConnectionString)
#     try:
#
#         conn.autocommit = True
#         conn.execute(fr"CREATE DATABASE Shelter320;")
#
#     except pyodbc.ProgrammingError as ex:
#         print(ex)
#     else:
#         print("База данных Shelter320 успешно создана")
#     finally:
#         conn.close().
