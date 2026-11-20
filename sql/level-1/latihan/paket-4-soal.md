# Soal SQL Paket 4 — Biaya iklan dan CPL per platform

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `iklan_harian` | tanggal, bulan, platform, id_iklan, kreatif, impresi, klik, biaya, lead |
| `platform_master` | platform, jenis, cpl_target |

Catatan: `biaya` dalam rupiah, `lead` = jumlah prospek yang masuk. CPL = biaya / lead. Satu platform di `platform_master` belum pernah dipakai beriklan.

Kerjakan di `paket-4-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal. Semua soal level 1 cukup dengan SELECT/WHERE/GROUP BY/JOIN — tidak perlu subquery.

---

### SOAL 1
Total `biaya` seluruh iklan.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Total `impresi` per `platform`, urut dari terbesar.
Hasil: kolom `platform`, `total_impresi`. Urutan diuji.

### SOAL 3
5 baris dengan `klik` terbanyak.
Hasil: kolom `tanggal`, `kreatif`, `klik`. Urutan diuji (klik menurun).

### SOAL 4
Jumlah baris iklan yang `lead`-nya di bawah 20.
Hasil: 1 kolom, 1 baris.

### SOAL 5
CTR = total klik / total impresi untuk platform `TikTok`, dibulatkan 4 desimal.
Hasil: 1 kolom, 1 baris.

### SOAL 6
Total `biaya` per `bulan`, urut bulan menaik.
Hasil: kolom `bulan`, `total_biaya`. Urutan diuji.

### SOAL 7
Kreatif yang total `lead`-nya minimal 100 (pakai HAVING), urut lead menurun.
Hasil: kolom `kreatif`, `total_lead`. Urutan diuji.

### SOAL 8
Jumlah `kreatif` unik yang pernah dipakai.
Hasil: 1 kolom, 1 baris.

### SOAL 9
Per platform: total biaya, total lead, dan CPL (biaya / lead, dibulatkan 0 desimal).
Urut dari CPL termurah.
Hasil: kolom `platform`, `total_biaya`, `total_lead`, `cpl`. Urutan diuji.

### SOAL 10
Total `lead` dari platform berjenis `Search` saja.
Butuh JOIN ke `platform_master`.
Hasil: 1 kolom, 1 baris.

### SOAL 11
Beri label efisiensi per platform berdasarkan CPL: `EFISIEN` bila CPL <= 45.000, `SEDANG` bila <= 55.000, sisanya `MAHAL`. Tampilkan platform dan labelnya, urut label A-Z, lalu platform A-Z.
Hasil: kolom `platform`, `label_cpl`. Urutan diuji.

### SOAL 12
Platform yang terdaftar di `platform_master` tapi belum punya satu baris iklan pun.
Butuh LEFT JOIN + menyaring baris tanpa pasangan.
Hasil: 1 kolom berisi `platform` — 1 baris.
