# paket-5 — Penjualan produk dan status stok

Paket soal SQL level 1 (mandiri, data sendiri). Tingkat kesulitan sama dengan `../level-1`:
SELECT, WHERE, ORDER BY, LIMIT, agregasi, GROUP BY, HAVING, satu JOIN, CASE, DISTINCT, LIKE, IN.

## Isi folder

Dua folder: yang kamu sentuh dan yang tidak.

| Path | Fungsi |
|---|---|
| `../latihan/paket-5-soal.md` | 12 soal + hasil yang diharapkan (kolom & urutan) |
| `../latihan/paket-5-jawaban.sql` | **kamu tulis query di sini**, di bawah tiap penanda `-- === SOAL n ===` |
| `pendukung/cek_jawaban.py` | penilai otomatis: CSV -> SQLite, querymu dijalankan, dibandingkan dengan kunci |
| `pendukung/data/*.csv` | 2 tabel: `penjualan_produk` (24 baris), `produk` (12 baris) |

Soal & jawaban semua paket dikumpulkan di `sql/level-1/latihan/`, satu berkas per paket.
Isi `pendukung/` (penilai + CSV) jangan diedit.

## Cara mengerjakan

```
cd sql/level-1/paket-5
unset LD_LIBRARY_PATH            # hanya di Termux; di PC/Linux lewati baris ini
python3 pendukung/cek_jawaban.py # jalankan penilai
```

Penilai menampilkan **KOSONG**, **BENAR**, atau **SALAH** per soal, lalu skor.
Database dibangun ulang dari CSV setiap kali dijalankan. Penilai mencari
`latihan/paket-5-jawaban.sql` dan `pendukung/data/` dari lokasi file skripnya, jadi boleh dijalankan
dari folder mana pun.

Kalau satu soal tetap SALAH dan kamu tidak tahu sebabnya, periksa detailnya:

```
python3 pendukung/cek_jawaban.py --detail 11
```

Perintah itu menampilkan query kamu apa adanya, hasil yang keluar, kunci beserta hasil kunci, dan
kesimpulan: isi beda, hanya urutan beda, atau query error.

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris x kolom), bukan nama alias kolom.
- **Urutan baris** hanya diuji pada soal yang meminta `ORDER BY`.
- Angka dibandingkan dengan toleransi 4 desimal.

## Data

`penjualan_produk` 24 baris (2026-08 s/d 2026-10); `produk` 12 baris, `SKU-11` dan `SKU-12` sengaja belum pernah terjual.
