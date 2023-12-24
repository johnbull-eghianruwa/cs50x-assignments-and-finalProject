from flask import Flask, render_template, session, redirect, request, jsonify
from flask_session import Session
import sqlite3
import base64

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define DTOs
class Customer:
    def __init__(self, firstName, lastName, address, gender, id = None, email = None, phoneNumber = None, measurement = None, comment = None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.email = email
        self.phoneNumber = phoneNumber
        self.gender = gender
        self.measurement = measurement
        self.comment = comment

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'address': self.address,
            'email': self.email,
            'phoneNumber': self.phoneNumber,
            'gender': self.gender,
            'measurement': self.measurement,
            'comment': self.comment
        }
    
class Order:
    def __init__(self, customerId, type, deliveryAddress, totalCost, amountPaid, status, orderDate, deliveryDate, comment = None, id = None, customer: Customer = None):
        self.id = id
        self.customerId = customerId
        self.type = type
        self.deliveryAddress = deliveryAddress
        self.totalCost = totalCost
        self.amountPaid = amountPaid
        self.status = status
        self.orderDate = orderDate
        self.deliveryDate = deliveryDate
        self.comment = comment
        self.customer = customer

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'customerId': self.customerId,
            'type': self.type,
            'deliveryAddress': self.deliveryAddress,
            'totalCost': self.totalCost,
            'amountPaid': self.amountPaid,
            'status': self.status,
            'orderDate': self.orderDate,
            'deliveryDate': self.deliveryDate,
            'comment': self.comment,
            'customer': None if self.customer == None else self.customer.serialized 
        }

class User:
    def __init__(self, username, password, id = None):
        self.id = id
        self.username = username
        self.password = password

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }

def getListOfCustomers(conn):
    return conn.execute('SELECT * FROM Customers').fetchall()

def getListOfOrders(conn):
    return conn.execute('SELECT Orders.*, Customers.* FROM Orders INNER JOIN Customers ON Orders.customerId = Customers.id').fetchall()

def getListOfUsers(conn):
    return conn.execute('SELECT * FROM Users').fetchall()

def init_db():
    connection = sqlite3.connect('jbfashion.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())

        cur = connection.cursor()
        username = 'admin'
        password = 'random-string'

        user = cur.execute('SELECT * FROM Users WHERE username=?', [username]).fetchone()

        if user == None:
            cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)",
                (username, password)
            )

        connection.commit()
        connection.close()

init_db()

def connect_to_db():
    conn = sqlite3.connect('jbfashion.db')
    return conn

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pwd")

        try:
            conn = connect_to_db()
            user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

            if user == None:
                return render_template("login.html", message = "Please check the credential again either username or password or both are invalid.")
            else:
                session["name"] = username
                return redirect("/")
        except:
            return render_template("login.html", message = "Internal Server Error")
        finally:
            conn.close()
    return render_template("login.html")

@app.route("/customers")
def customerPage():
    if not session.get("name"):
        return redirect("/login")
    
    try:
        conn = connect_to_db()
        customers = getListOfCustomers(conn)
    except:
        return render_template("user.html", message = "unable to access the database")
    finally:
            conn.close()
    customerList = []
    for row in customers:
        customer = Customer(row[1], row[2], row[3], row[6], row[0], row[4], row[5], row[7], row[8])
        customerList.append(customer.serialized)
    return render_template("customer.html", customers = customerList)

@app.route("/orders")
def orderPage():
    if not session.get("name"):
        return redirect("/login")

    try:
        conn = connect_to_db()
        customers = getListOfCustomers(conn)
        orders = getListOfOrders(conn)
    except:
        return render_template("order.html", message = "unable to access the database")
    finally:
            conn.close()
    
    customerList = []
    orderList = []
    for row in customers:
        customer = Customer(row[1], row[2], row[3], row[6], row[0], row[4], row[5], row[7], row[8])
        customerList.append(customer.serialized)

    for row in orders:
        print(row)
        customer = Customer(row[11], row[12], row[13], row[16], row[10], row[14], row[15], row[17], row[18])
        order = Order(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[0], customer)
        orderList.append(order.serialized)

    print(orderList)

    return render_template("order.html", customers = customerList, orders = orderList)

