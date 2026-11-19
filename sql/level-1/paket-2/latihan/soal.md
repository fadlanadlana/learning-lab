# Soal SQL Paket 2 — Funnel website per kanal

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `trafik` | tanggal, bulan, kanal, device, sesi, konversi, revenue |
| `kanal_master` | kanal, jenis, biaya_per_klik |

Catatan: `sesi` = jumlah kunjungan, `konversi` = jumlah transaksi yang terjadi dari kunjungan itu. `kanal_master.biaya_per_klik` dipakai untuk menghitung biaya: `sesi * biaya_per_klik`. Satu kanal di `kanal_master` belum pernah punya baris trafik.

Kerjakan di `jawaban.sql` di bawah tiap penanda soal. Semua soal level 1 cukup dengan SELECT/WHERE/GROUP BY/JOIN — tidak perlu subquery.

---

### SOAL 1
Total `sesi` seluruh tabel `trafik`.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Total `sesi` per `device`, urut dari terbesar.
Hasil: kolom `device`, `total_sesi`. Urutan diuji.

### SOAL 3
5 baris dengan `revenue` terbesar.
Hasil: kolom `tanggal`, `kanal`, `revenue`. Urutan diuji (revenue menurun).

### SOAL 4
Jumlah baris trafik yang `revenue`-nya di bawah 1.000.000.
Hasil: 1 kolom, 1 baris.

### SOAL 5
Rata-rata `revenue` per `sesi` untuk kanal `Email`, dibulatkan 4 desimal.
Hasil: 1 kolom, 1 baris.

### SOAL 6
Total `revenue` per `bulan`, urut bulan menaik.
Hasil: kolom `bulan`, `total_revenue`. Urutan diuji.

### SOAL 7
Kanal yang total `sesi`-nya di atas 1.500 (pakai HAVING), urut nama kanal A-Z.
Hasil: 1 kolom berisi `kanal`. Urutan diuji.

### SOAL 8
Jumlah `device` unik di tabel `trafik`.
Hasil: 1 kolom, 1 baris.

### SOAL 9
Per kanal: total biaya (`sesi * biaya_per_klik`), total revenue, dan ROAS (total revenue / total biaya, dibulatkan 2 desimal).
Butuh JOIN ke `kanal_master`.
Hasil: kolom `kanal`, `total_biaya`, `total_revenue`, `roas`. Urutan diuji (ROAS menurun).

### SOAL 10
Total `revenue` untuk kanal berjenis `Paid` saja, urut nama kanal A-Z.
Hasil: kolom `kanal`, `total_revenue`. Urutan diuji.

### SOAL 11
Beri label tiap kanal berdasarkan total revenue: `UTAMA` bila >= 15.000.000, `POTENSIAL` bila >= 8.000.000, sisanya `KECIL`.
Hasil: kolom `kanal`, `label`. Urutan diuji (label A-Z, lalu kanal A-Z).

### SOAL 12
Kanal yang terdaftar di `kanal_master` tapi belum punya satu baris pun di `trafik`.
Butuh LEFT JOIN + menyaring baris tanpa pasangan.
Hasil: 1 kolom berisi `kanal` — 1 baris.
