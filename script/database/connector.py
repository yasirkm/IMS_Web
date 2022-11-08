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

if __name__ == '__main__':
    add_product('pillow', 'kamar', 200000, 'bantal untuk kamar')