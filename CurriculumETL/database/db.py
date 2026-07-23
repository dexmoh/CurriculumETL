import pyodbc

def get_connection() -> pyodbc.Connection:
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=CurriculumDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)

# Helper function for cleaning up variables fetched from the database.
def sanitize(var, add_quotes: bool = False, if_none = "N/A"):
    if var is None or var == "":
        return if_none
    elif add_quotes:
        return f"\"{str(var)}\""
    else:
        return var
