# Soal SQL Level 2 - Paket 2 - Pesanan, item pesanan, dan produk (JOIN bertingkat)

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `pesanan` | id_pesanan, tanggal, bulan, id_pelanggan, kota, status |
| `item_pesanan` | id_pesanan, sku, qty, harga |
| `produk` | sku, nama_produk, kategori, harga_modal |

Catatan: satu pesanan punya banyak baris di `item_pesanan`, dan nama/kategori/harga modal produk hanya ada di `produk`. Nilai satu pesanan = SUM(qty x harga). Status pesanan: `Selesai`, `Batal`, `Proses` — soal yang menyebut revenue/pendapatan berarti hanya `Selesai`. Satu SKU belum pernah terjual.

Kerjakan di `paket-2-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal.

---

### SOAL 1
Total pendapatan (SUM(qty x harga)) dari pesanan berstatus `Selesai`.
Butuh JOIN 2 tabel.
Hasil: 1 kolom, 1 baris.

### SOAL 2
Pendapatan per kategori produk dari pesanan `Selesai`, urut menurun.
Butuh JOIN 3 tabel.
Hasil: kolom `kategori`, `revenue`. Urutan diuji.

### SOAL 3
Jumlah SKU berbeda di tiap pesanan `Selesai`, urut jumlah menurun lalu `id_pesanan` menaik.
Hasil: kolom `id_pesanan`, `jumlah_sku`. Urutan diuji.

### SOAL 4
Pesanan `Selesai` yang nilainya di atas rata-rata nilai pesanan `Selesai` (pakai CTE + subquery), urut nilai menurun.
Hasil: kolom `id_pesanan`, `nilai`. Urutan diuji.

### SOAL 5
SKU yang belum pernah muncul di `item_pesanan` sama sekali (pakai NOT EXISTS), urut A-Z.
Hasil: 1 kolom berisi `sku`. Urutan diuji.

### SOAL 6
Margin kotor per kategori = SUM(qty x (harga - harga_modal)) dari pesanan `Selesai`, urut menurun.
Butuh JOIN 3 tabel.
Hasil: kolom `kategori`, `margin`. Urutan diuji.

### SOAL 7
Pelanggan yang total belanjanya (pesanan `Selesai`) di atas rata-rata pelanggan, urut menurun.
Pakai CTE.
Hasil: kolom `id_pelanggan`, `total_belanja`. Urutan diuji.

### SOAL 8
2 produk terlaris (qty terbanyak) di tiap kategori dari pesanan `Selesai`, pakai ROW_NUMBER().
Urut kategori A-Z, lalu qty menurun.
Hasil: kolom `kategori`, `nama_produk`, `total_qty`. Urutan diuji.

### SOAL 9
Pendapatan per bulan dari pesanan `Selesai` beserta total kumulatifnya, urut bulan.
Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.

### SOAL 10
Rata-rata nilai pesanan `Selesai` per kota, beserta selisihnya dari rata-rata nasional (bulatkan 0 desimal), urut kota A-Z.
Hasil: kolom `kota`, `rata_kota`, `selisih`. Urutan diuji.

### SOAL 11
Pesanan `Selesai` yang berisi lebih dari satu SKU: `id_pesanan` dan total qty-nya, urut total qty menurun lalu `id_pesanan` menaik.
Hasil: kolom `id_pesanan`, `total_qty`. Urutan diuji.

### SOAL 12
Kontribusi tiap kategori terhadap total pendapatan `Selesai`, dalam persen 2 desimal, urut persen menurun (pakai window SUM di atas agregat).
Hasil: kolom `kategori`, `revenue`, `persen`. Urutan diuji.
