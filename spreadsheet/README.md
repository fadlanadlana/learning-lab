# spreadsheet/ — konsep & rumus spreadsheet

Yang dilatih di sini adalah logika dan rumusnya, bukan menunya. Setiap file `.xlsx` di folder ini
harus bisa dibuka dan dikerjakan apa adanya di **Microsoft Excel**, **Google Sheets**, maupun
**LibreOffice Calc** — satu-satunya perbedaan yang diizinkan adalah tata letak UI.

Untuk latihan fitur khas Excel (PivotTable, Power Query, VBA, DAX) gunakan [`../excel/`](../excel/).

## Level tersedia

- [`level-1/`](level-1/) — Laporan Penjualan Tim Sales: SUM, AVERAGE, MIN, MAX, COUNT, SUMIF,
  COUNTIF, AVERAGEIF, IF, IFERROR, ROUND, persentase, referensi absolut. 24 baris data, 16 tugas
  rekap, validasi otomatis + skor.

## Level berikutnya (belum dibuat)

- **level-2 / Menengah** — tersedia 3 file bertema marketing (kinerja kampanye digital, engagement
  media sosial, funnel lead campaign): SUMIFS & COUNTIFS multi-kriteria, VLOOKUP, INDEX-MATCH,
  IF bertingkat, PROPER/TRIM, pengurangan tanggal, IFERROR. Lihat [`level-2/`](level-2/).
- **level-3 / Mahir** — tersedia 2 file: `level-3-dashboard-penjualan-pivot.xlsx` (PivotTable,
  SUMIFS bertingkat, growth, SUMPRODUCT unik) dan `level-3-pembersihan-data.xlsx` (duplikat,
  ISTEXT, TRIM/LEN, Power Query). Lihat [`level-3/`](level-3/).
- **level-4 / Expert** — model 3-statement sederhana, audit formula, penanganan data besar,
  jembatan ke SQL/Python (data yang sama dikerjakan ulang di sana).

## Konvensi tiap level

Setiap file punya 3 sheet dengan urutan tetap:

1. `1_Brief` — masalah kerja nyata, tujuan yang ingin dicapai, aturan, kriteria lulus.
2. `2_Latihan` — data mentah + sel kuning yang harus diisi dengan rumus.
3. `3_Validasi` — jawaban dibandingkan dengan rumus kunci, keluar BENAR/SALAH + skor.