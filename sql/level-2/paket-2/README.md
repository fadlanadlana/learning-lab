# paket-2 - Pesanan, item pesanan, dan produk (JOIN bertingkat) (SQL level 2)

Set latihan SQL level 2. Fokus: subquery, CTE, JOIN bertingkat, window function.

## Isi

| Path | Fungsi |
|---|---|
| `../latihan/paket-2-soal.md` | 12 soal + hasil yang diharapkan |
| `../latihan/paket-2-jawaban.sql` | **kamu tulis query di sini** |
| `pendukung/cek_jawaban.py` | penilai otomatis |
| `pendukung/data/*.csv` | 3 tabel: `pesanan` (20 baris), `item_pesanan` (30 baris), `produk` (9 baris) |

Soal & jawaban semua set level 2 dikumpulkan di `sql/level-2/latihan/`.

## Cara mengerjakan

```
cd sql/level-2
unset LD_LIBRARY_PATH
python3 paket-2/pendukung/cek_jawaban.py
python3 paket-2/pendukung/cek_jawaban.py --detail 3   # kalau ada yang SALAH
```

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat.

## Data

`pesanan` 20 baris (2026-08 s/d 2026-10), `item_pesanan` 30 baris, `produk` 9 baris. 15 pesanan berstatus Selesai, 3 Batal, 2 Proses. `SKU-I` tidak pernah terjual.
