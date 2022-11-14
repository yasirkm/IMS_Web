class Employee:
    def __init__(self, employee_id, username, password, name, phone_number, address, department):
        self.employee_id = employee_id
        self.username = username
        self.password = password
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.department = department

class Transaction:
    def __init__(self, transaction_id, employee_id, type, receipt_number, data):
        self.transaction_id = transaction_id
        self.employee_id = employee_id
        self.type = type
        self.receipt_number = receipt_number
        self.date = date

class Product:
    def __init__(self, product_id, name, category, price, stock, description):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

class Transaction_Detail:
    def __init__(self, transaction_id, product_id, quanitty):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quanitty