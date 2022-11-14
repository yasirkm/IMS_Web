from datetime import datetime

import psycopg2

from config import postgre_config

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



if __name__ == '__main__':
    add_product('pillow', 'kamar', 200000, 'bantal untuk kamar')
    transact(1, None, ((1,3),(2,3)), IN)
    transact(1, None, ((1,2),(2,2)), OUT)