import psycopg2

from database.config import postgre_config
from database.privileges import *


'''
    An interface for the purpose of communicating with the database
'''
class TableNotFoundError(Exception):
    pass

IN = 'IN'
OUT = 'OUT'
TRANSACTIONS = (IN, OUT)

CONNECTION_PARAMS = postgre_config()

def add_product(name, category, price, description):
    '''
        Add a new record to product table.
        Return product_id of added product.
    '''

    sql_statement = 'INSERT INTO product(name, category, price, stock, description, available) VALUES(%s,%s,%s,%s,%s,%s) RETURNING product_id;'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (name, category, price, 0, description, True))

    product_id = cursor.fetchone()[0]

    cursor.close()
    connection.commit()
    connection.close()

    return product_id


def transact(employee_id, receipt_number, transaction_details, transaction_type, date_time):
    '''
        Do a transaction. Update the database in accordance to transaction details and transaction type.
        Return transaction_id of transaction done.
        
        transaction_details: a tuple of product_id an its quantity
        transaction_type: 'IN' or 'OUT'
    '''
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
            add a new record for transaction_detail.
        '''

        sql_statement = 'INSERT INTO transaction_detail(transaction_id, product_id, quantity) VALUES(%s, %s, %s)'
        cursor.execute(sql_statement, (transaction_id, product_id, quantity))

    def _add_transaction_record(employee_id, receipt_number, transaction_type, date_time):
        '''
            add a new record for transaction.
            Return transaction_id of the added transaction
        '''
        sql_statement = 'INSERT INTO transaction(employee_id, type, receipt_number, date_time) VALUES(%s, %s, %s, %s) RETURNING transaction_id'

        cursor.execute(sql_statement, (employee_id, transaction_type, receipt_number, date_time))
        transaction_id = cursor.fetchone()[0]

        return transaction_id
    

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()

    transaction_id = _add_transaction_record(employee_id, receipt_number, transaction_type, date_time)

    # Adding transaction_detail record for each transaction_details
    for product_id, quantity in transaction_details:
        _add_transaction_detail(transaction_id, product_id, quantity)
        quantity = -quantity if transaction_type == OUT else quantity
        _update_product_stock_by(product_id, quantity)

    cursor.close()
    connection.commit()
    connection.close()
    return transaction_id

def get_product_information(product_id, columns=('product_id', 'name', 'category', 'price', 'stock', 'description', 'available')):
    '''
        Return an attribute dictionary of product with the product_id in database.
    '''

    sql_statement = f'SELECT {", ".join(columns)} FROM product WHERE product_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (product_id,))

    column_values = cursor.fetchone()

    # Raise an exception if query results in None
    if column_values is None:
        raise TableNotFoundError(f'The product with the id of {product_id} could not be found in the database')

    product_information= {column:value for column, value in zip(columns,column_values)}

    cursor.close()
    connection.close()

    return product_information

def get_transaction_information(transaction_id, columns=('transaction_id', 'employee_id', 'type', 'receipt_number', 'date_time')):
    '''
        Return an attribute dictionary of transaction with the transaction_id in database.
    '''
    sql_statement = f'SELECT {", ".join(columns)} FROM transaction WHERE transaction_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (transaction_id,))

    column_values = cursor.fetchone()

    # Raise an exception if query results in None
    if column_values is None:
        raise TableNotFoundError(f'The transaction with the id of {transaction_id} could not be found in the database')

    transaction_information= {column:value for column, value in zip(columns,column_values)}

    cursor.close()
    connection.close()

    return transaction_information

def get_transaction_details(transaction_id, columns=('transaction_id', 'product_id', 'quantity')):
    '''
        Return a list of attribute dictionary of transaction_details with the transaction_id in database.
    '''
    sql_statement = f'SELECT {", ".join(columns)} FROM transaction_detail WHERE transaction_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (transaction_id,))

    transaction_detail_list = []
    result = cursor.fetchall()
    # Raise an exception if query results in None

    if result is None:
        raise TableNotFoundError(f'The transaction with the id of {transaction_id} could not be found in the database')
    
    # Creating list of transaction details
    for values in result:
        transaction_detail = {column:value for column, value in zip(columns, values)}
        transaction_detail_list.append(transaction_detail)

    cursor.close()
    connection.close()

    return transaction_detail_list

def get_catalog(columns=('product_id', 'name', 'category', 'price', 'stock', 'description')):
    '''
        Return a list of attribute dictionary of available product in database.
    '''
    sql_statement = f'SELECT {", ".join(columns)} FROM product WHERE available IS TRUE ORDER BY product_id'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    result=cursor.fetchall()

    catalog = []
    for product_information in result:
        catalog.append({column:value for column, value in zip(columns, product_information)})

    cursor.close()
    connection.close()

    return catalog

def get_transactions(columns=('transaction_id', 'employee_id', 'type', 'receipt_number', 'date_time')):
    '''
        Return a list of attribute dictionary of transactions in database
    '''
    sql_statement = f"SELECT {', '.join(columns)} FROM transaction ORDER BY transaction_id"

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    result = cursor.fetchall()

    transactions = []
    for transaction_information in result:
        transactions.append({column:value for column, value in zip(columns, transaction_information)})

    cursor.close()
    connection.close()

    return transactions

def edit_product_information(product_id, name=None, category=None, description=None, stock=None, price=None, available=None):
    '''
        Edit the information of product with given value.
    '''

    attribute_edit_value = { # Maps attribute with parameter
        'name':name,
        'category':category,
        'description':description,
        'price':price,
        'stock':stock,
        'available':available
    }
    # Filtering un-edited attribute
    edit_attributes = [attribute for attribute in attribute_edit_value if attribute_edit_value[attribute] is not None]

    sql_statement = f'UPDATE product SET {", ".join(f"{attribute}=%s" for attribute in edit_attributes)} WHERE product_id=%s'

    connection = psycopg2.connect(**CONNECTION_PARAMS)
    cursor = connection.cursor()
    cursor.execute(sql_statement, tuple(attribute_edit_value[attribute] for attribute in edit_attributes)+(product_id,))
    cursor.close()
    connection.commit()
    connection.close()

def register(username, password, name, phone_number, address, department):
    '''
        Add a new record for employee table in database.
        Return employee_id of added employee.
    '''
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
