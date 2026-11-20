-- Jawaban Funnel website per kanal
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

-- === SOAL 1 ===
SELECT SUM(sesi) AS total_sesi
FROM trafik;

-- === SOAL 2 ===
SELECT
device,
SUM(sesi) AS total_sesi
FROM trafik
GROUP BY device
ORDER BY total_sesi DESC;

-- === SOAL 3 ===
SELECT
 tanggal,
 kanal,
 revenue
FROM trafik
ORDER BY revenue DESC
LIMIT 5;

-- === SOAL 4 ===
SELECT
 COUNT(*) AS total_trafik 
 FROM trafik
 WHERE revenue < 1000000;

-- === SOAL 5 ===
SELECT ROUND(1.0*SUM(revenue)/SUM(sesi), 4)
FROM trafik 
WHERE kanal = 'Email';

-- === SOAL 6 ===
SELECT bulan,
SUM(revenue) AS total_revenue
FROM trafik 
GROUP BY bulan ORDER BY bulan ASC;

-- === SOAL 7 ===
SELECT kanal FROM trafik GROUP BY kanal 
HAVING SUM(sesi) > 1500 ORDER BY kanal ASC;

-- === SOAL 8 ===
SELECT COUNT(DISTINCT device) AS total_device
FROM trafik;

-- === SOAL 9 ===

SELECT t.kanal,
 SUM(t.sesi*m.biaya_per_klik) AS total_biaya,
 SUM(t.revenue) AS total_revenue,
 ROUND(1.0*SUM(t.revenue)/SUM(t.sesi*m.biaya_per_klik), 2) AS roas FROM trafik t
 JOIN kanal_master m ON m.kanal = t.kanal GROUP BY t.kanal
 ORDER BY roas DESC;

-- === SOAL 10 ===

SELECT t.kanal,
 SUM(t.revenue) AS total_revenue
 FROM trafik t JOIN kanal_master m ON m.kanal = t.kanal
 WHERE m.jenis = 'Paid'
GROUP BY t.kanal ORDER BY t.kanal;

-- === SOAL 11 ===
SELECT
kanal,
CASE
 WHEN SUM(revenue) >= 15000000 THEN 'UTAMA'
 WHEN SUM(revenue) >= 8000000 THEN 'POTENSIAL'
 ELSE 'KECIL' END AS label
FROM trafik GROUP BY kanal ORDER BY label, kanal;

-- === SOAL 12 ===

SELECT m.kanal FROM kanal_master m
LEFT JOIN trafik t ON t.kanal = m.kanal WHERE t.kanal IS NULL;

