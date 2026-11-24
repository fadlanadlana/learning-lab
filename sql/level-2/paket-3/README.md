# paket-3 - Kunjungan pelanggan per kanal (window function) (SQL level 2)

Set latihan SQL level 2. Fokus: subquery, CTE, JOIN bertingkat, window function.

## Isi

| Path | Fungsi |
|---|---|
| `../latihan/paket-3-soal.md` | 12 soal + hasil yang diharapkan |
| `../latihan/paket-3-jawaban.sql` | **kamu tulis query di sini** |
| `pendukung/cek_jawaban.py` | penilai otomatis |
| `pendukung/data/*.csv` | 2 tabel: `kunjungan` (24 baris), `pelanggan` (8 baris) |

Soal & jawaban semua set level 2 dikumpulkan di `sql/level-2/latihan/`.

## Cara mengerjakan

```
cd sql/level-2
unset LD_LIBRARY_PATH
python3 paket-3/pendukung/cek_jawaban.py
python3 paket-3/pendukung/cek_jawaban.py --detail 3   # kalau ada yang SALAH
```

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat.

## Data

`kunjungan` 24 baris (8 pelanggan x 3 bulan), `pelanggan` 8 baris. Total revenue 41.120.000.
