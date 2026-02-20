# import flask and its components
from flask import *

# import pymysql module - Helps create a connection between python flask and mysql database
import pymysql

# Create and flask application and give it a name
app = Flask(__name__)


# Below is the sign up route
@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        # Extract the different details enter on the form
        username = request.form["username"]
        email   = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # By use of the print function lets print all those details sent with the upcoming request
        # print(username, email, password, phone)

        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # Create a cursor to execute the sql queries
        cursor = connection.cursor()

        # Structure the sql to insert the details received from the form
        # %s -A placeholder(Stands inplaces of actual values i.e we shall place them later on)
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s,%s,%s,%s)"

        # create a tuple that will hold all the data gotten from the form
        data = (username, email, phone, password)

        # By use of the cursor, execute the sql as you replace the place holders with the actual values
        cursor.execute(sql,data)

        # commit the changes to the database
        connection.commit()

        return jsonify({"message" : "User registered successfully"})


# Below is the login/signin in route
@app.route("/api/signin", methods= ["POST"])
def signin():
    if request.method == "POST":
        # Extract two details entered in the form
        email= request.form["email"]
        password = request.form["password"]

        # # Print out the details entered
        # print(email, password)

        # Create/establish a connection to the database
        connection = pymysql.connect(host = "localhost", user = "root", password = "", database = "sokogardenonline")

        # Create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Structure an sql query that will check whether the email and password entered are correct
        sql = "SELECT * FROM users WHERE email= %s AND password = %s"

        # Put the data received from the form into a tuple
        data = (email, password)

        # By use of the cursor execute the sql
        cursor.execute(sql,data)

        # Check whether there are rows returned and store the same on a variable
        count = cursor.rowcount

        # If there are records returned it means the password and email are correct otherwise it means they are wrong
        if count == 0:
            return jsonify({"messsage" : " Failed Login"})
        else:
            # There must be a user so we create a variable that will hold the details of the user fetched from the database
            user = cursor.fetchone()
            # Return the details to the frintend as well as a message
            return jsonify({"message" : "Successful User Login ", "user":user})
















# Run the application
app.run(debug=True)








