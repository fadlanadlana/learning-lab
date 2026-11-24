# Soal SQL Level 2 - Paket 1 - Subquery, CTE, dan window function pada data penjualan

Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):

| Tabel | Kolom |
|---|---|
| `penjualan` | id, tanggal, bulan, region, kanal, produk, qty, harga, diskon, revenue |
| `kampanye_iklan` | tanggal, id_kampanye, nama_kampanye, kanal, impresi, klik, biaya, konversi, revenue |
| `lead` | tanggal_masuk, id_lead, nama, kode_sumber, kota, status, nilai |
| `master_sumber` | kode_sumber, nama_sumber, biaya_per_lead |

Data sama dengan SQL level 1 (penjualan 60 baris, kampanye_iklan 30, lead 28, master_sumber 4), tapi soal-soalnya menuntut subquery, CTE, dan window function. SQLite di sini mendukung CTE (`WITH`) dan window function (`OVER`).

Kerjakan di `paket-1-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal.

---

### SOAL 1
Jumlah transaksi yang `revenue`-nya di atas rata-rata seluruh transaksi (pakai subquery).
Hasil: 1 kolom, 1 baris.

### SOAL 2
Produk unik yang pernah terjual di region `Jabodetabek` (pakai IN + subquery), urut A-Z.
Hasil: 1 kolom berisi `produk`. Urutan diuji.

### SOAL 3
Total revenue per region, hanya region yang totalnya di atas rata-rata total antar-region.
Pakai derived table (subquery di FROM) atau CTE.
Hasil: kolom `region`, `total_revenue`. Urutan diuji (region A-Z).

### SOAL 4
Nama sumber lead yang punya minimal satu lead berstatus `Won` (pakai EXISTS), urut A-Z.
Hasil: 1 kolom berisi `nama_sumber`. Urutan diuji.

### SOAL 5
Produk yang **tidak pernah** terjual di region `Sumatera` (pakai NOT EXISTS), urut A-Z.
Hasil: 1 kolom berisi `produk`. Urutan diuji.

### SOAL 6
Kanal iklan yang total biayanya di atas rata-rata total biaya antar-kanal, urut biaya menurun.
Pakai CTE.
Hasil: kolom `kanal`, `total_biaya`. Urutan diuji.

### SOAL 7
Per nama sumber lead: jumlah lead, jumlah lead `Won`, dan total biaya sumber itu (jumlah lead x `biaya_per_lead`), urut total biaya menurun.
Hasil: kolom `nama_sumber`, `jumlah_lead`, `jumlah_won`, `total_biaya`. Urutan diuji.

### SOAL 8
Transaksi terbesar di tiap region (satu baris per region), pakai ROW_NUMBER().
Hasil: kolom `region`, `id`, `revenue`. Urutan diuji (region A-Z).

### SOAL 9
Revenue per bulan beserta total kumulatif sampai bulan itu (window SUM), urut bulan.
Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.

### SOAL 10
Revenue per bulan beserta selisih terhadap bulan sebelumnya (pakai LAG), urut bulan.
Hasil: kolom `bulan`, `revenue`, `selisih`. Urutan diuji.

### SOAL 11
Per region: total revenue dan persentase kontribusinya terhadap total seluruh region (pakai window SUM di atas agregat), dibulatkan 2 desimal, urut persen menurun.
Hasil: kolom `region`, `total_revenue`, `persen`. Urutan diuji.

### SOAL 12
Jumlah transaksi yang revenue-nya di atas rata-rata **region-nya sendiri** (subquery berkorelasi), 1 baris.
Hasil: 1 kolom, 1 baris.
