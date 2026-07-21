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
