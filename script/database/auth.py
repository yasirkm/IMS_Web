from config import postgre_config
import connector
import psycopg2

class AuthenticationError(Exception):
    pass

def login(username, password, columns=('employee_id', 'username', 'password', 'name', 'phone_number', 'address', 'department')):
    sql_statement = f'SELECT {", ".join(columns)} FROM employee WHERE username=%s AND password=%s'

    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (username, password))

    column_values = cursor.fetchone()

    if column_values is None:
        raise AuthenticationError("username or password is incorrect!")

    employee_information= {column:value for column, value in zip(columns,column_values)}

    cursor.close()
    connection.close()

    return employee_information

def department_check(username):
    sql_statement = "SELECT * FROM karyawan"
    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    
    rows = cursor.fetchall()
    list_user = []
    department = []
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j == 1:
                list_user.append(rows[i][j])
            elif j == 6:
                department.append(rows[i][j])
    fin_list = list(zip(list_user, department))
    for i in range(len(fin_list)):
        if username in fin_list[i]:
            dep = fin_list[i][1]
        else:
            pass
    
    cursor.close()
    connection.commit()
    connection.close()
    return  dep
    
def show_information():
    sql_statement = "SELECT * FROM barang"
    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    
    rows = cursor.fetchall()
    id_produk = []
    nama_barang = []
    kategori_barang = []
    harga_barang = []
    stok = []
    deskripsi = []
    print(len(rows))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j == 0:
                id_produk.append(rows[i][j])
            elif j == 1:
                nama_barang.append(rows[i][j])
            elif j == 2:
                kategori_barang.append(rows[i][j])
            elif j == 3:
                harga_barang.append(rows[i][j])
            elif j == 4:
                stok.append(rows[i][j])
            elif j == 5:
                deskripsi.append(rows[i][j])
    print(id_produk)
    print(nama_barang)
    print(kategori_barang)
    print(harga_barang)
    print(stok)
    print(deskripsi)
                       
    cursor.close()
    connection.commit()
    connection.close()
    pass
