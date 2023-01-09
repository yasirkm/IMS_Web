from datetime import datetime
from abc import ABC

import database.connector as connector
import database.auth as auth

from database.privileges import *

class PrivilegeError(Exception):
    pass

class Employee:
    '''
        Class which correspond to the table employee in database
    '''
    def __init__(self, employee_id, username, password, name, phone_number, department, address=None):
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

    @classmethod
    def login(cls, username, password):
        '''
            Logs user in.
            Return logged employee.
        '''
        employee = Employee(**auth.login(username, password))

        return employee

    def get_info_privilege(self):
        '''
            Return privilege value for informations the user's department has access to
        '''
        return INFO_PRIVILEGES[self.get_department()]

    def get_edit_privilege(self):
        '''
            Return privilege value for informations the employee's department can edit
        '''
        return EDIT_PRIVILEGES[self.get_department()]

    def _get_query_columns(self):
        '''
            Return columns for informations the employee has access to based on their privilege
        '''
        privilege_column = {
            PRODUCT_NAME:'name',
            PRODUCT_CATEGORY:'category',
            PRODUCT_PRICE:'price',
            PRODUCT_STOCK:'stock',
            PRODUCT_DESCRIPTION:'description'
        }
        user_privilege = self.get_info_privilege()

        query_columns = ('product_id',)+tuple(column for privilege, column in privilege_column.items() if user_privilege&privilege)

        return query_columns

    def _get_edit_columns(self):
        '''
            Return columns for informations the employee can edit based on their privilege
        '''
        privilege_column = {
            PRODUCT_NAME:'name',
            PRODUCT_CATEGORY:'category',
            PRODUCT_PRICE:'price',
            PRODUCT_STOCK:'stock',
            PRODUCT_DESCRIPTION:'description'
        }
        user_privilege = self.get_edit_privilege()

        edit_columns = tuple(column for privilege, column in privilege_column.items() if user_privilege&privilege)

        return edit_columns

    def show_product_information(self, product):
        '''
            Print out a product's information which the employee has access to
        '''
        query_columns = self._get_query_columns()
        query_columns = {column:product[column] for column in query_columns}

        row = "{:<20}"*len(query_columns) # Template for string formatting
        print(row.format(*map(str, query_columns))) # Print column header
        print(row.format(*map(str, query_columns.values()))) # Print column value
    
    def show_transaction_information(self, transaction):
        '''
            Print out the information of a transaction
        '''
        def _show_transaction_details():
            '''
                Print out the detail of the transaction
            '''
            transaction_detail_list = connector.get_transaction_details(transaction.transaction_id)
            for transaction_detail_information in transaction_detail_list:
                transaction_detail = Transaction_Detail(**transaction_detail_information)
                product = Product(**connector.get_product_information(transaction_detail.product_id))
                print(f'product_name: {product.name}')
                print(f'quantity: {transaction_detail.quantity}')
                print(f'price at transaction: {transaction_detail.price_at_transaction}')
                print()

        user_privilege = self.get_info_privilege()
        if not user_privilege&TRANSACTION:
                raise PrivilegeError('User has no privilege to see transaction history')
        print(f'transaction_id: {transaction.transaction_id}')
        print(f'employee_id: {transaction.employee_id}')
        print(f'type: {transaction.type}')
        print(f'receipt_number: {transaction.receipt_number}')
        print(f'date_time: {transaction.date_time}')
        print()
        print('details: ')
        _show_transaction_details()

    def show_catalog(self):
        '''
            Print out all products available
        '''
        query_columns = self._get_query_columns()
        row = "{:<20}"*len(query_columns) # Template for string formatting
        print(row.format(*map(str, query_columns))) # Print column header

        # Getting catalog
        catalog = connector.get_catalog()
        catalog = (Product(**product) for product in catalog)

        # Printing all products in catalog
        for product in catalog:
            query_columns = {column:product[column] for column in query_columns}
            print(row.format(*map(str, query_columns.values())))

    def show_transaction_history(self):
        '''
            Print out transaction history
        '''
        user_privilege = self.get_info_privilege()
        if not user_privilege&TRANSACTION: # Deny usage by raising exception
            raise PrivilegeError("User don't have the privilege to view transaction history")

        pad = 20
        print(f"{'transaction_id':<{pad}}{'employee_id':<{pad}}{'type':<{pad}}{'receipt_number':<{pad}}{'date':<{pad}}")

        # Getting transaction history
        transactions = connector.get_transactions()
        transactions = (Transaction(**transaction) for transaction in transactions)

        # Printing all transactions
        for transaction in transactions:
            print(f"{transaction.transaction_id:<{pad}}{transaction.employee_id:<{pad}}{transaction.type:<{pad}}{transaction.receipt_number:<{pad}}{transaction.date_time.strftime('%Y-%m-%d %H:%M:%S'):<{pad}}")

    def __getitem__(self, attribute):
        '''
            Special method for attribute access
        '''
        callback = {
            'employee_id':self.get_employee_id,
            'username':self.get_username,
            'password':self.get_password,
            'name':self.get_name,
            'phone_number':self.get_phone_number,
            'address':self.get_address,
            'department':self.get_department
        }
        return callback[attribute]()
    def keys(self):
        '''
            Helper method for the purpose of keyword unpacking purpose
        '''
        return ('employee_id', 'username', 'password', 'name', 'phone_number', 'address', 'department')
    
