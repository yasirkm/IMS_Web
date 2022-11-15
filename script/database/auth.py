from config import postgre_config
import connector
import psycopg2
import plotly
import plotly.graph_objects as go

def login(username, password):
    sql_statement = "SELECT * FROM karyawan"
    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    
    rows = cursor.fetchall()

    cursor.close()
    connection.commit()
    connection.close()
    user = []
    pw = []
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j == 1:
                user.append(rows[i][j])
            elif j == 2:
                pw.append(rows[i][j])
    fin_list = list(zip(user, pw))
    for i in range(len(fin_list)):
        if username in fin_list[i]:
            if password == fin_list[i][1]:
                print("login berhasil")
            else:
                print("username atau password salah")
        else:
            pass

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

def register(username, password, name, no_hp, alamat, department):
    sql_statement = 'INSERT INTO karyawan(username, password, nama, no_hp, alamat, department) VALUES(%s,%s,%s,%s,%s,%s);'

    params = postgre_config()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute(sql_statement, (username, password, name, no_hp, alamat, department))

    cursor.close()
    connection.commit()
    connection.close()

    
    

if __name__ == '__main__':
    show_information()
    #print(department_check("tomuto"))
    username = str(input("Masukkan Username : "))
    password = str(input("Masukkan Password : "))
    nama = str(input("Masukkan nama : "))
    no_hp = str(input("Masukkan Nomor Handphone : "))
    alamat = str(input("Masukkan Alamat : "))
    department = str(input("Masukkan Department : "))

    register(username, password, nama, no_hp, alamat, department)

    #login(username, password)
