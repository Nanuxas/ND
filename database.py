import sqlite3


class DatabaseContextManager(object):

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


def create_employee_table():
    query = """CREATE TABLE Employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                role TEXT,
                annual_salary FLOAT,
                feedback INTEGER,
                years_employed INTEGER,
                email TEXT)"""
    with DatabaseContextManager("employees") as db:
        db.execute(query)


def create_employee(first_name: str, last_name: str, role: str, annual_salary: float, feedback: int, years_employed:int, email: str) -> object:
    query = f"""INSERT INTO Employees(first_name, last_name, role, annual_salary, feedback, years_employed, email) 
                VALUES('{first_name}','{last_name}','{role}',{annual_salary},'{feedback}','{years_employed}', '{email}')"""
    with DatabaseContextManager("employees") as db:
        db.execute(query)


def get_employees():
    query = f"SELECT * FROM Employees"
    with DatabaseContextManager("employees") as db:
        data = db.execute(query)
        for record in data:
            print(record)


def delete_employee(email: str):
    query = f"DELETE FROM Employees WHERE email = '{email}'"
    with DatabaseContextManager("employees") as db:
        db.execute(query)

def check_if_employee_exists(email: str):
    query = f"SELECT * FROM Employees WHERE email = '{email}'"
    with DatabaseContextManager("employees") as db:
        db.execute(query)
        employee = db.fetchone()
    if employee == None:
        return False
    return True