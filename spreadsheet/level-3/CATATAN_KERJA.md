# Catatan Kerja — spreadsheet/level-3

Catatan alur kerja untuk level 3. Tidak mengubah soal. Sengaja **tanpa path
spesifik perangkat** dan tanpa nama pengguna — repo ini publik.

## Dua workbook yang harus dikerjakan

| File | Sheet | Soal | Fokus |
|---|---|---|---|
| `level-3-dashboard-penjualan-pivot.xlsx` | `1_Masalah` → `3_Soal` → `4_Kerja` | 13 | PivotTable, SUMIFS bertingkat, growth, SUMPRODUCT unik |
| `level-3-pembersihan-data.xlsx` | `1_Masalah` → `3_Soal` → `4_Kerja` | 12 | duplikat, ISTEXT, TRIM/LEN, Power Query, tabel `DataBersih` |

Data: 240 baris (dashboard) dan 120 baris kotor (pembersihan). Kunci **tidak** ada di
workbook — disimpan di `pendukung/kunci/*.json` dan hanya dibaca penilai.

## Alur kerja

1. Buka workbook dari folder `latihan/` di Excel.
2. Baca `1_Masalah`, lalu `3_Soal`.
3. Isi kolom **C** di sheet `4_Kerja` — kolom A (nomor soal) dan B (kunci baris) jangan diubah.
4. Angka di kolom C harus **nilai jadi**, bukan formula. Kalau dari pivot/formula:
   Paste Special → Values. Penilai tidak menghitung ulang formula.
5. Jalankan penilai dari folder `spreadsheet/level-3`:

```bash
python pendukung/cek_kerja.py latihan/level-3-dashboard-penjualan-pivot.xlsx
python pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx
python pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx --detail 5
```

## Menjalankan penilai

Penilai membutuhkan **Python 3** + paket `openpyxl`.

```bash
# cek Python tersedia
python --version

# install dependensi (sekali saja)
python -m pip install openpyxl

# jalankan penilai
python pendukung/cek_kerja.py latihan/level-3-dashboard-penjualan-pivot.xlsx
python pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx
python pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx --detail 5
```

**Windows:** nama perintahnya `python` (atau `py`), bukan `python3`. `python3.exe`
tidak ada di Windows — yang muncul dengan nama itu biasanya hanya stub Microsoft
Store yang memunculkan pesan "install from the Microsoft Store". Kalau `python3`
gagal, coba `python` atau `py`.

## Kriteria lulus

- Dashboard: **13/13** soal benar.
- Pembersihan: **12/12** soal benar **dan** tabel `DataBersih` benar (100 baris, kota bersih,
  nilai angka, `id_transaksi` unik).
