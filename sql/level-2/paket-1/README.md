# paket-1 - Subquery, CTE, dan window function pada data penjualan (SQL level 2)

Set latihan SQL level 2. Fokus: subquery, CTE, JOIN bertingkat, window function.

## Isi

| Path | Fungsi |
|---|---|
| `../latihan/paket-1-soal.md` | 12 soal + hasil yang diharapkan |
| `../latihan/paket-1-jawaban.sql` | **kamu tulis query di sini** |
| `pendukung/cek_jawaban.py` | penilai otomatis |
| `pendukung/data/*.csv` | 4 tabel: `penjualan` (0 baris), `kampanye_iklan` (0 baris), `lead` (0 baris), `master_sumber` (0 baris) |

Soal & jawaban semua set level 2 dikumpulkan di `sql/level-2/latihan/`.

## Cara mengerjakan

```
cd sql/level-2
unset LD_LIBRARY_PATH
python3 paket-1/pendukung/cek_jawaban.py
python3 paket-1/pendukung/cek_jawaban.py --detail 3   # kalau ada yang SALAH
```

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat.

## Data

Disalin dari `sql/level-1/pendukung/data`. Angka kunci level 2 dihitung dari data yang sama, jadi hasil level 1 bisa dipakai sebagai pembanding.
