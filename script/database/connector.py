from datetime import datetime

import psycopg2

from config import postgre_config
from privileges import *

IN = 'IN'
OUT = 'OUT'
TRANSACTIONS = (IN, OUT)

CONNECTION_PARAMS = postgre_config()

def add_product(employee, product):
    department = employee.get_department()
    name = product.name
    category = product.category
    price = product.price
    description = product.description

    user_privilege = EDIT_PRIVILEGES[department]
    if not user_privilege&CATALOG:
        raise PermissionError("User doesn't have the privilege")

    sql_statement = 'INSERT into product(name, category, price, stock, description) VALUES(%s,%s,%s,0,%s);'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (name, category, price, description))

    cursor.close()
    connection.commit()
    connection.close()

def _update_product_stock_by(product, quantity):
    product_id = product.product_id
    sql_statement = "UPDATE product SET stock=stock+%s WHERE product_id=%s;"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (quantity, product_id))

    cursor.close()
    connection.commit()
    connection.close()

def _add_transaction_detail(transaction_id, product, quantity):
    '''
        Insert a transaction detail
    '''
    product_id = product.product_id

    sql_statement = 'INSERT INTO transaction_detail(transaction_id, product_id, quantity) VALUES(%s, %s, %s)'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (transaction_id, product_id, quantity))

    cursor.close()
    connection.commit()
    connection.close()

def _add_transaction_record(employee, receipt_number, transaction_type):
    '''
        Insert a transaction record and return its transaction_id
    '''
    employee_id = employee.get_employee_id()

    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

    sql_statement = 'INSERT INTO transaction(employee_id, type, receipt_number, date_time) VALUES(%s, %s, %s, %s) RETURNING transaction_id'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (employee_id, transaction_type, receipt_number, date_time))
    transaction_id = cursor.fetchone()[0]

    cursor.close()
    connection.commit()
    connection.close()

    return transaction_id

def transact(employee, receipt_number, transaction_details, transaction_type):
    '''
        Do a transaction. Update the database in accordance to transaction details and transaction type
        
        transaction_details: a tuple of product_id an its quantity
        transaction_type: IN or OUT
    '''
    transaction_id = _add_transaction_record(employee, receipt_number, transaction_type)

    for product, quantity in transaction_details:
        _add_transaction_detail(transaction_id, product, quantity)
        quantity = -quantity if transaction_type == OUT else quantity
        _update_product_stock_by(product, quantity)

def get_product_information(employee, product_id):
    department = employee.get_department()

    privilege_attribute = {
        PRODUCT_NAME:'name',
        PRODUCT_CATEGORY:'category',
        PRODUCT_PRICE:'price',
        PRODUCT_STOCK:'stock',
        PRODUCT_DESCRIPTION:'description'
    }
    user_privilege = INFO_PRIVILEGES[department]

    query_attributez = [attribute for privilege, attribute in privilege_attribute.items() if user_privilege&privilege]

    sql_statement = f'SELECT product_id, {", ".join(query_attributez)} FROM product WHERE product_id={product_id}'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    product_information=cursor.fetchone()

    cursor.close()
    connection.close()

    return product_information

def get_catalog(employee):
    department = employee.get_department()

    privilege_attribute = {
        PRODUCT_NAME:'name',
        PRODUCT_CATEGORY:'category',
        PRODUCT_PRICE:'price',
        PRODUCT_STOCK:'stock',
        PRODUCT_DESCRIPTION:'description'
    }
    user_privilege = INFO_PRIVILEGES[department]

    query_attributez = [attribute for privilege, attribute in privilege_attribute.items() if user_privilege&privilege]

    sql_statement = f'SELECT product_id, {", ".join(query_attributez)} FROM product ORDER BY product_id'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    catalog=cursor.fetchall()

    cursor.close()
    connection.close()

    return catalog

def get_transactions(employee):
    department = employee.get_department()

    user_privilege = INFO_PRIVILEGES[department]
    if not user_privilege&TRANSACTION:
        raise PermissionError("User doesn't have the privilege")

    sql_statement = "SELECT * from transaction"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def get_transaction_details(transaction_id):
    sql_statement = f"SELECT * FROM transaction_detail WHERE transaction_id={transaction_id}"
    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    transaction_details = cursor.fetchall()
    cursor.close()
    connection.close()


def edit_product_information(employee, product, name=None, category=None, description=None, price=None):
    product_id = product.product_id
    department = employee.get_department()
    privilege_attribute = {
        PRODUCT_NAME:'name',
        PRODUCT_CATEGORY:'category',
        PRODUCT_DESCRIPTION:'description',
        PRODUCT_PRICE:'price'
    }
    attribute_edit_value = {
        'name':name,
        'category':category,
        'description':description,
        'price':price
    }

    user_privilege = EDIT_PRIVILEGES[department]
    edit_attributes = [attribute for privilege, attribute in privilege_attribute.items() if user_privilege&privilege and attribute_edit_value[attribute] is not None]
    sql_statement = f'UPDATE product SET {", ".join(f"{attribute}=%s" for attribute in edit_attributes)} WHERE product_id={product_id}'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, tuple(attribute_edit_value[attribute] for attribute in edit_attributes))
    cursor.close()
    connection.commit()
    connection.close()