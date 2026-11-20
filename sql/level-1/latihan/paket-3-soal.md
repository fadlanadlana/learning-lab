# Soal SQL Paket 3 — Repeat order pelanggan

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `pesanan` | id_pesanan, tanggal, bulan, id_pelanggan, kota, kanal, qty, nilai |
| `pelanggan` | id_pelanggan, nama, segmen, kota_domisili |
| `ongkir` | kota, tarif_per_kg |

Catatan: `kota` di tabel `pesanan` adalah kota pengiriman, bisa beda dengan `kota_domisili` pelanggan. `segmen` pelanggan hanya `Loyal` atau `Baru`. Satu kota di tabel `ongkir` belum pernah dikirimi pesanan.

Kerjakan di `paket-3-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal. Semua soal level 1 cukup dengan SELECT/WHERE/GROUP BY/JOIN — tidak perlu subquery.

---

### SOAL 1
Total `nilai` seluruh pesanan.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Jumlah pesanan per `id_pelanggan`, urut jumlah menurun. Kalau jumlahnya sama, urutkan `id_pelanggan` menaik (A-Z).
Hasil: kolom `id_pelanggan`, `jumlah_pesanan`. Urutan diuji.

### SOAL 3
3 pelanggan dengan total nilai pesanan terbesar, tampilkan `nama` (dari `pelanggan`, bukan ID-nya).
Butuh JOIN.
Hasil: kolom `nama`, `total_nilai`. Urutan diuji (total menurun).

### SOAL 4
Jumlah pesanan dengan `nilai` minimal 1.000.000.
Hasil: 1 kolom, 1 baris.

### SOAL 5
Rata-rata `qty` per pesanan untuk kanal `WhatsApp`, dibulatkan 2 desimal.
Hasil: 1 kolom, 1 baris.

### SOAL 6
Total `nilai` per `bulan`, urut bulan menaik.
Hasil: kolom `bulan`, `total_nilai`. Urutan diuji.

### SOAL 7
Kota pengiriman yang rata-rata nilai pesanannya di atas 900.000 (pakai HAVING), urut kota A-Z.
Hasil: 1 kolom berisi `kota`. Urutan diuji.

### SOAL 8
Jumlah kota unik yang pernah menerima pesanan.
Hasil: 1 kolom, 1 baris.

### SOAL 9
Per `segmen` pelanggan: jumlah pesanan dan total nilai, urut total nilai menurun.
Butuh JOIN ke `pelanggan`.
Hasil: kolom `segmen`, `jumlah_pesanan`, `total_nilai`. Urutan diuji.

### SOAL 10
Total nilai pesanan dari kanal `Marketplace` atau `Website` (pakai IN, bukan dua OR).
Hasil: 1 kolom, 1 baris.

### SOAL 11
Jumlah pesanan dari pelanggan yang namanya mengandung `Putri`.
Butuh JOIN + LIKE.
Hasil: 1 kolom, 1 baris.

### SOAL 12
Kota yang ada di tabel `ongkir` tapi belum pernah menerima pesanan.
Butuh LEFT JOIN + menyaring baris tanpa pasangan.
Hasil: 1 kolom berisi `kota` — 1 baris.
