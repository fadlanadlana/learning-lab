# Soal SQL Level 2 - Paket 3 - Kunjungan pelanggan per kanal (window function)

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `kunjungan` | tanggal, bulan, id_pelanggan, kanal, sesi, revenue |
| `pelanggan` | id_pelanggan, nama, kota |

Catatan: tiap baris `kunjungan` = satu pelanggan pada satu bulan lewat satu kanal. Setiap pelanggan punya tepat satu baris per bulan (3 bulan). Fokus set ini: window function (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `SUM/AVG OVER`, `FIRST_VALUE`).

Kerjakan di `paket-3-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal.

---

### SOAL 1
Total revenue per kanal, urut menurun.
Hasil: kolom `kanal`, `total_revenue`. Urutan diuji.

### SOAL 2
Revenue per bulan beserta total kumulatifnya (window SUM), urut bulan.
Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.

### SOAL 3
Pertumbuhan revenue bulanan dalam persen dibanding bulan sebelumnya (pakai LAG), dibulatkan 2 desimal, urut bulan.
Hasil: kolom `bulan`, `revenue`, `growth_persen`. Urutan diuji.

### SOAL 4
Peringkat kanal berdasarkan revenue di tiap bulan (pakai RANK), urut bulan lalu peringkat.
Hasil: kolom `bulan`, `kanal`, `revenue`, `peringkat`. Urutan diuji.

### SOAL 5
Kunjungan dengan revenue terbesar milik tiap pelanggan (satu baris per pelanggan, pakai ROW_NUMBER), urut `id_pelanggan` A-Z.
Hasil: kolom `id_pelanggan`, `bulan`, `revenue`. Urutan diuji.

### SOAL 6
Tiap baris kunjungan beserta rata-rata revenue kanalnya (pakai AVG OVER PARTITION), dibulatkan 0 desimal.
Urut kanal A-Z, lalu bulan, lalu revenue menurun.
Hasil: kolom `kanal`, `bulan`, `revenue`, `rata_kanal`. Urutan diuji.

### SOAL 7
Peringkat rapat (DENSE_RANK) kanal berdasarkan total revenue, urut peringkat.
Hasil: kolom `kanal`, `total_revenue`, `peringkat`. Urutan diuji.

### SOAL 8
Revenue per bulan per kanal, plus nama kanal dengan revenue terbesar di bulan itu (pakai FIRST_VALUE), urut bulan lalu revenue menurun.
Hasil: kolom `bulan`, `kanal`, `revenue`, `kanal_top`. Urutan diuji.

### SOAL 9
Total revenue kumulatif tiap pelanggan per bulan (SUM OVER PARTITION BY pelanggan), urut `id_pelanggan` lalu bulan.
Hasil: kolom `id_pelanggan`, `bulan`, `revenue`, `kumulatif`. Urutan diuji.

### SOAL 10
Selisih revenue tiap pelanggan dibanding bulannya yang lalu (LAG per pelanggan), urut `id_pelanggan` lalu bulan.
Hasil: kolom `id_pelanggan`, `bulan`, `revenue`, `selisih`. Urutan diuji.

### SOAL 11
Jumlah pelanggan unik per kanal, urut jumlah menurun lalu kanal A-Z.
Hasil: kolom `kanal`, `jumlah_pelanggan`. Urutan diuji.

### SOAL 12
Kanal yang total revenue-nya di atas rata-rata antar-kanal (pakai subquery), urut menurun.
Hasil: kolom `kanal`, `total_revenue`. Urutan diuji.