class Can_Edit_Catalog(ABC):
    '''
        Abstract class for implementation purpose. Needed for DRY principle
    '''

    def add_product(self, name, category, price, description=None):
        '''
            Add a new product.
            Return the newly added product.
        '''
        # Privilege checking
        user_privilege = self.get_edit_privilege()
        if not user_privilege&CATALOG:
            raise PrivilegeError("User don't have catalog edit privilege")
        
        product_id=connector.add_product(name=name, category=category, price=price, description=description)
        new_product = Product(product_id=product_id, name=name, category=category, price=price, description=description)
        
        return new_product
    
    def delete_product(self, product):
        '''
            Delete a product.
        '''
        # Privilege checking
        user_privilege = self.get_edit_privilege()
        if not user_privilege&CATALOG:
            raise PrivilegeError("User don't have catalog edit privilege")
        
        # Deleting product
        product.available = False # Editing the available attribute essentially deletes the product from catalog
        # Updating database
        connector.edit_product_information(**product)
    
class Can_Edit_Product_Info(ABC):
    '''
        Abstract class for implementation purpose. Needed for DRY principle
    '''
    def edit_product(self, product, name=None, category=None, price=None,  description=None):
        '''
            Edit a product with the given value.
        '''
        columns_value = {
            'name':name,
            'category':category,
            'price':price,
            'description':description
        }
        edit_columns = self._get_edit_columns()

        if not edit_columns:
            raise PrivilegeError("User don't have the privilege to edit product")
        
        # Editing product
        for column in edit_columns:
            product[column] = columns_value[column] if columns_value[column] is not None else product[column]

        # Updating database
        connector.edit_product_information(**product)

class Can_Do_Transaction(ABC):
    '''
        Abstract class for implementation purpose. Needed for DRY principle
    '''
    def do_transaction(self, receipt_number, transaction_details, transaction_type):
        '''
            Do a transaction.
            Return done transaction.

            transaction_details: a tuple of product, its quantity, and its current price
            transaction_type: 'IN' or 'OUT'
        '''
        date_time = datetime.now()
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        employee_id = self.get_employee_id()
        user_privilege = self.get_edit_privilege()

        if not user_privilege%TRANSACTION:
            raise PrivilegeError("User don't have the privilge to do transaction")
        
        transaction_id = connector.transact(employee_id, receipt_number, transaction_details, transaction_type, date_time)

        new_transaction = Transaction(transaction_id, employee_id, transaction_type, date_time, receipt_number)

        return new_transaction

class Management(Employee, Can_Edit_Catalog, Can_Edit_Product_Info, Can_Do_Transaction):
    '''
        Subclass of Employee in which the employee's department is Management
    '''  
    def register_account(self, username, password, name, phone_number, department, address=None):
        '''
            Register a new employee account with given arguments.
            Return newly registered employee.
        '''
        user_privilege = self.get_edit_privilege()
        if not user_privilege&REGISTRATION:
            raise PrivilegeError("User don't have the privilege to register an employee account")

        employee_id = connector.register(username=username, password=password, name=name, phone_number=phone_number, department=department, address=address)
        new_employee = Employee(employee_id=employee_id, username=username, password=password, name=name, phone_number=phone_number, department=department, address=address)
        return new_employee
    
class Storage(Employee, Can_Edit_Catalog, Can_Edit_Product_Info, Can_Do_Transaction):
    '''
        Subclass of Employee in which the employee's department is Storage
    '''  
    pass

class Finance(Employee, Can_Edit_Product_Info):
    '''
        Subclass of Employee in which the employee's department is Finance
    '''  
    pass

class Transaction:
    '''
        Class which correspond to the table transaction in database
    '''
    def __init__(self, transaction_id, employee_id, type, date_time, receipt_number=None):
        self.transaction_id = transaction_id
        self.employee_id = employee_id
        self.type = type
        self.receipt_number = receipt_number
        self.date_time = date_time
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
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        self._date_time = value

    def __getitem__(self, attribute):
        '''
            Special method for attribute access
        '''
        return getattr(self, attribute)
    
    def keys(self):
        '''
            Helper method for keyword unpacking purpose
        '''
        return ('transaction_id', 'employee_id', 'type', 'receipt_number', 'date_time')

class Product:
    '''
        Class which correspond to the table product in database
    '''
    def __init__(self, product_id, name, category, price=0, stock=0, description=None, available=True):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description
        self.available=None

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

    @property
    def available(self):
        return self._available
    
    @available.setter
    def available(self, value):
        self._available = value

    def __iter__(self):
        '''
            Helper method for unpacking purpose
        '''
        return iter((self.product_id, self.name, self.category, self.price, self.stock, self.description))

    def __getitem__(self, attribute):
        '''
            Special method for attribute access
        '''
        return getattr(self, attribute)

    def __setitem__(self, attribute, value):
        '''
            Special method for attribute assignment
        '''
        setattr(self, attribute, value)

    def keys(self):
        '''
            Helper method for keyword unpacking purpose
        '''
        return ('product_id', 'name', 'category', 'price', 'stock', 'description', 'available')

class Transaction_Detail:
    '''
        Class which correspond to the table transaction_detail in database
    '''
    def __init__(self, transaction_id, product_id, quantity, price_at_transaction):
        self._transaction_id = transaction_id
        self._product_id = product_id
        self._quantity = quantity
        self._price_at_transaction = price_at_transaction

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

    @property
    def price_at_transaction(self):
        return self._price_at_transaction

    @price_at_transaction.setter
    def price_at_transaction(self, value):
        self._price_at_transaction = value