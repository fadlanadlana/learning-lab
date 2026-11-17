# learning-lab

Latihan pribadi lintas tools data: **spreadsheet, Excel, SQL, Python** — dari pemula sampai expert.
Aturannya sederhana: setiap level punya file latihan yang menilai jawaban sendiri, jadi saya tahu
salah/benar tanpa perlu tutor.

Repo: <https://github.com/fadlanadlana/learning-lab>

## Struktur

```
learning-lab/
├── excel/                  # latihan khusus Microsoft Excel (PivotTable, Power Query, VBA, fungsi Excel-only)
├── spreadsheet/            # rumus & analisis spreadsheet (Excel, Google Sheets, LibreOffice)
│   ├── level-1/            # pemula   : 1 workbook, 16 tugas
│   ├── level-2/            # menengah : 3 workbook tema marketing, 14 tugas/file
│   ├── level-3/            # mahir    : 2 workbook (dashboard PivotTable, pembersihan data)
│   └── selesai/            # salinan hasil pengerjaan (bukti lulus)
├── sql/
│   └── level-1/            # 12 soal + cek_jawaban.py (SQLite) + data/*.csv
└── python/
    └── level-1/            # 12 soal + cek_jawaban.py + data/*.csv
```

`excel/` dan `spreadsheet/` sengaja dipisah:

- **spreadsheet/** — yang dilatih adalah *cara berpikir dan rumusnya* (SUM, SUMIF, IF, referensi absolut).
  File `.xlsx` di sini harus jalan apa adanya di Excel, Google Sheets, maupun LibreOffice.
- **excel/** — yang dilatih adalah *fitur yang hanya ada di Excel*: PivotTable, Power Query, Power Pivot/DAX,
  VBA, dynamic array, XLOOKUP/LET/LAMBDA. Kalau ilmunya pindah ke aplikasi lain, isinya tidak berlaku.

## Level

| Level | Nama | Fokus | Status |
|---|---|---|---|
| 1 | Pemula | rumus dasar, referensi absolut, IF, format angka | spreadsheet: tersedia |
| 2 | Menengah | SUMIFS bertingkat, lookup (VLOOKUP/XLOOKUP/INDEX-MATCH), teks, tanggal | spreadsheet: tersedia (3 file tema marketing) |
| 3 | Mahir | PivotTable, Power Query, SUMPRODUCT, kualitas data | spreadsheet: tersedia (2 file) |
| 4 | Expert | VBA/Apps Script, DAX, otomasi end-to-end, model keuangan | belum |

| Jalur | Level 1 | Cara menilai |
|---|---|---|
| sql | tersedia (12 soal) | `python3 cek_jawaban.py` — query dijalankan di SQLite, hasil dibandingkan dengan kunci |
| python | tersedia (12 soal) | `python3 cek_jawaban.py` — fungsimu dipanggil, hasil dibandingkan dengan kunci |

Ketiga jalur memakai dataset yang sama (penjualan, kampanye iklan, lead), jadi satu angka bisa
dikerjakan dengan SUMIFS di spreadsheet, GROUP BY di SQL, dan dict comprehension di Python.

## Cara memakai file latihan

1. Buka file `.xlsx` di aplikasi spreadsheet (Excel di PC, atau Google Sheets kalau di HP).
2. Baca sheet **1_Brief** — masalah, tujuan, aturan, kriteria lulus.
3. Kerjakan sheet **2_Latihan** — isi hanya sel kuning; jangan ubah data dan parameter.
4. Cek sheet **3_Validasi** — status BENAR/SALAH per tugas plus skor otomatis.
5. Ulangi sampai lulus, commit, push, baru naik level.

Semua kunci dihitung dengan rumus, bukan angka mati — kalau data diubah, kunci ikut menyesuaikan.