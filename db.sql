CREATE TABLE employee (
    employee_id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address TEXT,
    department TEXT NOT NULL
);

CREATE TABLE transaction (
    transaction_id serial PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employee(employee_id),
    type TEXT NOT NULL,
    receipt_number TEXT,
    date_time TIMESTAMP NOT NULL
);

CREATE TABLE product (
    product_id serial PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    available BOOLEAN NOT NULL
);

CREATE TABLE transaction_detail (
    transaction_id INTEGER REFERENCES transaction(transaction_id),
    product_id INTEGER REFERENCES product(product_id),
    quantity INTEGER NOT NULL
);

INSERT INTO product(name, category, price, stock, description)
VALUES('Guling', 'Kamar', 30000, 3, 'Bantal guling untuk tidur');

INSERT INTO product(name, category, price, stock, description)
VALUES('Selimut', 'Kamar', 100000, 1, 'Selimut untuk kasur');

INSERT INTO employee(username, password, name, phone_number, address, department)
VALUES('eric', 'hahaha', 'Eric Nur', '08122121212', 'Bandung', 'Management');

INSERT INTO employee(username, password, name, phone_number, address, department)
VALUES('pahrul', 'hihihi', 'Fahrul Maul', '08113123123', 'Bandung', 'Management');

INSERT INTO transaction(employee_id, type, receipt_number, date_time)
VALUES(1, 'IN', '6801000042069', '15-10-2022');

INSERT INTO transaction(employee_id, type, receipt_number, date_time)
VALUES(2, 'IN', '6801000042179', '22-02-2022');

INSERT INTO transaction_detail(transaction_id, product_id, quantity)
VALUES(1, 1, 3);

INSERT INTO transaction_detail(transaction_id, product_id, quantity)
VALUES(2, 2, 1);