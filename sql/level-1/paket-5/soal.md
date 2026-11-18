# Soal SQL Paket 5 — Penjualan produk dan status stok

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `penjualan_produk` | tanggal, bulan, sku, qty, harga, revenue |
| `produk` | sku, nama_produk, kategori, stok_akhir, harga_modal |

Catatan: tabel `penjualan_produk` **tidak** punya kolom kategori — kategori dan nama produk hanya ada di tabel `produk`, jadi soal yang menyebut kategori butuh JOIN. Ada SKU di `produk` yang belum pernah terjual.

Kerjakan di `jawaban.sql` di bawah tiap penanda soal. Semua soal level 1 cukup dengan SELECT/WHERE/GROUP BY/JOIN — tidak perlu subquery.

---

### SOAL 1
Total `qty` yang terjual.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Total `qty` terjual per `kategori`, urut dari terbesar.
Butuh JOIN ke `produk`.
Hasil: kolom `kategori`, `total_qty`. Urutan diuji.

### SOAL 3
5 baris dengan `revenue` terbesar.
Hasil: kolom `tanggal`, `sku`, `revenue`. Urutan diuji (revenue menurun).

### SOAL 4
Jumlah transaksi dengan `qty` minimal 20.
Hasil: 1 kolom, 1 baris.

### SOAL 5
Rata-rata `harga` per transaksi untuk kategori `Sepatu`, dibulatkan 0 desimal.
Butuh JOIN ke `produk`.
Hasil: 1 kolom, 1 baris.

### SOAL 6
Total `revenue` per `bulan`, urut bulan menaik.
Hasil: kolom `bulan`, `total_revenue`. Urutan diuji.

### SOAL 7
Kategori dengan total `qty` di atas 80 (pakai HAVING), urut kategori A-Z.
Butuh JOIN.
Hasil: 1 kolom berisi `kategori`. Urutan diuji.

### SOAL 8
Jumlah SKU unik yang pernah terjual.
Hasil: 1 kolom, 1 baris.

### SOAL 9
Per SKU: `nama_produk` (dari tabel `produk`) dan total `qty` terjual, urut total qty menurun.
Hasil: kolom `nama_produk`, `total_qty`. Urutan diuji.

### SOAL 10
Total `revenue` dari produk berkategori `Aksesoris` saja.
Butuh JOIN.
Hasil: 1 kolom, 1 baris.

### SOAL 11
Beri label stok tiap SKU: `HABIS` bila `stok_akhir` = 0, `TIPIS` bila di bawah 10, sisanya `AMAN`. Hitung jumlah SKU per label, urut label A-Z.
Hasil: kolom `label_stok`, `jumlah_sku`. Urutan diuji.

### SOAL 12
SKU yang terdaftar di `produk` tapi belum pernah terjual sama sekali.
Butuh LEFT JOIN + menyaring baris tanpa pasangan.
Hasil: 1 kolom berisi `sku`. Urutan diuji (sku A-Z).
