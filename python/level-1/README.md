# python/level-1 — dasar Python untuk data

Jalur Python level 1 (pemula). Tanpa pandas — sengaja. Tujuannya menguasai dulu tipe data, list,
dict, loop, dan fungsi memakai data CSV yang sama dengan latihan spreadsheet dan SQL. pandas masuk
di level 2.

## Isi folder

| File | Fungsi |
|---|---|
| `soal.md` | 12 soal + contoh keluaran yang diharapkan |
| `jawaban.py` | **kamu isi fungsinya** (tiap fungsi punya docstring + contoh) |
| `cek_jawaban.py` | penilai otomatis: memanggil fungsimu, bandingkan dengan kunci |
| `data/*.csv` | `penjualan.csv` (60 baris), `kampanye_iklan.csv` (30), `lead.csv` (28), `master_sumber.csv` (4) |

## Cara mengerjakan

```
cd python/level-1
unset LD_LIBRARY_PATH        # hanya di Termux; di PC/Linux lewati
python3 cek_jawaban.py
```

Penilai menampilkan **KOSONG** (fungsi belum diisi / masih `raise NotImplementedError`), **BENAR**,
atau **SALAH** per soal, lalu skor. Bandingkan angka: bilangan desimal dinilai dengan toleransi
4 desimal, jadi pembulatan wajar tidak dihukum.

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat.

## Catatan

- Jangan mengubah `cek_jawaban.py`; nilai datang dari kunci di dalamnya.
- Setiap fungsi boleh kamu tambahkan fungsi bantu sendiri di `jawaban.py`.
- Setelah lulus, lanjut ke `python/level-2` (pandas: baca CSV, groupby, merge, dan otomasi laporan).
