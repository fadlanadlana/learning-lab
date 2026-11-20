-- Jawaban SQL Level 1
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Contoh bentuk jawaban:
--   SELECT region, SUM(qty) AS total_qty
--   FROM penjualan
--   GROUP BY region
--   ORDER BY total_qty DESC;
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

-- === SOAL 1 ===
SELECT SUM(revenue) AS total_revenue_pen
FROM penjualan;

-- === SOAL 2 ===
SELECT
	region, 
	SUM(qty) AS total_qty
FROM penjualan
GROUP BY region
ORDER BY total_qty DESC;

-- === SOAL 3 ===

SELECT id, produk, revenue FROM penjualan ORDER BY revenue DESC LIMIT 5;


-- === SOAL 4 ===
SELECT COUNT(*) AS total_diskon
FROM penjualan
WHERE diskon >=0.1;


-- === SOAL 5 ===

SELECT ROUND(AVG(diskon),4) FROM penjualan WHERE kanal ='Marketplace';

-- === SOAL 6 ===

SELECT bulan, SUM(revenue) AS total_revenue FROM penjualan GROUP BY bulan ORDER BY bulan ASC;

-- === SOAL 7 ===

SELECT region  FROM penjualan GROUP BY region
HAVING AVG(revenue) > 5000000 ORDER BY region;

-- === SOAL 8 ===

SELECT COUNT(DISTINCT produk)
FROM penjualan;

-- === SOAL 9 ===

SELECT
kanal,
 SUM(biaya) AS total_biaya,
 SUM(revenue) AS total_revenue,
 ROUND(1.0*SUM(revenue)/SUM(biaya),2) AS roas
FROM kampanye_iklan GROUP BY kanal
ORDER BY roas DESC;

-- === SOAL 10 ===
SELECT m.nama_sumber, COUNT(*) AS jumlah_won FROM lead l
 JOIN master_sumber m ON m.kode_sumber = l.kode_sumber WHERE l.status = 'Won'
 GROUP BY m.nama_sumber ORDER BY jumlah_won DESC;

-- === SOAL 11 ===

 SELECT CASE WHEN nilai >= 50000000 THEN 'BESAR'
 WHEN nilai >= 10000000 THEN 'MENENGAH'
 ELSE 'KECIL' END AS kategori, COUNT(*) AS jumlah, SUM(nilai) AS total_nilai FROM lead
 GROUP BY kategori ORDER BY kategori;


-- === SOAL 12 ===

SELECT
 kanal,
	ROUND(1.0*SUM(revenue)/SUM(biaya),2) AS roas 
FROM kampanye_iklan
GROUP BY kanal
ORDER BY roas
DESC LIMIT 1;
