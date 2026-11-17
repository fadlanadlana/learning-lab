# Level 3 — Mahir (PivotTable, Power Query, kualitas data)

Dua workbook, tema: analisis lanjutan dan pembersihan data. Kontrak 3 sheet tetap sama
(`1_Brief` / `2_Latihan` / `3_Validasi`), plus kolom **Hasil yang diharapkan** di blok REKAP.

| # | File | Fokus | Tugas rekap | Kolom isian |
|---|---|---|---|---|
| 1 | `level-3-dashboard-penjualan-pivot.xlsx` | dashboard penjualan: tren bulanan, region, growth, kontribusi | 13 | — (kolom Revenue sudah diisi) |
| 2 | `level-3-pembersihan-data.xlsx` | kualitas data: duplikat, spasi, angka tersimpan sebagai teks | 12 | Kota Bersih 40 baris |

## Rumus dan cara kerja yang dilatih

**File 1 (dashboard):**
- SUMIFS multi-kriteria (region + bulan), AVERAGEIF, COUNTIFS
- `SUMPRODUCT(1/COUNTIFS(...))` untuk menghitung kombinasi unik Region-Kanal
- pertumbuhan periode: `(Okt - Sep) / Sep`
- kontribusi persen dan capaian target dari parameter
- alur kerja: buat PivotTable dulu untuk eksplorasi, cocokkan angkanya dengan rumus yang dilaporkan

**File 2 (kualitas data):**
- `SUMPRODUCT(1/COUNTIF(...))` → nilai unik; `SUMPRODUCT(--(COUNTIF(...)>1))` → baris duplikat
- `SUMPRODUCT(--ISTEXT(...))` → jumlah sel yang salah tipe
- `SUMPRODUCT(--(...))` → menjumlahkan kolom yang campur angka dan teks
- `LEN` vs `TRIM` → menghitung spasi berlebih; `COUNTIF` wildcard `"*jakarta*"`
- `PROPER(TRIM(...))` untuk membersihkan 40 baris kota
- alur kerja: Power Query (hapus spasi, ubah tipe, hapus duplikat) untuk membersihkan, rumus untuk
  mengukur seberapa kotor datanya sebelum dibersihkan

## Angka acuan dataset

- Penjualan: 60 baris, total revenue Rp 427.283.425, September Rp 149.249.600, Oktober Rp 194.191.975
  (growth 30,11%), Region Sumatera Rp 60.337.350 (target Rp 60.000.000 → capaian 100,6%)
- Pembersihan: 40 baris, 35 ID unik (10 baris duplikat), 10 sel nilai bertipe teks,
  total nilai Rp 93.568.000, 5 baris kota mengandung "jakarta", 17 baris kota berspasi berlebih

## Kriteria lulus

File 1: 13/13 BENAR. File 2: 12/12 rekap BENAR dan 40/40 baris Kota Bersih benar.
80% ke atas = lulus bersyarat.

## Catatan

Beberapa kunci memakai rumus array (`SUMPRODUCT`). Kalau muncul `#VALUE!`, biasanya karena range
yang diblok tidak sama panjang dengan range pembanding — periksa `$` dan baris akhirnya.
