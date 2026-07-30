import pyodbc
from pyodbc import Connection

CONN_STR: str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=CurriculumDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

def get_connection() -> Connection | None:
    try:
        return pyodbc.connect(CONN_STR)
    except Exception as e:
        print(f"ERROR: Couldn't connect to the database.")
        print(f"ERROR: {e}")

        return None

# Helper function for cleaning up variables fetched from the database.
def sanitize(var, add_quotes: bool = False, if_none = "N/A"):
    if var is None or var == "":
        return if_none
    elif add_quotes:
        return f"\"{str(var)}\""
    else:
        return var
