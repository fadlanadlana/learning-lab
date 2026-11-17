# python/ — jalur Python

Latihan Python untuk pekerjaan data, dengan penilai otomatis. Level 1 sengaja **tanpa pandas**:
tipe data, list, dict, loop, dan fungsi dilatih dulu memakai data CSV yang sama dengan jalur
spreadsheet dan SQL.

## Level tersedia

| Level | Isi | Modul | Cara menilai |
|---|---|---|---|
| `level-1/` | 12 fungsi: baca CSV, agregasi, dict, sorting, string cleaning | stdlib (`csv`) | `python3 cek_jawaban.py` |

## Cara kerja penilai

`cek_jawaban.py` memuat datanya sendiri dari `data/`, mengimpor `jawaban.py`, memanggil tiap fungsi
dengan argumen yang ditentukan, lalu membandingkan hasilnya dengan kunci:

- **KOSONG** bila fungsi masih `raise NotImplementedError`;
- **SALAH** bila hasil beda tipe/nilai, atau fungsinya melempar error (pesan error ikut ditampilkan);
- **BENAR** bila cocok (angka desimal toleransi 4 desimal).

## Data

Sama dengan jalur SQL: `penjualan.csv` (60 baris), `kampanye_iklan.csv` (30), `lead.csv` (28),
`master_sumber.csv` (4). Kolom `nama` di `lead.csv` sengaja kotor untuk soal pembersihan string.

## Level berikutnya (belum dibuat)

- **level-2** — pandas: `read_csv`, `groupby`, `merge`, `pivot_table`, tanggal, ekspor ke Excel.
- **level-3** — otomasi: baca banyak file, validasi skema, buat laporan Excel/PNG otomatis.
- **level-4** — pipeline data end-to-end: ekstrak → bersihkan → analisis → kirim laporan.

Prasyarat level 1: Python 3.10+ saja. Tidak perlu `pip install` apa pun.
