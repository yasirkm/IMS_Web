CREATE TABLE karyawan (
    user_id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nama TEXT NOT NULL,
    no_hp TEXT NOT NULL,
    alamat TEXT,
    Department TEXT NOT NULL
);

CREATE TABLE transaksi (
    transaction_id serial PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES karyawan(user_id),
    jenis_transaksi TEXT NOT NULL,
    no_resi TEXT,
    tanggal TIMESTAMP NOT NULL
);

CREATE TABLE barang (
    product_id serial PRIMARY KEY,
    nama TEXT NOT NULL,
    kategori TEXT NOT NULL,
    harga INTEGER NOT NULL,
    stok INTEGER NOT NULL,
    deskripsi TEXT
);

CREATE TABLE detail_transaksi (
    transaction_id INTEGER REFERENCES transaksi(transaction_id),
    product_id INTEGER REFERENCES barang(product_id),
    jumlah INTEGER NOT NULL
);

INSERT INTO barang(nama, kategori, harga, stok, deskripsi)
VALUES('Guling', 'Kamar', 30000, 3, 'Bantal guling untuk tidur');

INSERT INTO barang(nama, kategori, harga, stok, deskripsi)
VALUES('Selimut', 'Kamar', 100000, 1, 'Selimut untuk kasur');

INSERT INTO karyawan(username, password, nama, no_hp, alamat, Department)
VALUES('eric', 'hahaha', 'Eric Nur', '08122121212', 'Bandung', 'Management');

INSERT INTO karyawan(username, password, nama, no_hp, alamat, Department)
VALUES('pahrul', 'hihihi', 'Fahrul Maul', '08113123123', 'Bandung', 'Management');

INSERT INTO transaksi(user_id, jenis_transaksi, no_resi, tanggal)
VALUES(1, 'PEMASOKAN', '6801000042069', '15-10-2022');

INSERT INTO transaksi(user_id, jenis_transaksi, no_resi, tanggal)
VALUES(2, 'PEMASOKAN', '6801000042179', '22-02-2022');

INSERT INTO detail_transaksi(transaction_id, product_id, jumlah)
VALUES(1, 1, 3);

INSERT INTO detail_transaksi(transaction_id, product_id, jumlah)
VALUES(2, 2, 1);