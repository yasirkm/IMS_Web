from config import postgre_config
import psycopg2

TRANSACTIONS = ('PEMASOKAN', 'PENGELUARAN')
PEMASOKAN = 0
PENGELUARAN = 1

def add_product(name, category, price=0, description=None):
    sql_statement = 'INSERT into barang(nama, kategori, harga, stok, deskripsi) VALUES(%s,%s,%s,0,%s);'
    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (name, category, price, description))

    cursor.close()
    connection.commit()
    connection.close()

def _update_product_stock_by(amount, transaction_type, id):
    if transaction_type not in TRANSACTIONS:
        raise ValueError("Illegal transaction type")
    amount = -amount if transaction_type == TRANSACTIONS[PENGELUARAN] else amount
    sql_statement = "UPDATE barang SET stok=stok+%s WHERE product_id=%s;"

    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (amount, id))

    cursor.close()
    connection.commit()
    connection.close()

def _add_transaction_record():
    pass

def _add_transaction_detail():
    pass

def transact():
    pass

if __name__ == '__main__':
    add_product('pillow', 'kamar', 200000, 'bantal untuk kamar')
    _update_product_stock_by(5, "PEMASOKAN", 2)
    _update_product_stock_by(3, "PENGELUARAN", 2)