import mysql.connector
from datetime import date, timedelta

# =========================
# DATABASE CONNECTION
# =========================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE",
    database="mydb"
)

cursor = connection.cursor()


# =========================
# REGISTER PERSON
# =========================

def register_person():
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")

    sql = """
    INSERT INTO pessoa (Nome, Sobrenome)
    VALUES (%s, %s)
    """

    values = (first_name, last_name)

    cursor.execute(sql, values)
    connection.commit()

    print("Person registered successfully!")


# =========================
# LIST PEOPLE
# =========================

def list_people():
    cursor.execute("SELECT * FROM pessoa")

    results = cursor.fetchall()

    if len(results) == 0:
        print("No people registered.")
        return

    for row in results:
        print(row)


# =========================
# REGISTER LICENSE
# =========================

def register_license():
    list_people()

    person_id = int(input("Enter the person ID: "))
    number = input("Enter the license number: ")
    expiration = input("Enter the expiration date (YYYY-MM-DD): ")

    sql = """
    INSERT INTO habilitacao
    (Num_Habilitacao, Validade, Pessoa_Id_pessoa)
    VALUES (%s, %s, %s)
    """

    values = (number, expiration, person_id)

    cursor.execute(sql, values)
    connection.commit()

    print("License registered successfully!")


# =========================
# LIST PEOPLE + LICENSES
# =========================

def list_people_with_licenses():
    sql = """
    SELECT
        pessoa.Id_pessoa,
        pessoa.Nome,
        pessoa.Sobrenome,
        habilitacao.Num_Habilitacao,
        habilitacao.Validade
    FROM pessoa
    LEFT JOIN habilitacao
    ON pessoa.Id_pessoa = habilitacao.Pessoa_Id_pessoa
    """

    cursor.execute(sql)

    results = cursor.fetchall()

    for row in results:
        print(row)


# =========================
# SEARCH PERSON
# =========================

def search_person():
    name = input("Enter the person's name: ")

    sql = """
    SELECT
        pessoa.Id_pessoa,
        pessoa.Nome,
        pessoa.Sobrenome,
        habilitacao.Num_Habilitacao,
        habilitacao.Validade
    FROM pessoa
    LEFT JOIN habilitacao
    ON pessoa.Id_pessoa = habilitacao.Pessoa_Id_pessoa
    WHERE pessoa.Nome LIKE %s
    """

    cursor.execute(sql, ("%" + name + "%",))

    results = cursor.fetchall()

    if len(results) == 0:
        print("Person not found.")
        return

    for row in results:
        print(row)

        expiration = row[4]

        if expiration is not None:
            if expiration < date.today():
                print("LICENSE EXPIRED")
            else:
                print("LICENSE VALID")


# =========================
# EDIT PERSON
# =========================

def edit_person():
    list_people()

    person_id = int(input("Enter the person ID: "))

    new_first_name = input("Enter the new first name: ")
    new_last_name = input("Enter the new last name: ")

    sql = """
    UPDATE pessoa
    SET Nome = %s, Sobrenome = %s
    WHERE Id_pessoa = %s
    """

    values = (new_first_name, new_last_name, person_id)

    cursor.execute(sql, values)
    connection.commit()

    print("Person updated successfully!")


# =========================
# DELETE PERSON
# =========================

def delete_person():
    list_people()

    person_id = int(input("Enter the ID of the person to delete: "))

    # first delete the linked licenses
    cursor.execute(
        "DELETE FROM habilitacao WHERE Pessoa_Id_pessoa = %s",
        (person_id,)
    )

    # then delete the person
    cursor.execute(
        "DELETE FROM pessoa WHERE Id_pessoa = %s",
        (person_id,)
    )

    connection.commit()

    print("Person deleted successfully!")


# =========================
# EDIT LICENSE
# =========================

def edit_license():
    number = input("Enter the license number to edit: ")

    new_expiration = input("Enter the new expiration date (YYYY-MM-DD): ")

    sql = """
    UPDATE habilitacao
    SET Validade = %s
    WHERE Num_Habilitacao = %s
    """

    values = (new_expiration, number)

    cursor.execute(sql, values)
    connection.commit()

    print("License updated successfully!")


# =========================
# DELETE LICENSE
# =========================

def delete_license():
    number = input("Enter the license number: ")

    sql = """
    DELETE FROM habilitacao
    WHERE Num_Habilitacao = %s
    """

    cursor.execute(sql, (number,))
    connection.commit()

    print("License deleted successfully!")


# =========================
# EXPIRATION ALERT
# =========================

def check_expirations():
    today = date.today()
    limit = today + timedelta(days=30)

    sql = """
    SELECT
        pessoa.Nome,
        pessoa.Sobrenome,
        habilitacao.Num_Habilitacao,
        habilitacao.Validade
    FROM pessoa
    JOIN habilitacao
    ON pessoa.Id_pessoa = habilitacao.Pessoa_Id_pessoa
    WHERE habilitacao.Validade BETWEEN %s AND %s
    """

    cursor.execute(sql, (today, limit))

    results = cursor.fetchall()

    if len(results) == 0:
        print("No licenses expiring in the next 30 days.")
        return

    print("\nLicenses expiring within 30 days:")

    for row in results:
        print(row)


# =========================
# MENU
# =========================

while True:
    print("\n===== DRIVER'S LICENSE MANAGEMENT SYSTEM =====")

    print("1 - Register person")
    print("2 - List people")
    print("3 - Register license")
    print("4 - List people and licenses")
    print("5 - Search person")
    print("6 - Edit person")
    print("7 - Delete person")
    print("8 - Edit license")
    print("9 - Delete license")
    print("10 - Check expiring licenses")
    print("0 - Exit")

    option = input("Choose an option: ")

    if option == "1":
        register_person()

    elif option == "2":
        list_people()

    elif option == "3":
        register_license()

    elif option == "4":
        list_people_with_licenses()

    elif option == "5":
        search_person()

    elif option == "6":
        edit_person()

    elif option == "7":
        delete_person()

    elif option == "8":
        edit_license()

    elif option == "9":
        delete_license()

    elif option == "10":
        check_expirations()

    elif option == "0":
        print("Closing system...")
        break

    else:
        print("Invalid option!")


cursor.close()
connection.close()
