# Excel Data Cleaning — 5 Dataset Latihan

Latihan data cleaning di Excel dengan **data kotor realistis**.
Setiap file berisi 2 sheet: `Data Kotor` (~2.500 baris) dan `Checklist` (6 area, 37 item).

Repo: <https://github.com/fadlanadlana/learning-lab>

## File

| # | File | Domain | Baris terbaca | Target bersih |
|---|---|---|---:|---:|
| 1 | `01-penjualan-retail.xlsx` | Transaksi penjualan | 2.560 | 2.498 |
| 2 | `02-pelanggan-crm.xlsx` | Data pelanggan | 2.555 | 2.498 |
| 3 | `03-inventori-gudang.xlsx` | Stok gudang | 2.555 | 2.498 |
| 4 | `04-kampanye-marketing.xlsx` | Performa kampanye | 2.560 | 2.498 |
| 5 | `05-kehadiran-karyawan.xlsx` | Absensi karyawan | 2.555 | 2.498 |

Kelima file punya **6 jenis masalah yang sama** tapi isi & variasi berbeda — jadi bisa
dilatih berulang tanpa hafal jawaban.

## Sheet "Data Kotor"

Empat lapis kotoran struktural sengaja ditanam:

| Baris | Isi | Tindakan |
|---|---|---|
| 1 | Judul (merged) | Hapus |
| 2 | Kosong | Hapus |
| 3 | **Header asli** | Jadikan header |
| 4 dst | Data | — |
| tengah | **Header terduplikasi** | Hapus |
| tengah | **Baris kosong** (3 buah) | Hapus |
| akhir | **Baris TOTAL/footer** | Hapus |

Plus 6 kategori masalah kotoran data:

| Kategori | Contoh yang ditanam |
|---|---|
| **Missing Values** | 3 kolom wajib berisi sel kosong (200–270 baris kena) |
| **Standardise Numbers** | angka jadi teks: `1.500.000`, `3 pcs`, `Rp 4.250.000`; tanggal campur 3–4 format |
| **Standardise Text** | `JAKARTA` / `jakarta` / `Jakarta ` / `DKI Jakarta` / `Jogja`; singkatan & kapitalisasi campur |
| **Fix Invalid Values** | tanggal 2099, qty negatif, diskon 150%, klik > impresi, jam keluar < jam masuk, stok −20 |
| **Filter Data** | ±50–57 baris duplikat utuh |

## Sheet "Checklist"

37 item dalam 6 area yang Anda minta:

1. **Fix rows and columns** — header, baris kosong, footer, tipe kolom, grain
2. **Missing Values** — kolom wajib, keputusan per kolom
3. **Standardise Numbers** — teks→angka, pemisah, mata uang, satuan, persen
4. **Standardise Text** — TRIM, kapitalisasi, variasi penulisan, karakter tersembunyi
5. **Fix Invalid Values** — negatif, tanggal mustahil, nol, outlier
6. **Filter Data** — duplikat, dummy, rekonsiliasi

Kolom **Status** punya dropdown: `Belum` / `OK` / `Ada masalah` / `N/A`.
Di bawahnya ada ringkasan otomatis + blok **REKONSILIASI**.

## Cara mengerjakan

1. Buka file, buat **sheet baru** bernama `Salinan` — jangan kerja di `Data Kotor`.
2. Salin data mentah ke `Salinan`, lalu bereskan **struktur dulu** (area 1), baru nilai.
3. Isi kolom Status di sheet `Checklist` sambil jalan.
4. Isi blok REKONSILIASI di bawah. **Selisih harus 0** — kalau tidak, ada baris hilang tanpa jejak.

### Urutan yang disarankan

```
struktur → missing → angka → teks → invalid → duplikat → rekonsiliasi
```

Jangan dibalik. Kalau Anda memperbaiki nilai di atas struktur yang masih rusak,
semua hitungan membengkak (kejadian nyata: `COUNTA` menghitung baris header
duplikat sebagai data → 720 bukan 120).

## Pemeriksaan hasil

Ingin tahu apakah pekerjaan Anda benar? Kunci jawaban (jumlah masalah per kategori)
ada di `kunci/*.json` — terpisah dari workbook, bukan di dalam Excel.

```bash
python _tools/cek_hasil.py salinan-01-penjualan.xlsx 01-penjualan-retail.xlsx
```

## Struktur folder

```
excel/data-cleaning/
├── 01-penjualan-retail.xlsx      <- buka di Excel
├── 02-pelanggan-crm.xlsx
├── 03-inventori-gudang.xlsx
├── 04-kampanye-marketing.xlsx
├── 05-kehadiran-karyawan.xlsx
├── kunci/*.json                   <- jumlah masalah terukur (jangan dibuka dulu)
└── _tools/
    ├── gen_dirty_data.py          <- generator kelima file
    └── ukur_kunci.py              <- hitung ulang kunci dari file jadi
```

## Catatan

- Semua data **sintetis**, dibuat dengan seed tetap — bisa diregenerasi identik.
- Angka di `kunci/*.json` dihitung dari file nyata, bukan diperkirakan.
- Baris bersih 2.498 (bukan 2.500) karena sebagian baris duplikat menimpa baris asli
  yang sudah punya masalah lain. Itu memang wajar — rekonsiliasi tetap balance.
