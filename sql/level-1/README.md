# sql/level-1 — dasar SQL (SELECT, WHERE, GROUP BY, JOIN)

Jalur SQL level 1 (pemula). Semua dikerjakan terhadap data yang sama dengan latihan spreadsheet,
sehingga terasa kaitannya: angka yang dulu dihitung dengan SUMIFS sekarang diambil dengan query.

## Struktur folder

Tiap folder latihan (`level-1/`, `paket-2/` … `paket-5/`) bentuknya sama: satu folder untuk yang
kamu kerjakan, satu folder untuk penunjangnya. Hanya `latihan/` yang perlu dibuka.

```
level-1/
├── latihan/                 <- buka ini
│   ├── soal.md              12 soal + hasil yang diharapkan (kolom & urutan)
│   └── jawaban.sql          KAMU tulis query di sini, di bawah tiap `-- === SOAL n ===`
├── pendukung/               <- jangan diedit
│   ├── cek_jawaban.py       penilai otomatis: CSV -> SQLite, querymu dijalankan, dibandingkan kunci
│   ├── coba.py              uji query langsung tanpa mengubah jawaban.sql
│   └── data/*.csv           4 tabel: penjualan (60 baris), kampanye_iklan (30), lead (28), master_sumber (4)
├── _tools/gen_paket.py      generator paket-2..paket-5
└── README.md                halaman ini
```

Penilai mencari `latihan/jawaban.sql` dan `pendukung/data/` dari lokasi file skripnya, bukan dari
folder tempat kamu berdiri — jadi `python3 pendukung/cek_jawaban.py` jalan dari folder mana pun.

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
python3 pendukung/coba.py "SELECT * FROM penjualan LIMIT 5"
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
