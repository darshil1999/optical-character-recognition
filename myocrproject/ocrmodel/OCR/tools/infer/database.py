import mysql.connector
import json
from config.config import hostname, username, password, database

mydb = mysql.connector.connect(
  host=hostname,
  user=username,
  password=password,
  database=database
)
mycursor = mydb.cursor()


def save(file_id,data):

    query = """INSERT INTO file_row_data (file_id,data) VALUES (%s, %s)"""
    values = (file_id, data)

    mycursor.execute(query, values)
    mydb.commit()

    if mycursor.rowcount == 1:
        print(f"JSON is saved in database for File - {file_id}.")
    else:
        print(f"There seems to be an issue in saving the JSON of File - {file_id}.")
    return mycursor.rowcount


def update_status(file_id,status):
    
    query = """UPDATE file_management SET status=(%s) WHERE id=(%s)"""
    values = (status, file_id)

    mycursor.execute(query, values)
    mydb.commit()

    # print(mycursor.rowcount, "record updated.")
    if mycursor.rowcount == 1:
        print(f"Status is updated for File - {file_id}.")
    else:
        print(f"There seems to be an issue in updating the status of File - {file_id}.")

    return mycursor.rowcount
