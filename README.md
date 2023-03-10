
# Mathesis MOOCs - Advanced Programming in Python

The code in the `main.py` file, is a Python script that uses the sqlite3 module to store and manipulate data related to students' grades. It also includes a Student class to manage each student's information, including registration number, name, assignment grades, and exam grades.

The script reads data from two text files named "actresses.txt" and "actors.txt" and uses the names listed in these files to create a new cohort of students. The class size of the cohort is defined by the user, and the names are randomly assigned to the students.

After creating the new cohort, the script allows the user to add and modify the students' grades and calculate their final grades. It also provides functions to print out detailed records of the students' data and their final grades.

The script uses SQLite to persistently store the students' information in a database file named `students.sqlite.sql`, which is created if it does not exist. It also includes functions to create the necessary tables and indices in the database file if they are not already present.

