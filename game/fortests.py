from .models import Table


def free_table(request):
    """Return table (table as a thing, not row in db) with free spot or 'None'"""
    for table_obj in Table.objects.raw("""
        #SELECT * FROM game_table
        #WHERE Player1 IS NULL
        #OR Player2 IS NULL
        #OR Player3 IS NULL
        #OR Player4 IS NULL
        
        SELECT * FROM game_table

        """):
        return table_obj


print(free_table())
