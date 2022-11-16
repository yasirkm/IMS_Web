import connector

class Employee:
    def __init__(self, employee_id, username, password, name, phone_number, address, department):
        self._employee_id = employee_id
        self._username = username
        self._password = password
        self._name = name
        self._phone_number = phone_number
        self._address = address
        self._department = department

    def get_employee_id(self):
        return self._employee_id

    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
    
    def get_phone_number(self):
        return self._phone_number

    def set_phone_number(self, phone_number):
        self._phone_number = phone_number

    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    def get_department(self):
        return self._department

    def set_department(self, department):
        self._department = department

    def add_product(self, product):
        connector.add_product(self, product)

    def show_product_information(self, product_id):
        product_information = connector.get_product_information(self, product_id)
        print(product_information)

    def show_catalog(self):
        catalog = connector.get_catalog(self)
        print(catalog)

    def show_transactions(self):
        transactions = connector.get_transactions(self)
        print(transactions)

    def register_account(self, username, password, name):
        pass

    def do_transaction(self, receipt_number, transaction_details, transaction_type):
        connector.transact(self, receipt_number, transaction_details, transaction_type)

    def edit_product(self, product_id, name=None, category=None, price=None,  description=None):
        connector.edit_product_information(self, product_id, name, category, price, description)

    
class Transaction:
    def __init__(self, transaction_id, employee_id, type, receipt_number, date):
        self.transaction_id = transaction_id
        self.employee_id = employee_id
        self.type = type
        self.receipt_number = receipt_number
        self.date = date

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value):
        self._transaction_id = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        self._employee_id = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def receipt_number(self):
        return self._receipt_number

    @receipt_number.setter
    def receipt_number(self, value):
        self._receipt_number = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value


class Product:
    def __init__(self, product_id, name, category, price=0, stock=0, description=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

class Transaction_Detail:
    def __init__(self, transaction_id, product_id, quanitty):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quanitty

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value):
        self._transaction_id = value

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value