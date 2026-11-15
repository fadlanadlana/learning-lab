# Level 2 — Menengah (tema marketing)

Tiga workbook, satu tema kerja: marketing. Semua pakai kontrak 3 sheet yang sama seperti level 1
(`1_Brief` / `2_Latihan` / `3_Validasi`), dengan tambahan kolom **Hasil yang diharapkan** di blok
REKAP supaya tidak perlu menebak format jawaban.

| # | File | Tema | Isian per baris | Tugas rekap |
|---|---|---|---|---|
| 1 | `level-2-kinerja-kampanye-digital.xlsx` | Performance marketing: belanja iklan, CTR, CPC, ROAS | ROAS 30 baris | 14 |
| 2 | `level-2-engagement-media-sosial.xlsx` | Content marketing: reach, engagement rate, konten terbaik | Engagement Rate 24 baris | 14 |
| 3 | `level-2-funnel-lead-campaign.xlsx` | Marketing operations: lead, konversi, pipeline, umur lead | Umur Lead 28 baris | 14 |

Urutan pengerjaan sesuai nomor: kampanye digital → media sosial → funnel lead.

## Rumus yang dilatih

- **File 1:** SUM, SUMIF, SUMIFS (2 kriteria), COUNTIFS, VLOOKUP, INDEX-MATCH, IF, pembagian +
  referensi absolut, persentase (CTR, kontribusi).
- **File 2:** SUM, AVERAGE, AVERAGEIF, COUNTIF, COUNTIFS, MAX, INDEX-MATCH (ambil judul terbaik),
  VLOOKUP dari master, IF bertingkat (3 kategori), persentase.
- **File 3:** COUNTA, COUNTIF, COUNTIFS, SUMIF, VLOOKUP kode sumber, INDEX-MATCH (kota dengan deal
  terbesar), PROPER + TRIM (membersihkan nama), IF bertingkat, pengurangan tanggal, IFERROR.

## Yang membedakan dari level 1

- Ada **master referensi** di kanan data (kolom N–Q) untuk latihan VLOOKUP / INDEX-MATCH.
- Ada **blok PARAMETER** (kolom S–T): target ROAS, ambang viral, tanggal cut-off, batas kategori.
  Jangan diubah — kunci validasi membacanya.
- Setiap tugas punya kolom **Hasil yang diharapkan**: format angka, atau teks persis yang dinilai
  (misalnya `"EFISIEN"` / `"TIDAK EFISIEN"`, `"KAMPANYE TIDAK ADA"`).
- Status validasi tiga nilai: `KOSONG` (belum diisi), `BENAR`, `SALAH`. KOSONG tidak dihitung benar.
- Kolom isian (ROAS / Engagement Rate / Umur Lead) dicek baris per baris, bukan hanya rekap.

## Cara menilai diri

1. Kerjakan dulu tanpa membuka kolom Kunci (D) di sheet `3_Validasi`.
2. Baca `SKOR REKAP`, `PERSENTASE`, `BELUM DIISI (KOSONG)`, baris cek kolom isian, lalu `STATUS AKHIR`.
3. Lulus = semua rekap BENAR **dan** kolom isian penuh benar (misal 30/30). 80% ke atas = lulus
   bersyarat; di bawah itu ulangi.

Catatan: tidak ada `TODAY()` di file ini. Tanggal acuan selalu dari parameter supaya hasil bisa
dinilai ulang kapan pun.
