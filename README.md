# Driver's License Management System

A project built in Python with MySQL integration to practice database concepts and CRUD operations.

## Features

* Register people
* Register driver's licenses linked to a person
* List people
* List people with their driver's licenses
* Search people by name
* Check whether a license is valid or expired
* Edit people
* Delete people
* Edit driver's licenses
* Delete driver's licenses
* Alert for licenses expiring within 30 days

## Technologies

* Python
* MySQL
* MySQL Connector for Python

## Installation

Install the required dependency:

```bash
pip install mysql-connector-python
```

Then configure the database connection in the `main.py` file:

```python
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE",
    database="YOUR_DATABASE_HERE"
)
```

In the `password` field, enter your MySQL password.

In the `database` field, enter the name of the database you want to use.

Do not publish your real password on GitHub.

## Database

The `database.sql` file contains the commands needed to create the tables used by the system.

## Running

After setting up the database and installing MySQL Connector, run:

```bash
python main.py
```

The system runs in the terminal and uses user input through `input()`.
