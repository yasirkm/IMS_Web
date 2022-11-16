from datetime import datetime

import psycopg2

from config import postgre_config
from privileges import *

IN = 'IN'
OUT = 'OUT'
TRANSACTIONS = (IN, OUT)

CONNECTION_PARAMS = postgre_config()

def add_product(name, category, price=0, description=None):
    sql_statement = 'INSERT into product(name, category, price, stock, description) VALUES(%s,%s,%s,0,%s);'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (name, category, price, description))

    cursor.close()
    connection.commit()
    connection.close()

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

def get_product_information(product_id, department):
    privilege_attribute = {
        PRODUCT_NAME:'name',
        PRODUCT_CATEGORY:'category',
        PRODUCT_DESCRIPTION:'description',
        PRODUCT_PRICE:'price',
        PRODUCT_STOCK:'stock'
    }
    user_privilege = INFO_PRIVILEGES[department]

    query_attributez = [attribute for privilege, attribute in privilege_attribute.items() if user_privilege&privilege]

    sql_statement = f'SELECT {", ".join(query_attributez)} FROM product WHERE product_id={product_id}'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    product_information=cursor.fetchone()

    cursor.close()
    connection.close()

    return product_information

def edit_product_information(product_id, department, name=None, category=None, description=None, price=None):
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
    sql_statement = f'UPDATE product SET {", ".join(f"{attribute}={attribute_edit_value[attribute]}" for attribute in edit_attributes)} WHERE product_id={product_id}'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    cursor.close()
    connection.commit()
    connection.close()


if __name__ == '__main__':
    # add_product('pillow', 'kamar', 200000, 'bantal untuk kamar')
    # transact(1, None, ((1,3),(2,3)), IN)
    # transact(1, None, ((1,2),(2,2)), OUT)
    print(get_product_information(1, 'Management'))
    print(get_product_information(1, 'Development'))