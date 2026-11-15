# Level 1 — Laporan Penjualan Tim Sales

File: `level-1-laporan-penjualan.xlsx`

Satu file, tiga sheet:

| Sheet | Isi |
|---|---|
| `1_Brief` | Masalah kerja, tujuan, 4 aturan main, kriteria lulus |
| `2_Latihan` | 24 baris data penjualan Oktober 2026 + kolom Total (J5:J28) + 16 tugas rekap (F32:F47) |
| `3_Validasi` | Bandingkan jawabanmu dengan rumus kunci: BENAR/SALAH per tugas, cek kolom Total baris per baris, skor total |

## Skenario

Atasan minta rekap penjualan tim sales besok pagi. Data ekspor sistem cuma punya qty, harga satuan,
dan diskon — belum ada total per baris dan belum ada rekap per cabang/sales. Semua harus dihitung
dengan rumus, bukan angka ketik manual.

## Yang harus dikerjakan

1. **Kolom Total Penjualan (J5:J28)** — 24 sel.
   Total = Qty × Harga Satuan × (1 − Diskon). Contoh baris pertama: `=G5*H5*(1-I5)`, lalu copy ke bawah.
2. **Blok REKAP (F32:F47)** — 16 sel, masing-masing satu rumus:

| # | Tugas | Rumus |
|---|---|---|
| 1 | Total penjualan seluruh transaksi | `SUM` |
| 2 | Rata-rata nilai per transaksi | `AVERAGE` |
| 3 | Nilai transaksi terbesar | `MAX` |
| 4 | Nilai transaksi terkecil | `MIN` |
| 5 | Jumlah transaksi | `COUNT` |
| 6–8 | Total penjualan Cabang Jakarta / Bandung / Surabaya | `SUMIF` |
| 9 | Jumlah transaksi Sales S01 | `COUNTIF` |
| 10 | Jumlah transaksi di atas ambang (sel C52) | `COUNTIF` + `">"&` |
| 11 | Rata-rata nilai transaksi Sales S02 | `AVERAGEIF` |
| 12 | Total unit (Qty) terjual | `SUM` |
| 13 | Kontribusi Cabang Jakarta (%) | pembagian + referensi absolut `$` |
| 14 | Rata-rata dibulatkan ke ribuan terdekat | `ROUND(...,-3)` |
| 15 | Evaluasi target vs parameter C51 | `IF` |
| 16 | Rata-rata transaksi Sales S05 (tidak ada di data) | `IFERROR` + `AVERAGEIF` |

Jangan mengubah data `A4:J28` dan parameter `C51:C52` — kunci validasi membaca keduanya.

## Cara menilai diri

Buka sheet `3_Validasi`:

- kolom **E** → `KOSONG` (belum diisi) / `BENAR` / `SALAH` per tugas;
- **SKOR REKAP** → jumlah benar dari 16 (format `x / 16 benar`);
- **BARIS KOLOM TOTAL (J) BENAR** → harus 24/24;
- **STATUS AKHIR** → `LULUS SEMPURNA`, `LULUS BERSYARAT`, atau `BELUM LULUS`;
- **Belum diisi (KOSONG)** → jumlah tugas yang belum kamu isi (bukan salah).

Kriteria lulus: 16/16 rekap benar **dan** 24/24 baris Total benar.
Skor 13–15 dengan 20+ baris benar = lulus bersyarat; perbaiki yang salah sebelum ke level 2.

## Kalau hasilnya aneh

- **Hampir semua SALAH padahal merasa benar** → kolom Total (J) belum benar. Cek `24/24` dulu.
- **Kolom Kunci menampilkan `#DIV/0!` sebelum kamu isi apa pun** → normal: AVERAGE/AVERAGEIF
  atas kolom Total yang masih kosong. Statusnya tetap `KOSONG`. Kunci terisi begitu kolom J selesai.
- **Muncul `#DIV/0!` di sheet 2** → ada pembagian dengan sel kosong; kerjakan berurutan dari tugas 1.
- **Ingin melihat kunci** → kolom D dan H di sheet `3_Validasi` disembunyikan. Blok kolom C:D → klik
  kanan → *Unhide*. Sebaiknya hanya setelah mencoba serius: kuncimu hilang kalau langsung dilihat.
- **Nilai 0 di sel yang seharusnya kosong** → normal; `3_Validasi` menarik sel kosong sebagai 0 lalu
  menandainya SALAH.

## Setelah lulus

```bash
git add -A && git commit -m "level 1: laporan penjualan selesai" && git push
```

Lanjut ke `spreadsheet/level-2/` (SUMIFS/COUNTIFS bertingkat, VLOOKUP/XLOOKUP, INDEX-MATCH).