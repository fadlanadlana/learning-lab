# sql/ — jalur SQL

Latihan SQL dengan penilai otomatis. Data yang dipakai sama dengan latihan spreadsheet, jadi
angkanya bisa dibandingkan antar-tools: yang di spreadsheet dihitung `SUMIFS`, di sini diambil
dengan `GROUP BY`.

## Level tersedia

| Level | Isi | Cara menilai |
|---|---|---|
| `level-1/` | 12 soal: SELECT, WHERE, ORDER BY, agregasi, GROUP BY, HAVING, JOIN, CASE | `python3 cek_jawaban.py` |

## Cara kerja penilai

`cek_jawaban.py` memuat semua CSV di `data/` ke database SQLite di memori (stdlib, tanpa server),
membaca `jawaban.sql`, menjalankan query per soal, lalu membandingkan hasilnya dengan kunci:

- **isi hasil** yang dinilai (jumlah baris × kolom dan nilainya), nama alias bebas;
- **urutan baris** ikut diuji pada soal yang meminta `ORDER BY`;
- desimal dibandingkan dengan toleransi 4 desimal;
- status: **KOSONG** (belum diisi), **BENAR**, **SALAH**, lalu skor dan status akhir.

## Data

| File | Baris | Isi |
|---|---|---|
| `penjualan.csv` | 60 | id, tanggal, bulan, region, kanal, produk, qty, harga, diskon, revenue |
| `kampanye_iklan.csv` | 30 | tanggal, id_kampanye, nama_kampanye, kanal, impresi, klik, biaya, konversi, revenue |
| `lead.csv` | 28 | tanggal_masuk, id_lead, nama (kotor), kode_sumber, kota, status, nilai |
| `master_sumber.csv` | 4 | kode_sumber, nama_sumber, biaya_per_lead |

## Level berikutnya (belum dibuat)

- **level-2** — JOIN dua tabel ke atas, subquery, CTE, window function (`ROW_NUMBER`, `SUM OVER`),
  `RANK`, deduplikasi.
- **level-3** — desain skema, index, analisis funnel dengan kohort bulanan.
- **level-4** — study case end-to-end: data kotor → tabel bersih → metrik marketing siap lapor.

Catatan: SQLite dipakai supaya bisa jalan tanpa instalasi apa pun. Dialek yang dilatih (SELECT,
JOIN, GROUP BY, HAVING, CASE) berlaku juga di PostgreSQL/MySQL; window function menyusul di level 2.
