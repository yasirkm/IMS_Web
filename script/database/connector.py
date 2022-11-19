from datetime import datetime

import psycopg2

from config import postgre_config
from privileges import *

class ProductNotFoundError(Exception):
    pass

IN = 'IN'
OUT = 'OUT'
TRANSACTIONS = (IN, OUT)

CONNECTION_PARAMS = postgre_config()

def add_product(name, category, price, description):

    sql_statement = 'INSERT into product(name, category, price, stock, description) VALUES(%s,%s,%s,0,%s) RETURNING product_id;'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (name, category, price, description))

    product_id = cursor.fetchone()[0]

    cursor.close()
    connection.commit()
    connection.close()

    return product_id

def _update_product_stock_by(product_id, quantity):
    sql_statement = "UPDATE product SET stock=stock+%s WHERE product_id=%s;"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (quantity, product_id))

    cursor.close()
    connection.commit()
    connection.close()

def _add_transaction_detail(transaction_id, product_id, quantity):
    '''
        Insert a transaction detail
    '''

    sql_statement = 'INSERT INTO transaction_detail(transaction_id, product_id, quantity) VALUES(%s, %s, %s)'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (transaction_id, product_id, quantity))

    cursor.close()
    connection.commit()
    connection.close()

def _add_transaction_record(employee_id, receipt_number, transaction_type):
    '''
        Insert a transaction record and return its transaction_id
    '''

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

def transact(employee_id, receipt_number, transaction_details, transaction_type):
    '''
        Do a transaction. Update the database in accordance to transaction details and transaction type
        
        transaction_details: a tuple of product_id an its quantity
        transaction_type: IN or OUT
    '''
    transaction_id = _add_transaction_record(employee_id, receipt_number, transaction_type)

    for product_id, quantity in transaction_details:
        _add_transaction_detail(transaction_id, product_id, quantity)
        quantity = -quantity if transaction_type == OUT else quantity
        _update_product_stock_by(product_id, quantity)

def get_product_information(product_id, columns=('product_id', 'name', 'category', 'price', 'stock', 'description')):

    sql_statement = f'SELECT {", ".join(columns)} FROM product WHERE product_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (product_id,))

    column_values = cursor.fetchone()
    if column_values is None:
        raise ProductNotFoundError(f'The product with the id of {product_id} could not be found in the database')

    product_information= {column:value for column, value in zip(columns,column_values)}

    cursor.close()
    connection.close()

    return product_information

def get_catalog(columns=('product_id', 'name', 'category', 'price', 'stock', 'description')):

    sql_statement = f'SELECT {", ".join(columns)} FROM product ORDER BY product_id'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    catalog=cursor.fetchall()

    cursor.close()
    connection.close()

    return catalog

def get_transactions(columns=('transaction_id', 'employee_id', 'type', 'receipt_number', 'date_time')):
    sql_statement = f"SELECT {', '.join(columns)} FROM transaction ORDER BY transaction_id"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions

def get_transaction_details(transaction_id, columns=('transaction_id', 'product_id', 'quantity')):
    sql_statement = f"SELECT {', '.join(columns)} FROM transaction_detail WHERE transaction_id=%s"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()

    cursor.execute(sql_statement, (transaction_id,))
    transaction_details = cursor.fetchall()

    cursor.close()
    connection.close()

    return transaction_details


def edit_product_information(product_id, name=None, category=None, description=None, price=None):
    attribute_edit_value = {
        'name':name,
        'category':category,
        'description':description,
        'price':price
    }
    edit_attributes = [attribute for attribute in attribute_edit_value if attribute_edit_value[attribute] is not None]
    sql_statement = f'UPDATE product SET {", ".join(f"{attribute}=%s" for attribute in edit_attributes)} WHERE product_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, tuple(attribute_edit_value[attribute] for attribute in edit_attributes)+(product_id,))
    cursor.close()
    connection.commit()
    connection.close()

def register(username, password, name, phone_number, address, department):
    sql_statement = 'INSERT INTO employee(username, password, name, phone_number, address, department) VALUES(%s,%s,%s,%s,%s,%s) RETURNING employee_id;'

    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (username, password, name, phone_number, address, department))
    employee_id = cursor.fetchone()[0]
    cursor.close()
    connection.commit()
    connection.close()
    return employee_id