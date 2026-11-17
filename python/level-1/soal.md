# Soal Python Level 1

Semua fungsi ada di `jawaban.py`. Data dibaca dari `data/`.

Kolom `penjualan.csv`: id, tanggal, bulan, region, kanal, produk, qty, harga, diskon, revenue
(`diskon` pecahan: 0.1 = 10%; `bulan` format `2026-08`).

Kolom `kampanye_iklan.csv`: tanggal, id_kampanye, nama_kampanye, kanal, impresi, klik, biaya,
konversi, revenue.

Kolom `lead.csv`: tanggal_masuk, id_lead, nama, kode_sumber, kota, status, nilai
(kolom `nama` masih kotor: spasi ganda, huruf besar semua, spasi di ujung).

---

### SOAL 1 — `baca_csv(path)`
Baca file CSV menjadi `list` berisi `dict` per baris, dengan konversi tipe:
kolom yang isinya angka bulat jadi `int`, angka desimal jadi `float`, sisanya `str`.
Contoh: baris pertama `penjualan.csv` harus menjadi
`{"id": 1, "tanggal": "2026-08-01", "bulan": "2026-08", "region": "Jawa Barat",
 "kanal": "Distributor", "produk": "PR-02 Kaos Polos", "qty": 21, "harga": 95000,
 "diskon": 0, "revenue": 1995000}` — perhatikan `id`, `qty`, `harga` bertipe `int`.

### SOAL 2 — `total_revenue(rows)`
Jumlahkan kolom `revenue`. Keluaran: `int`.

### SOAL 3 — `total_qty(rows)`
Jumlahkan kolom `qty`. Keluaran: `int`.

### SOAL 4 — `revenue_per_region(rows)`
Keluaran: `dict` {nama region: total revenue}. Semua region harus muncul.

### SOAL 5 — `transaksi_terbesar(rows)`
Keluaran: satu `dict` berisi baris dengan `revenue` terbesar.

### SOAL 6 — `id_diskon_minimal(rows, batas)`
Keluaran: `list` berisi `id` yang diskonnya >= `batas`, diurutkan menaik.
Contoh: `id_diskon_minimal(rows, 0.1)`.

### SOAL 7 — `rata_rata_diskon_kanal(rows, kanal)`
Rata-rata kolom `diskon` untuk kanal tertentu. Keluaran: `float` (4 desimal).
Contoh: `rata_rata_diskon_kanal(rows, "Marketplace")`.

### SOAL 8 — `growth_bulanan(rows, bulan_awal, bulan_akhir)`
Pertumbuhan revenue: (revenue bulan akhir - bulan awal) / revenue bulan awal.
Keluaran: `float` (4 desimal). Contoh: `growth_bulanan(rows, "2026-09", "2026-10")`.

### SOAL 9 — `produk_unik(rows)`
Keluaran: `list` nama produk unik, diurutkan menaik (A-Z).

### SOAL 10 — `top_produk(rows, n)`
Keluaran: `list` berisi `tuple` (nama produk, total revenue), diurutkan dari terbesar,
sebanyak `n`. Contoh: `top_produk(rows, 3)`.

### SOAL 11 — `roas_total(kampanye)`
Dari data kampanye iklan: total revenue dibagi total biaya. Keluaran: `float` (2 desimal).

### SOAL 12 — `bersihkan_nama(nama)`
Rapikan nama: buang spasi di ujung, rapatkan spasi ganda, jadikan huruf besar di awal kata.
`"  RINA  kartika "` → `"Rina Kartika"`.
