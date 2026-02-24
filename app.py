# import flask and its components
from flask import *
import os

# import pymysql module - Helps create a connection between python flask and mysql database
import pymysql

# Create/instanciate and flask application and give it a name
app = Flask(__name__)

# Configure the location to where your product images will be saved on your application
app.config["UPLOAD_FOLDER"] = "static/images"

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

        # By use of the cursor execute the sql checking whether the details entered compare with those in the database
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


# Below is the route for adding products.
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        # Extract the data enterd on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # For the product_photo, we shall fetch it from files as shown below
        product_photo = request.files["product_photo"]

        # Extract the file name of the product photo
        filename = product_photo.filename

        # By use of the os(Operating System) module, we can extract the file path where the image is currently saved.
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save the productphoto image into the new location
        product_photo.save(photo_path)

        # Printed out to test whether the details are received when sent with the request.
        # print(product_name, product_description, product_cost, product_photo)

        # Establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # Create a cursor
        cursor = connection.cursor()

        # Structure a sql query that will insert the details entered in the form
        sql = "INSERT INTO product_details(product_name,product_description,product_cost,product_photo) VALUES(%s,%s,%s,%s)"

        # Insert details entered into a tulpe
        data = (product_name,product_description,product_cost,filename)

        # Execute the sql by use of the cursor as you replace the place holders with the actual details
        cursor.execute(sql,data)

        # Commit the data entered in the form to the database
        connection.commit()

        return jsonify({"message":"Product inclusion successful"})
    
# Below is the route to fetch products
@app.route("/api/get_products")
def get_products():
    # Create a connection
    connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

    # Create a cursor
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Structure the query to fetch all the products from table product_details
    sql = "SELECT * FROM product_details"

    #Execute the query
    cursor.execute(sql)

    # Create a variable holding data fetched from the table
    products = cursor.fetchall()

    return jsonify(products)












# Run the application
app.run(debug=True)








