"""
Two companies just merged. Your task is to add company B into company A database.
The company B held their infromation in two files. company_employees and feedback_for_employees.
Their data was overlapping left and right:
company_employees had these fields (first_name, last_name, annual_salary, years_employed, email).
feedback_for_employees had (first_name, last_name, feedback, role, email).
Your main task is to comcatinate employees from 2 files into 1 record.
1.Use Employee class and class method to create new employee from a string.
2.Use context manager for database.
3.Lambda usage for filtering people with less than 3 years of work experience
4.Regular expressions usage for email check (can use staticmethod)
5.Serialization/Deserialization initial data is from json.

OUTPUT: Use already written get_employees method to show the comcatinated record
Collapse

"""

import json
import re
import database


class Employee:
    def __init__(self, first_name: str, last_name: str, role: str, annual_salary: float, feedback: int,
                 years_employed: int, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.annual_salary = annual_salary
        self.feedback = feedback
        self.years_employed = years_employed
        self.email = email

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.role},{self.annual_salary},{self.feedback},{self.years_employed}, {self.email}"

    @classmethod
    def create_from_string(cls, employee_string: str):
        first_name, last_name, role, annual_salary, feedback, years_employed, email = employee_string.split(",")
        annual_salary, feedback, years_employed = float(annual_salary), int(feedback), int(years_employed)
        if cls.validate_email(email):
            return cls(first_name, last_name, role, annual_salary, feedback, years_employed, email)

    @staticmethod
    def validate_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            return True
        return False


naujas_darbuotojas1 = Employee.create_from_string("bbbbbbbbbb,gerulis,CEO,4,5,2,labas@gmail.com")
print(naujas_darbuotojas1)

tikrina_ar_isdirbes_metus = lambda x: x > 3
if tikrina_ar_isdirbes_metus(naujas_darbuotojas1.years_employed):
    database.create_employee(naujas_darbuotojas1.first_name, naujas_darbuotojas1.last_name, naujas_darbuotojas1.role,
                             naujas_darbuotojas1.annual_salary, naujas_darbuotojas1.feedback,
                             naujas_darbuotojas1.years_employed, naujas_darbuotojas1.email)


with open("company_employees.json") as in_file:
    data_company_employees = json.load(in_file)

for i in data_company_employees["Employees"]:
    database.create_employee(i["firstName"], i["lastName"], 0, i["annual_salary"], 0,
                             i["years_employed"], i["emailAddress"])


with open("feedback_for_employees.json") as in_file:
    data_feedback = json.load(in_file)

for i in data_feedback["Feedback"]:
    database.create_employee(i["firstName"], i["lastName"], i["role"], 0, i["feedback"],
                             0, i["emailAddress"])

print("___")
database.get_employees()
