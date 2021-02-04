import mysql.connector
from mysql.connector import Error

try:
	connection = mysql.connector.connect(host="localhost",user="newuser1",password="1234",database="activitytracker")

	sql_select_Query = "select * from tb_tracker1"

	cursor = connection.cursor()
	cursor.execute(sql_select_Query)
	records = cursor.fetchall()
	print("Total number of rows in tb_tracker1 is: ", cursor.rowcount)
	for row in records:
		print("data=",row[1] )
	# for i in range(count):
	# 	sql_select_Query1 = "select i[1] from tb_tracker1"
	# 	cursor = connection.cursor()
	# 	cursor.execute(sql_select_Query1)
	# 	records = cursor.fetchone()


except Error as e:
	print("Error reading data from MySQL table", e)
finally:
	if (connection.is_connected()):
		connection.close()
		cursor.close()
		print("MySQL connection is closed")




#############code to delete data##########################
    # sql_Delete_query = """Delete from Laptop where id = 7"""
    # cursor.execute(sql_Delete_query)
    # connection.commit()
