-- Jawaban Penjualan produk dan status stok
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

-- === SOAL 1 ===
SELECT
SUM(qty) AS total_qty
FROM penjualan_produk;

-- === SOAL 2 ===
SELECT
m.kategori,
SUM(t.qty) AS total_qty
FROM penjualan_produk t
JOIN produk m ON m.sku = t.sku
GROUP BY m.kategori
ORDER BY total_qty DESC; 

-- === SOAL 3 ===
SELECT tanggal,sku,revenue
FROM penjualan_produk
GROUP BY revenue
ORDER BY revenue DESC
LIMIT 5;

-- === SOAL 4 ===
SELECT COUNT(*) AS jumlah_transaksi
FROM penjualan_produk
WHERE qty >= 20;

-- === SOAL 5 ===
SELECT AVG(m.harga) AS rata_harga
FROM penjualan_produk m
JOIN produk t ON m.sku = t.sku
WHERE kategori = 'Sepatu';

-- === SOAL 6 ===
SELECT bulan, SUM(revenue) AS total_revenue
FROM penjualan_produk
GROUP BY bulan
ORDER BY bulan ASC;

-- === SOAL 7 ===
SELECT m.kategori
FROM penjualan_produk t
JOIN produk m ON t.sku = m.sku
GROUP BY m.kategori
HAVING SUM(t.qty) >= 80
ORDER by m.kategori ASC; 

-- === SOAL 8 ===
SELECT COUNT(DISTINCT sku) AS sku_unik
FROM penjualan_produk;

-- === SOAL 9 ===
SELECT t.nama_produk, SUM(m.qty) AS total_qty
FROM produk t
JOIN penjualan_produk m ON t.sku = m.sku
GROUP BY t.nama_produk
ORDER BY total_qty DESC;

-- === SOAL 10 ===
SELECT SUM(m.revenue) AS total_revenue
FROM penjualan_produk m
JOIN produk t ON t.sku = m.sku
WHERE kategori ='Aksesoris'; 

-- === SOAL 11 ===
SELECT
CASE 
WHEN stok_akhir = 0 THEN 'HABIS'
WHEN stok_akhir < 10 THEN 'TIPIS'
ELSE 'AMAN' END AS label_stok,
COUNT(*) AS jumlah_sku
FROM produk 
GROUP BY label_stok
ORDER BY label_stok;

-- === SOAL 12 ===
SELECT m.sku
FROM produk m LEFT JOIN penjualan_produk t ON t.sku = m.sku
WHERE t.sku IS NULL ORDER BY m.sku;
