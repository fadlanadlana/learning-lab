# Soal SQL Level 1

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `penjualan` | id, tanggal, bulan, region, kanal, produk, qty, harga, diskon, revenue |
| `kampanye_iklan` | tanggal, id_kampanye, nama_kampanye, kanal, impresi, klik, biaya, konversi, revenue |
| `lead` | tanggal_masuk, id_lead, nama, kode_sumber, kota, status, nilai |
| `master_sumber` | kode_sumber, nama_sumber, biaya_per_lead |

Catatan: `diskon` disimpan sebagai pecahan (0.1 = 10%). `bulan` berformat `2026-08`. Kolom `nama`
di tabel `lead` sengaja masih kotor (spasi ganda, huruf besar semua).

Kerjakan di `jawaban.sql` di bawah tiap penanda soal. Semua soal level 1 cukup dengan SELECT/WHERE/
GROUP BY/JOIN — tidak perlu subquery, kecuali soal 12.

---

### SOAL 1
Total revenue seluruh tabel `penjualan`.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Total qty per region, urut dari total terbesar.
Hasil: kolom `region`, `total_qty`. Urutan diuji.

### SOAL 3
5 transaksi dengan revenue terbesar.
Hasil: kolom `id`, `produk`, `revenue`. Urutan diuji (revenue menurun).

### SOAL 4
Jumlah transaksi yang diskonnya minimal 10% (>= 0.1).
Hasil: 1 kolom, 1 baris.

### SOAL 5
Rata-rata diskon untuk kanal `Marketplace`, dibulatkan 4 desimal.
Hasil: 1 kolom, 1 baris.

### SOAL 6
Total revenue per bulan, urut bulan menaik.
Hasil: kolom `bulan`, `total_revenue`. Urutan diuji.

### SOAL 7
Region yang rata-rata revenue per transaksinya di atas 5.000.000 (pakai HAVING).
Hasil: 1 kolom berisi nama region. Urutan diuji (bebas arah diuji apa adanya, pakai ORDER BY region).

### SOAL 8
Jumlah produk unik di tabel `penjualan`.
Hasil: 1 kolom, 1 baris.

### SOAL 9
Total biaya, total revenue, dan ROAS (revenue / biaya, dibulatkan 2 desimal) per kanal dari tabel
`kampanye_iklan`, urut ROAS menurun.
Hasil: kolom `kanal`, `total_biaya`, `total_revenue`, `roas`. Urutan diuji.

### SOAL 10
Jumlah lead berstatus `Won` per nama sumber (ambil `nama_sumber` dari `master_sumber`, bukan kodenya).
Hasil: kolom `nama_sumber`, `jumlah_won`. Urutan diuji (jumlah_won menurun).

### SOAL 11
Jumlah lead dan total nilai per kategori nilai:
`BESAR` bila nilai >= 50.000.000, `MENENGAH` bila >= 10.000.000, sisanya `KECIL`.
Hasil: kolom `kategori`, `jumlah`, `total_nilai`. Urutan diuji (kategori A-Z).

### SOAL 12
Kanal iklan dengan ROAS tertinggi (revenue / biaya) dari tabel `kampanye_iklan`.
Hasil: kolom `kanal`, `roas` — 1 baris saja.
