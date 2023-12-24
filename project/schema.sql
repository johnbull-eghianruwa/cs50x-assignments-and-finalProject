CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT UNIQUE,
    phoneNumber TEXT,
    gender TEXT,
    measurement TEXT,
    comment TEXT
);

CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customerId INTEGER NOT NULL,
    type TEXT NOT NULL,
    deliveryAddress TEXT NOT NULL,
    totalCost REAL NOT NULL,
    amountPaid REAL NOT NULL,
    status TEXT NOT NULL,
    orderDate DATE,
    deliveryDate DATE,
    comment TEXT,
    FOREIGN KEY (customerId) REFERENCES Customers (id)
);
