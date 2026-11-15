# learning-lab

Latihan pribadi lintas tools data: **spreadsheet, Excel, SQL, Python** — dari pemula sampai expert.
Aturannya sederhana: setiap level punya file latihan yang menilai jawaban sendiri, jadi saya tahu
salah/benar tanpa perlu tutor.

Repo: <https://github.com/fadlanadlana/learning-lab>

## Struktur

```
learning-lab/
├── excel/                  # latihan khusus Microsoft Excel (PivotTable, Power Query, VBA, fungsi Excel-only)
│   └── README.md
└── spreadsheet/            # latihan konsep & rumus spreadsheet (berlaku di Excel, Google Sheets, LibreOffice)
    ├── README.md
    ├── level-1/
    │   ├── level-1-laporan-penjualan.xlsx
    │   └── README.md
    └── level-2/
        ├── level-2-kinerja-kampanye-digital.xlsx
        ├── level-2-engagement-media-sosial.xlsx
        ├── level-2-funnel-lead-campaign.xlsx
        └── README.md
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
| 3 | Mahir | PivotTable, Power Query, tabel terstruktur, dashboard | belum |
| 4 | Expert | VBA/Apps Script, DAX, otomasi end-to-end, model keuangan | belum |

Jalur SQL dan Python belum dibuat; urutannya setelah spreadsheet level 2 (lihat `01_Roadmap.md`
di vault Obsidian pribadi).

## Cara memakai file latihan

1. Buka file `.xlsx` di aplikasi spreadsheet (Excel di PC, atau Google Sheets kalau di HP).
2. Baca sheet **1_Brief** — masalah, tujuan, aturan, kriteria lulus.
3. Kerjakan sheet **2_Latihan** — isi hanya sel kuning; jangan ubah data dan parameter.
4. Cek sheet **3_Validasi** — status BENAR/SALAH per tugas plus skor otomatis.
5. Ulangi sampai lulus, commit, push, baru naik level.

Semua kunci dihitung dengan rumus, bukan angka mati — kalau data diubah, kunci ikut menyesuaikan.