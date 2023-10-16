POKEAPI

run "create_db.py" to create the "pokemon" MYSQL database
you need to change the password in the file for the one you selected when installing mysql.

the first time you run the code, un-comment line 19 of the "__init__.py" file inside the "website" folder to create the "pokemon" table
here you also need to put your own password in line 9 (the one you select when installing mysql), right after "root:" (mine is "1234") 
afterwards, comment line 19 back.

to start the app, run the "main.py" file.

pip packages:
	flask
	flask-sqlalchemy
	mysql-connector-python
	requests
	sqlalchemy
	pymysql