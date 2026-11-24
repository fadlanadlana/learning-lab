# spreadsheet/level-3 — PivotTable & Power Query

Dua workbook, dua fokus. Workbook **tidak** memuat kunci jawaban: kunci disimpan terpisah di
`pendukung/kunci/*.json` dan hanya dibaca penilai.

## Struktur folder

```
level-3/
├── latihan/                                    <- buka di Excel/WPS
│   ├── level-3-dashboard-penjualan-pivot.xlsx      240 baris data, 13 soal, fokus PivotTable
│   └── level-3-pembersihan-data.xlsx               120 baris data kotor, 12 soal, fokus Power Query
├── pendukung/
│   ├── cek_kerja.py                           penilai otomatis (BENAR/SALAH per soal)
│   └── kunci/*.json                           kunci jawaban (tidak ada di workbook)
├── _tools/gen_workbook.py                     generator kedua workbook
└── README.md
```

## Isi tiap workbook (4 sheet)

| Sheet | Isi | Kamu sentuh? |
|---|---|---|
| `1_Masalah` | konteks bisnis, pertanyaan yang harus dijawab, tujuan, tool yang dilatih, target per region (workbook pivot) | baca |
| `2_Data` | data mentah apa adanya — jangan diubah | tidak |
| `3_Soal` | 12-13 soal: pertanyaan, bentuk jawaban, letak jawaban | baca |
| `4_Kerja` | blok jawaban SOAL / KUNCI BARIS / JAWABAN (kolom C kamu isi) + tempat pivot & Power Query | **ya** |

Blok jawaban ada di `4_Kerja` mulai baris 3. Kolom A (nomor soal) dan B (kunci baris) sudah
disediakan; kamu hanya mengisi kolom C. Jangan pindahkan bloknya — penilai membaca dari situ.
Pivot table atau hasil Power Query taruh di sebelah kanan blok (mulai kolom F) atau di sheet baru.

## Cara mengerjakan

1. Buka workbook dari folder `latihan/` di Excel/WPS/Google Sheets.
2. Baca `1_Masalah`, lalu `3_Soal`.
3. Kerjakan di `4_Kerja`, lalu isi kolom C. Angka di kolom C harus nilai jadi: kalau berasal dari
   pivot atau formula, salin sebagai nilai (Paste Special > Values), karena penilai tidak
   menghitung ulang formula.
4. Jalankan penilai dari Termux:

```
cd spreadsheet/level-3
python3 pendukung/cek_kerja.py latihan/level-3-dashboard-penjualan-pivot.xlsx
python3 pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx
python3 pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx --detail 5
```

Penilai mencetak BENAR/SALAH per soal, skor, dan status. `--detail N` menampilkan jawabanmu
berdampingan dengan kunci untuk soal itu — jadi kunci tidak perlu terpampang di Excel.

Untuk workbook pembersihan, penilai juga memeriksa tabel **DataBersih** (100 baris:
`id_transaksi`, `kota_bersih`, `nilai`).

## Kriteria lulus

- Dashboard: 13/13 soal benar.
- Pembersihan: 12/12 soal benar dan tabel DataBersih benar (100 baris, kota bersih, nilai angka).
- Kurang 2 soal = lulus bersyarat.

## Catatan jujur soal penilaian

Penilai memeriksa **hasil**, bukan bahwa kamu benar-benar memakai PivotTable atau Power Query.
Kalau langkah tool-nya mau ikut diperiksa (bukti Remove Duplicates, Change Type, Trim), kirim
filenya setelah selesai.

## Angka acuan (untuk mengecek kewajaran hasilmu)

Dashboard, 240 baris:

    total revenue        965.710.750
    total qty            3.676
    kombinasi region x kanal unik   20
    produk dengan revenue terbesar  PR-05 Sepatu Sneaker
    rata-rata diskon Marketplace    0,0829
    growth Oktober vs September     -28,69%   (turun, bukan naik)
    kontribusi region teratas       23,03%
    transaksi dengan diskon >= 10%  111
    capaian target Bali             344,09%

Pembersihan, 120 baris:

    100 transaksi unik, 20 baris duplikat
    37 sel nilai tersimpan sebagai teks
    total nilai semua baris         222.550.000
    baris kota mengandung "jakarta" 32
    baris kota berspasi berlebih    51
    total nilai setelah bersih      175.550.000
    kota unik setelah bersih        5
    rata-rata nilai bersih          1.755.500

Angka lengkap dan resmi ada di `pendukung/kunci/*.json` — bukan di workbook.