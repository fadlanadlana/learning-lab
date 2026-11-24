# sql/level-2 — SQL lanjutan (subquery, CTE, JOIN bertingkat, window function)

Lanjutan dari `../level-1`. Tingkat soalnya naik, bentuk berkasnya sama: semua soal dan jawaban
dikumpulkan di satu folder `latihan/`, penilai + data di `pendukung/` tiap set.

## Struktur folder

```
level-2/
├── latihan/                        <- satu-satunya folder yang perlu dibuka
│   ├── paket-1-soal.md             12 soal + hasil yang diharapkan
│   ├── paket-1-jawaban.sql         KAMU tulis query di sini
│   ├── paket-2-soal.md             pesanan/item/produk, JOIN bertingkat
│   ├── paket-2-jawaban.sql
│   ├── paket-3-soal.md             kunjungan pelanggan, window function
│   └── paket-3-jawaban.sql
├── paket-1/ … paket-3/             <- masing-masing hanya pendukung/ (penilai + data set itu)
│   ├── cek_jawaban.py
│   └── data/*.csv
├── _tools/gen_paket.py             generator ketiga set
└── README.md                       halaman ini
```

## Isi tiap set

| Set | Data | Fokus |
|---|---|---|
| `paket-1` | 4 tabel level-1: `penjualan` (60), `kampanye_iklan` (30), `lead` (28), `master_sumber` (4) | subquery skalar, `IN`, `EXISTS`/`NOT EXISTS`, derived table, CTE, `ROW_NUMBER`, `LAG`, running total, window `SUM` di atas agregat, subquery berkorelasi |
| `paket-2` | `pesanan` (20), `item_pesanan` (30), `produk` (9) | JOIN 3 tabel, nilai pesanan = SUM(qty x harga), margin, `NOT EXISTS`, CTE + agregat, `ROW_NUMBER` per kategori, kontribusi persen |
| `paket-3` | `kunjungan` (24), `pelanggan` (8) | `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `LAG`, `SUM/AVG OVER`, `FIRST_VALUE`, `PARTITION BY` |

Data `paket-1` sengaja sama dengan level-1: yang dilatih tekniknya, bukan data baru, jadi hasil level-1
bisa dipakai sebagai pembanding.

## Cara mengerjakan

```
cd sql/level-2
unset LD_LIBRARY_PATH                # hanya di Termux
python3 paket-1/pendukung/cek_jawaban.py
python3 paket-2/pendukung/cek_jawaban.py
python3 paket-3/pendukung/cek_jawaban.py
```

Kalau ada yang SALAH, lihat detailnya (query kamu, hasilnya, kunci, dan kesimpulan):

```
python3 paket-1/pendukung/cek_jawaban.py --detail 8
```

Penilai mencari `<set>-jawaban.sql` di folder `latihan/` bersama dan `pendukung/data/` miliknya
sendiri, dihitung dari lokasi file skripnya — jadi bisa dijalankan dari folder mana pun.

## Kriteria lulus

12/12 BENAR per set. 10-11 benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris x kolom), bukan nama alias kolom.
- **Urutan baris** hanya diuji pada soal yang meminta `ORDER BY`; kalau ada nilai kembar, soal
  menyebut kolom penentu urutan berikutnya.
- Angka dibandingkan dengan toleransi 4 desimal.

## Catatan teknis

CSV dimuat dengan tipe kolom eksplisit (`INTEGER`/`REAL`/`TEXT`, lihat `SKEMA` di tiap
`pendukung/cek_jawaban.py`). Tanpa itu SQLite memberi TEXT affinity dan `ORDER BY revenue DESC`
akan mengurutkan secara abjad. Window function dan CTE didukung SQLite versi yang dipakai di sini.

Setelah lulus ketiga set, lanjut ke materi database nyata: file `.db`, transaksi, index, lalu
menyambung dari Python (`sqlite3`/`psycopg`).
