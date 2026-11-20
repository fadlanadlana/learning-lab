# sql/level-1 — dasar SQL (SELECT, WHERE, GROUP BY, JOIN)

Jalur SQL level 1 (pemula). Semua dikerjakan terhadap data yang sama dengan latihan spreadsheet,
sehingga terasa kaitannya: angka yang dulu dihitung dengan SUMIFS sekarang diambil dengan query.

## Struktur folder

Semua soal dan jawaban dikumpulkan di satu folder `latihan/`, satu berkas per paket. Sisanya
(penilai + CSV) ada di `pendukung/` masing-masing paket dan tidak perlu dibuka.

```
level-1/
├── latihan/                        <- satu-satunya folder yang perlu dibuka
│   ├── level-1-soal.md             12 soal + hasil yang diharapkan (kolom & urutan)
│   ├── level-1-jawaban.sql         KAMU tulis query di sini
│   ├── paket-2-soal.md             paket funnel website
│   ├── paket-2-jawaban.sql
│   ├── paket-3-soal.md             paket repeat order
│   ├── paket-3-jawaban.sql
│   ├── paket-4-soal.md             paket biaya iklan & CPL
│   ├── paket-4-jawaban.sql
│   ├── paket-5-soal.md             paket penjualan produk & stok
│   └── paket-5-jawaban.sql
├── pendukung/                      <- level-1: penilai, coba.py, data
│   ├── cek_jawaban.py
│   ├── coba.py
│   └── data/*.csv                  4 tabel: penjualan (60), kampanye_iklan (30), lead (28), master_sumber (4)
├── paket-2/ … paket-5/             <- masing-masing hanya berisi pendukung/ (penilai + data paket)
├── _tools/gen_paket.py             generator paket-2..paket-5
└── README.md                       halaman ini
```

Penilai mencari `<set>-jawaban.sql` di folder `latihan/` bersama dan `pendukung/data/` miliknya sendiri,
dihitung dari lokasi file skripnya — bukan dari folder tempat kamu berdiri — jadi `python3 pendukung/cek_jawaban.py` jalan dari folder mana pun.

## Cara mengerjakan

```
cd sql/level-1
unset LD_LIBRARY_PATH                # hanya di Termux; di PC/Linux lewati baris ini
python3 pendukung/cek_jawaban.py     # jalankan penilai
```

Penilai menampilkan status **KOSONG** (belum diisi), **BENAR**, atau **SALAH** per soal, lalu skor.
Semua soal dijalankan di database SQLite sementara yang dibangun ulang dari CSV setiap kali dijalankan,
jadi kamu boleh mengubah data, tapi angka kunci ikut berubah.

Mau mencoba query tanpa menyentuh `jawaban.sql`:

```
python3 pendukung/coba.py "SELECT * FROM penjualan LIMIT 5"   # hanya ada di level-1
```

Kalau satu soal tetap SALAH dan kamu tidak tahu sebabnya, periksa detailnya:

```
python3 pendukung/cek_jawaban.py --detail 11
```

Perintah itu menampilkan query kamu apa adanya, hasil yang keluar, kunci beserta hasil kunci, dan
kesimpulan: isi beda, hanya urutan beda, atau query error.

Urutan pengerjaan yang disarankan: soal 1-6 (SELECT, WHERE, agregasi), 7-9 (GROUP BY, HAVING),
10 (JOIN), 11-12 (CASE dan subquery/menyaring hasil agregat).

Catatan teknis: CSV dimuat dengan tipe kolom eksplisit (`INTEGER`/`REAL`/`TEXT`, lihat `SKEMA` di
`pendukung/cek_jawaban.py`). Kalau kolom angka dimuat tanpa tipe, SQLite memberi TEXT affinity dan
`ORDER BY revenue DESC` akan mengurutkan secara abjad — jadi kalau kamu memuat CSV ini sendiri di
tempat lain, deklarasikan tipenya juga.

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris × kolom), bukan nama alias kolom. Jadi `AS total` boleh apa saja.
- **Urutan baris** hanya diuji pada soal yang memang meminta `ORDER BY` (ditandai di `soal.md`).
- Angka desimal dibandingkan dengan toleransi 4 desimal.

## Paket latihan tambahan (data sendiri, tema marketing & sales)

Folder di bawah ini **mandiri**: dataset berbeda, 12 soal, penilai sendiri, dan struktur folder sama
(`latihan/` + `pendukung/`). Tingkat kesulitannya sama dengan level-1 di atas, jadi bisa dikerjakan
kapan saja tanpa mengubah `soal.md` di folder ini.

| Paket | Tema | Tabel (di `pendukung/data/`) |
|---|---|---|
| `paket-2/` | Funnel website per kanal | `trafik` (24), `kanal_master` (6) |
| `paket-3/` | Repeat order pelanggan | `pesanan` (24), `pelanggan` (10), `ongkir` (5) |
| `paket-4/` | Biaya iklan & CPL per platform | `iklan_harian` (24), `platform_master` (4) |
| `paket-5/` | Penjualan produk & status stok | `penjualan_produk` (24), `produk` (12) |

Cara pakai sama: masuk ke foldernya, lalu `unset LD_LIBRARY_PATH; python3 pendukung/cek_jawaban.py`.

Berkas paket dihasilkan oleh `_tools/gen_paket.py`. Kalau kamu mengubah CSV atau soal langsung,
jangan jalankan generator lagi dari situ — ubah dulu definisi di generator, karena generator menimpa
`latihan/soal.md`, `latihan/jawaban.sql`, `pendukung/cek_jawaban.py`, dan `README.md` tiap paket
(jawaban yang sudah kamu tulis ikut tertimpa).

Setelah lulus, lanjut ke `sql/level-2` (JOIN bertingkat, subquery, CTE, window function).