@app.route("/settings")
def settingPage():
    if not session.get("name"):
        return redirect("/login")

    try:
        conn = connect_to_db()
        users = []
        if session.get("name") == "admin":
            users = getListOfUsers(conn)
        else:
            u = conn.execute('SELECT * FROM Users WHERE username =? ', [session.get("name")]).fetchone()
            users.append(u)
    except:
        return render_template("setting.html", message = "unable to access the database")
    finally:
            conn.close()
    userList = []
    for row in users:
        user = User(row[1], row[2], row[0])
        userList.append(user.serialized)
    
    return render_template("setting.html", users = userList)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

#####
##### CUSTOMERS API
#####
# API to add a new customer
@app.route("/api/customers", methods=["POST"])
def addCustomerApi():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsonBody = request.json
        customer = Customer(**jsonBody)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                cursor = conn.cursor()

                if session.get("name"):
                    cursor.execute(
                        'INSERT INTO Customers (firstName, lastName, address, email, phoneNumber, gender, measurement, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                        (customer.firstName, customer.lastName, customer.address, customer.email, customer.phoneNumber, customer.gender, customer.measurement, customer.comment)
                    )

                    conn.commit()

                    customer.id = cursor.lastrowid

                    return jsonify(customer.serialized), 201
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'error': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        cursor.execute(
                            'INSERT INTO Customers (firstName, lastName, address, email, phoneNumber, gender, measurement, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (customer.firstName, customer.lastName, customer.address, customer.email, customer.phoneNumber, customer.gender, customer.measurement, customer.comment)
                        )

                        conn.commit()

                        customer.id = cursor.lastrowid

                    return jsonify(customer.serialized), 201
            except sqlite3.IntegrityError as err:
                print(err)
                conn.rollback()
                return jsonify({'message': 'The email is already register to another customer'}), 400
            except BaseException as ex:
                print(ex)
                conn.rollback()
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400

