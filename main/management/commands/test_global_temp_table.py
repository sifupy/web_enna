from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Test global temporary tables'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE #test (id INT, name VARCHAR(50))")
            cursor.execute("INSERT INTO #test VALUES (1, 'John Doe')")
            cursor.execute("SELECT * FROM #test")
            results = cursor.fetchall()
            print("Results:", results)
