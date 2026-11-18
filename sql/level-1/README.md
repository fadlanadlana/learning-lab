# sql/level-1 — dasar SQL (SELECT, WHERE, GROUP BY, JOIN)

Jalur SQL level 1 (pemula). Semua dikerjakan terhadap data yang sama dengan latihan spreadsheet,
sehingga terasa kaitannya: angka yang dulu dihitung dengan SUMIFS sekarang diambil dengan query.

## Isi folder

| File | Fungsi |
|---|---|
| `soal.md` | 12 soal + hasil yang diharapkan (kolom & urutan) |
| `jawaban.sql` | **kamu tulis query di sini**, di bawah tiap penanda `-- === SOAL n ===` |
| `cek_jawaban.py` | penilai otomatis: memuat CSV ke SQLite, menjalankan querymu, bandingkan dengan kunci |
| `coba.py` | uji query langsung tanpa mengubah `jawaban.sql`: `python3 coba.py "SELECT * FROM penjualan LIMIT 5"` |
| `data/*.csv` | 4 tabel: `penjualan` (60 baris), `kampanye_iklan` (30), `lead` (28), `master_sumber` (4) |

## Cara mengerjakan

```
cd sql/level-1
unset LD_LIBRARY_PATH            # hanya di Termux; di PC/Linux lewati baris ini
python3 cek_jawaban.py           # jalankan penilai
```

Penilai menampilkan status **KOSONG** (belum diisi), **BENAR**, atau **SALAH** per soal, lalu skor.
Semua soal dijalankan di database SQLite sementara yang dibangun ulang dari CSV setiap kali dijalankan,
jadi kamu boleh mengubah data, tapi angka kunci ikut berubah.

Urutan pengerjaan yang disarankan: soal 1-6 (SELECT, WHERE, agregasi), 7-9 (GROUP BY, HAVING),
10 (JOIN), 11-12 (CASE dan subquery/menyaring hasil agregat).

Catatan teknis: CSV dimuat dengan tipe kolom eksplisit (`INTEGER`/`REAL`/`TEXT`, lihat `SKEMA` di
`cek_jawaban.py`). Kalau kolom angka dimuat tanpa tipe, SQLite memberi TEXT affinity dan
`ORDER BY revenue DESC` akan mengurutkan secara abjad — jadi kalau kamu memuat CSV ini sendiri di
tempat lain, deklarasikan tipenya juga.

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris × kolom), bukan nama alias kolom. Jadi `AS total` boleh apa saja.
- **Urutan baris** hanya diuji pada soal yang memang meminta `ORDER BY` (ditandai di `soal.md`).
- Angka desimal dibandingkan dengan toleransi 4 desimal.

## Paket latihan tambahan (data sendiri, tema marketing & sales)

Folder di bawah ini **mandiri**: dataset berbeda, 12 soal, penilai sendiri. Tingkat kesulitannya sama
dengan level-1 di atas, jadi bisa dikerjakan kapan saja tanpa mengubah `soal.md` di folder ini.

| Paket | Tema | Tabel |
|---|---|---|
| `paket-2/` | Funnel website per kanal | `trafik` (24), `kanal_master` (6) |
| `paket-3/` | Repeat order pelanggan | `pesanan` (24), `pelanggan` (10), `ongkir` (5) |
| `paket-4/` | Biaya iklan & CPL per platform | `iklan_harian` (24), `platform_master` (4) |
| `paket-5/` | Penjualan produk & status stok | `penjualan_produk` (24), `produk` (12) |

Cara pakai sama: masuk ke foldernya, lalu `unset LD_LIBRARY_PATH; python3 cek_jawaban.py`.

Berkas paket dihasilkan oleh `_tools/gen_paket.py`. Kalau kamu mengubah CSV atau soal langsung,
jangan jalankan generator lagi dari situ — jalankan setelah mengubah definisi di generator, karena
generator menimpa `soal.md`, `jawaban.sql`, `cek_jawaban.py`, dan README tiap paket.

Setelah lulus, lanjut ke `sql/level-2` (JOIN bertingkat, subquery, CTE, window function).