# API to get list of all customers
@app.route("/api/customers", methods=["GET"])
def getListOfCustomersApi():
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            customerList = []

            if session.get("name"):
                rows = getListOfCustomers(conn)

                for row in rows:
                    customer = Customer(row[1], row[2], row[3], row[6], row[0], row[4], row[5], row[7], row[8])
                    customerList.append(customer.serialized)

                return jsonify(customerList), 200
            else:
                authenticationHeader = request.headers.get('Authorization').strip().split(" ")

                if 'basic' in authenticationHeader[0].lower():
                    auth = authenticationHeader[1]
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        rows = getListOfCustomers(conn)

                        for row in rows:
                            customer = Customer(row[1], row[2], row[3], row[6], row[0], row[4], row[5], row[7], row[8])
                            customerList.append(customer.serialized)

                        return jsonify(customerList), 200
                else:
                    return jsonify({"message": "Unsupported authentication scheme"}), 400    
        except:
            return jsonify({'message': 'Server side error, please contact the admin'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401

# API to get details of a specified customer   
@app.route("/api/customers/<id>", methods=["GET"])
def getCustomerByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            if session.get("name"):
                row = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                customer = Customer(row[1], row[2], row[3], row[6], row[0], row[4], row[5], row[7], row[8])
                return jsonify(customer.serialized), 200
            else:
                authenticationHeader = request.headers.get('Authorization')
                auth = authenticationHeader.strip().split(" ")
                decode = base64.decode(auth)
                username = decode.split(":")[0]
                password = decode.split(":")[1]
                user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                if user == None:
                    return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                else:
                    retrievedRawData = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                    customer = Customer(retrievedRawData[1], retrievedRawData[2], retrievedRawData[3], retrievedRawData[6], retrievedRawData[0], retrievedRawData[4], retrievedRawData[5], retrievedRawData[7], retrievedRawData[8])
                    return jsonify(customer.serialized), 200
        except:
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401

# API to modify an existing customer
@app.route("/api/customers/<id>", methods=["PUT"])
def modifyCustomerByIdApi(id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        customer = Customer(**json)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                if session.get("name"):
                    retrievedCustomer = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                    if retrievedCustomer == None:
                        return jsonify({'message': 'Unable to update the order item, the order item does not exist'}), 400
                    else:  
                        # modify -> 200
                        cursor = conn.cursor()
                        cursor.execute(
                            '''UPDATE Customers SET firstName = ?, lastName = ?, address = ?, email = ?, phoneNumber = ?, gender = ?, measurement = ?, comment = ? WHERE id = ?''',
                            (customer.firstName, customer.lastName, customer.address, customer.email, customer.phoneNumber, customer.gender, customer.measurement, customer.comment, customer.id)
                        )
                        conn.commit()
                        return jsonify(customer.serialized), 200
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        retrievedCustomer = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                        if retrievedCustomer == None:
                            return jsonify({'message': 'Unable to update the order item, the order item does not exist'}), 400
                        else: 
                            # modify -> 200
                            cursor = conn.cursor()
                            cursor.execute(
                                '''UPDATE Customers SET firstName = ?, lastName = ?, address = ?, email = ?, phoneNumber = ?, gender = ?, measurement = ?, comment = ? WHERE id = ?''',
                                (customer.firstName, customer.lastName, customer.address, customer.email, customer.phoneNumber, customer.gender, customer.measurement, customer.comment, customer.id)
                            )
                            conn.commit()
                            return jsonify(customer.serialized), 200
            except:
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400

# API for deleting a specified customer
@app.route("/api/customers/<id>", methods=["DELETE"])
def DeleteCustomerByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            if session.get("name"):
                customer = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                if customer != None:
                    ordersId = conn.execute("SELECT id FROM Orders WHERE customerId=?", [id]).fetchall()

                    if ordersId != None:
                        for orderId in ordersId:
                            conn.execute("DELETE FROM Orders WHERE id=?", (orderId))
                            conn.commit()

                    conn.execute('DELETE FROM Customers WHERE id = ?', (id,))
                    conn.commit()
                return "", 204
            else:
                authenticationHeader = request.headers.get('Authorization')
                auth = authenticationHeader.strip().split(" ")
                decode = base64.decode(auth)
                username = decode.split(":")[0]
                password = decode.split(":")[1]
                user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                if user == None:
                    return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                else:
                    customer = conn.execute('SELECT * FROM Customers WHERE id=?', [id]).fetchone()
                    if customer != None:
                        ordersId = conn.execute("SELECT id FROM Orders WHERE customerId=?", [id]).fetchall()

                        if ordersId != None:
                            for orderId in ordersId:
                                conn.execute("DELETE FROM Orders WHERE id=?", [orderId])
                                conn.commit()

                        conn.execute('DELETE FROM Customers WHERE id = ?', (id,))
                        conn.commit()
                    return "", 204
        except BaseException as ex:
            print(ex)
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401 


#####
##### ORDERS API
#####
# API to add a new order
@app.route("/api/orders", methods=["POST"])
def addOrderApi():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsonBody = request.json
        print(jsonBody)
        order = Order(**jsonBody)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                cursor = conn.cursor()

                if session.get("name"):
                    customer = conn.execute('SELECT * FROM Customers WHERE id=?', [order.customerId]).fetchone()

                    if customer == None:
                        return jsonify({'error': 'The specify customer id does not exist.'}), 400
                    else:
                        cursor.execute(
                            'INSERT INTO Orders (customerId, type, deliveryAddress, totalCost, amountPaid, status, orderDate, deliveryDate, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                            (order.customerId, order.type, order.deliveryAddress, order.totalCost, order.amountPaid, order.status, order.orderDate, order.deliveryDate, order.comment)
                        )

                        conn.commit()

                        order.id = cursor.lastrowid

                        return jsonify(order.serialized), 201
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'error': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        customer = conn.execute('SELECT * FROM Customers WHERE id=?', [order.customerId]).fetchone()

                        if customer == None:
                            return jsonify({'error': 'The specify customer id does not exist.'}), 400
                        else:
                            cursor.execute(
                                'INSERT INTO Orders (customerId, type, deliveryAddress, totalCost, amountPaid, status, orderDate, deliveryDate, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                                (order.customerId, order.type, order.deliveryAddress, order.totalCost, order.amountPaid, order.status, order.orderDate, order.deliveryDate, order.comment)
                            )

                            conn.commit()

                            order.id = cursor.lastrowid

                            return jsonify(order), 201
            except BaseException as ex:
                print(ex)
                conn.rollback()
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400
    
# API to get list of all orders
@app.route("/api/orders", methods=["GET"])
def getListOfOrdersApi():
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            orderList = []

            if session.get("name"):
                rows = getListOfOrders(conn)

                for row in rows:
                    customer = Customer(row[11], row[12], row[13], row[16], row[10], row[14], row[15], row[17], row[18])
                    order = Order(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[0], customer)
                    orderList.append(order.serialized)

                return jsonify(orderList), 200
            else:
                authenticationHeader = request.headers.get('Authorization').strip().split(" ")

                if 'basic' in authenticationHeader[0].lower():
                    auth = authenticationHeader[1]
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        rows = getListOfOrders(conn)

                        for row in rows:
                            customer = Customer(row[11], row[12], row[13], row[16], row[10], row[14], row[15], row[17], row[18])
                            order = Order(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[0], customer)
                            orderList.append(order.serialized)

                        return jsonify(orderList), 200
                else:
                    return jsonify({"message": "Unsupported authentication scheme"}), 400    
        except:
            return jsonify({'message': 'Server side error, please contact the admin'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401

# API to get details of a specified order   
@app.route("/api/orders/<id>", methods=["GET"])
def getOrderByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            if session.get("name"):
                retrievedRawData = conn.execute('SELECT Orders.*, Customers.* FROM Orders INNER JOIN Customers ON Orders.customerId = Customers.id WHERE id=?', [id]).fetchone()
                customer = Customer(retrievedRawData[10], retrievedRawData[11], retrievedRawData[14], retrievedRawData[15], retrievedRawData[1], retrievedRawData[13], retrievedRawData[14], retrievedRawData[16], retrievedRawData[17])
                order = Order(retrievedRawData[1], retrievedRawData[2], retrievedRawData[3], retrievedRawData[4], retrievedRawData[5], retrievedRawData[6], retrievedRawData[7], retrievedRawData[8], retrievedRawData[9], retrievedRawData[0], customer)
                return jsonify(order.serialized), 200
            else:
                authenticationHeader = request.headers.get('Authorization')
                auth = authenticationHeader.strip().split(" ")
                decode = base64.decode(auth)
                username = decode.split(":")[0]
                password = decode.split(":")[1]
                user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                if user == None:
                    return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                else:
                    retrievedRawData = conn.execute('SELECT Orders.*, Customers.* FROM Orders INNER JOIN Customers ON Orders.customerId = Customers.id WHERE id=?', [id]).fetchone()
                    customer = Customer(retrievedRawData[10], retrievedRawData[11], retrievedRawData[14], retrievedRawData[15], retrievedRawData[1], retrievedRawData[13], retrievedRawData[14], retrievedRawData[16], retrievedRawData[17])
                    order = Order(retrievedRawData[1], retrievedRawData[2], retrievedRawData[3], retrievedRawData[4], retrievedRawData[5], retrievedRawData[6], retrievedRawData[7], retrievedRawData[8], retrievedRawData[9], retrievedRawData[0], customer)
                    return jsonify(order.serialized), 200
        except:
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401

# API to modify an existing order
@app.route("/api/orders/<id>", methods=["PUT"])
def modifyOrderByIdApi(id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        order = Order(**json)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                if session.get("name"):
                    retrievedCustomer = conn.execute('SELECT * FROM Customers WHERE id=?', [order.customerId]).fetchone()

                    if retrievedCustomer == None:
                        return jsonify({'message': 'Unable to update the order item, the specify customer does not exist'}), 400

                    retrievedOrder = conn.execute('SELECT * FROM Orders WHERE id=?', [id]).fetchone()
                    if retrievedOrder == None:
                        return jsonify({'message': 'Unable to update the order item, the order item does not exist'}), 400
                    else:  
                        # modify -> 200
                        cursor = conn.cursor()
                        cursor.execute(
                            '''UPDATE Orders SET customerId = ?, type = ?, deliveryAddress = ?, totalCost = ?, amountPaid = ?, status = ?, orderDate = ?, deliveryDate = ?, comment = ? WHERE id = ?''',
                            (order.customerId, order.type, order.deliveryAddress, order.totalCost, order.amountPaid, order.status, order.orderDate, order.deliveryDate, order.comment, order.id)
                        )
                        conn.commit()
                        customer = Customer(retrievedCustomer[1], retrievedCustomer[2], retrievedCustomer[3], retrievedCustomer[6], retrievedCustomer[0], retrievedCustomer[4], retrievedCustomer[5], retrievedCustomer[7], retrievedCustomer[8])
                        order.customer = customer
                        return jsonify(order.serialized), 200
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        retrievedCustomer = conn.execute('SELECT * FROM Customers WHERE id=?', [order.customerId]).fetchone()

                        if retrievedCustomer == None:
                            return jsonify({'message': 'Unable to update the order item, the specify customer does not exist'}), 400

                        retrievedOrder = conn.execute('SELECT * FROM Orders WHERE id=?', [id]).fetchone()
                        if retrievedOrder == None:
                            return jsonify({'message': 'Unable to update the order item, the order item does not exist'}), 400
                        else: 
                            # modify -> 200
                            cursor = conn.cursor()
                            cursor.execute(
                                '''UPDATE Orders SET customerId = ?, type = ?, deliveryAddress = ?, totalCost = ?, amountPaid = ?, status = ?, orderDate = ?, deliveryDate = ?, comment = ? WHERE id = ?''',
                                (order.customerId, order.type, order.deliveryAddress, order.totalCost, order.amountPaid, order.status, order.orderDate, order.deliveryDate, order.comment, order.id)
                            )
                            conn.commit()
                            customer = Customer(retrievedCustomer[1], retrievedCustomer[2], retrievedCustomer[3], retrievedCustomer[6], retrievedCustomer[0], retrievedCustomer[4], retrievedCustomer[5], retrievedCustomer[7], retrievedCustomer[8])
                            order.customer = customer
                            return jsonify(order.serialized), 200
            except:
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400


@app.route("/api/orders/<id>", methods=["DELETE"])
def DeleteOrderByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
                conn = connect_to_db()

                if session.get("name"):
                    order = conn.execute('SELECT * FROM Orders WHERE id=?', [id]).fetchone()
                    if order != None:
                        conn.execute("DELETE FROM Orders WHERE id=?", [id])
                        conn.commit()
                    return "", 204
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        order = conn.execute('SELECT * FROM Orders WHERE id=?', [id]).fetchone()
                        if order != None:
                            conn.execute("DELETE FROM Orders WHERE id=?", [id])
                            conn.commit()
                        return "", 204
        except:
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401 

 #####
##### USERS API
#####
# API to add a new user
@app.route("/api/users", methods=["POST"])
def adduserApi():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsonBody = request.json
        user = User(**jsonBody)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                cursor = conn.cursor()

                if session.get("name") == "admin":
                    cursor.execute(
                        'INSERT INTO Users (username, password) VALUES (?, ?)', 
                        (user.username, user.password)
                    )

                    conn.commit()

                    user.id = cursor.lastrowid

                    return jsonify(user.serialized), 201
                elif (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ): 
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]

                    if username == "admin":
                        adminUser = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                        if adminUser == None:
                            return jsonify({'error': 'Authorization failed, either username or password or both are incorrect'}), 401
                        else:
                            cursor.execute(
                                'INSERT INTO Users (username, password) VALUES (?, ?)', 
                                (user.username, user.password)
                            )

                            conn.commit()

                            user.id = cursor.lastrowid

                            return jsonify(user.serialized), 201
                    else:
                        return jsonify({'message': 'Permission denied'}), 403
                else:
                    return jsonify({'message': 'Permission denied'}), 403
            except sqlite3.IntegrityError as err:
                print(err)
                conn.rollback()
                return jsonify({'message': 'The username is already registered'}), 400
            except:
                conn.rollback()
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400

# API to get list of all users
@app.route("/api/users", methods=["GET"])
def getListOfUsersApi():
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            userList = []

            if session.get("name"):
                if session.get("name") == "admin":
                    rows = getListOfUsers(conn)

                    for row in rows:
                        user = User(row[1], row[2], row[0])
                        userList.append(user.serialized)

                    return jsonify(userList), 200
                else:
                    return jsonify({'message': 'Permission denied'}), 403
            else:
                authenticationHeader = request.headers.get('Authorization').strip().split(" ")

                if 'basic' in authenticationHeader[0].lower():
                    auth = authenticationHeader[1]
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if user == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    if user[0] != "admin":
                        return jsonify({'message': 'Permission denied'}), 403
                    else:
                        rows = getListOfUsers(conn)

                        for row in rows:
                            user = User(row[1], row[2], row[0])
                            userList.append(user.serialized)

                        return jsonify(userList), 200
                else:
                    return jsonify({"message": "Unsupported authentication scheme"}), 400    
        except:
            return jsonify({'message': 'Server side error, please contact the admin'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    
# API to get details of a specified user   
@app.route("/api/users/<id>", methods=["GET"])
def getUserByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            if session.get("name"):
                retrievedUser = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()
                if retrievedUser != None:
                    userJson = User(retrievedUser[1], retrievedUser[2], retrievedUser[0])
                    if session.get("name") == "admin" or userJson.username == session.get("name"):
                        return jsonify(userJson.serialized), 200
                    else:
                        return jsonify({'message': 'Permission denied'}), 403
                else:
                    return jsonify({'message': 'The specify user does not exist'}), 400
            else:
                authenticationHeader = request.headers.get('Authorization')
                auth = authenticationHeader.strip().split(" ")
                decode = base64.decode(auth)
                username = decode.split(":")[0]
                password = decode.split(":")[1]
                user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                if user == None:
                    return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                else:
                    retrievedUser = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()
                    if retrievedUser != None:
                        userJson = User(retrievedUser[1], retrievedUser[2], retrievedUser[0])
                        if user[1] == "admin" or userJson.username == user[1]:
                            return jsonify(user.serialized), 200
                        else:
                            return jsonify({'message': 'Permission denied'}), 403
                    else:
                        return jsonify({'message': 'The specify user does not exist'}), 400
        except:
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    
# API to modify an existing user
@app.route("/api/users/<id>", methods=["PUT"])
def modifyUserByIdApi(id):
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        user = User(**json)

        if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
            try:
                conn = connect_to_db()

                if session.get("name"):
                    retrievedUser = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()

                    if retrievedUser == None:
                        return jsonify({'message': 'The specify user does not exist'}), 400
                    else:
                        if retrievedUser[1] == "admin" and user.username != "admin":
                            return jsonify({'message': 'You cannot change the username of a special user'}), 400
                        
                        if session.get("name") != "admin" and user.username != retrievedUser[1]:
                            return jsonify({'message': 'You do not have the permission to make this changes'}), 403

                        # modify -> 200
                        cursor = conn.cursor()
                        cursor.execute(
                            '''UPDATE Users SET username = ?, password = ? WHERE id = ?''',
                            (user.username, user.password, id)
                        )
                        conn.commit()
                        return jsonify(user.serialized), 200
                else:
                    authenticationHeader = request.headers.get('Authorization')
                    auth = authenticationHeader.strip().split(" ")
                    decode = base64.decode(auth)
                    username = decode.split(":")[0]
                    password = decode.split(":")[1]
                    authenticatedUser = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()

                    if authenticatedUser == None:
                        return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                    else:
                        retrievedUser = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()

                        if retrievedUser == None:
                            return jsonify({'message': 'The specify user does not exist'}), 400
                        else: 
                            # modify -> 200
                            if retrievedUser[1] == "admin" and user.username != "admin":
                                return jsonify({'message': 'You cannot change the username of a special user'}), 400
                            
                            if authenticatedUser[1] != "admin" and user.username != retrievedUser[1]:
                                return jsonify({'message': 'You do not have the permission to make this changes'}), 403

                            # modify -> 200
                            cursor = conn.cursor()
                            cursor.execute(
                                '''UPDATE Users SET username = ?, password = ? WHERE id = ?''',
                                (user.username, user.password, id)
                            )
                            conn.commit()
                            return jsonify(user.serialized), 200
            except:
                return jsonify({'message': 'Internal Server Error'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401
    else:
        return jsonify({'message': 'Content-Type not supported'}), 400

# Delete a specified user
@app.route("/api/users/<id>", methods=["DELETE"])
def DeleteUserByIdApi(id):
    if session.get("name") or (request.headers.get('Authorization') != None  and len(request.headers.get('Authorization').strip()) > 0 ):
        try:
            conn = connect_to_db()

            if session.get("name"):
                if session.get("name") != "admin":
                    return jsonify({'message': 'You do not have the permission to execute this operation'}), 403
                    
                user = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()
                if user[1] == "admin":
                    return jsonify({'message': 'You do not have the permission to execute this operation'}), 403
                    
                if user != None:
                    conn.execute("DELETE FROM Users WHERE id=?", [id])
                    conn.commit()
                return "", 204
            else:
                authenticationHeader = request.headers.get('Authorization')
                auth = authenticationHeader.strip().split(" ")
                decode = base64.decode(auth)
                username = decode.split(":")[0]
                password = decode.split(":")[1]

                if username != "admin":
                    return jsonify({'message': 'You do not have the permission to execute this operation'}), 403

                user = conn.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, password)).fetchone()
                if user[1] == "admin":
                    return jsonify({'message': 'You do not have the permission to execute this operation'}), 403

                if user == None:
                    return jsonify({'message': 'Authorization failed, either username or password or both are incorrect'}), 401
                else:
                    user = conn.execute('SELECT * FROM Users WHERE id=?', [id]).fetchone()
                    if user != None:
                        conn.execute("DELETE FROM Users WHERE id=?", [id])
                        conn.commit()
                    return "", 204
        except:
            return jsonify({'message': 'Internal Server Error'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'Unauthorized access, please provide a valid credential'}), 401

if __name__ == "__main__":
    app.run(debug=True)
            