-- Jawaban Biaya iklan dan CPL per platform
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

-- === SOAL 1 ===
SELECT 
SUM (biaya) AS total_biaya
FROM iklan_harian;

-- === SOAL 2 ===
SELECT
platform,
SUM (impresi) AS total_impresi
FROM iklan_harian
GROUP BY platform
ORDER BY total_impresi DESC;

-- === SOAL 3 ===
SELECT
tanggal,
kreatif,
klik
FROM iklan_harian
ORDER BY klik DESC
LIMIT 5;

-- === SOAL 4 ===
SELECT
COUNT(*) AS jumlah_bk
FROM iklan_harian
WHERE lead < 20;

-- === SOAL 5 ===
SELECT
ROUND(1.0*SUM(klik)/SUM(impresi),4)
FROM iklan_harian
WHERE platform = 'TikTok';

-- === SOAL 6 ===
SELECT
bulan,
SUM(biaya) AS total_biaya
FROM iklan_harian
GROUP BY bulan
ORDER BY bulan ASC;

-- === SOAL 7 ===
SELECT
kreatif,
SUM(lead) AS total_lead
FROM iklan_harian
GROUP BY kreatif
HAVING total_lead >= 100
ORDER BY total_lead DESC;

-- === SOAL 8 ===
SELECT
COUNT(DISTINCT kreatif)
FROM iklan_harian;

-- === SOAL 9 ===

SELECT
platform,
SUM (biaya) AS total_biaya,
SUM (lead) AS total_lead,
ROUND (1.0*SUM(biaya)/SUM(lead),0) AS cpl
FROM iklan_harian
GROUP BY platform
ORDER BY cpl;

-- === SOAL 10 ===
SELECT
SUM (lead) AS total_lead
FROM iklan_harian t
JOIN platform_master m ON t.platform = m.platform
WHERE jenis = 'Search';

-- === SOAL 11 ===
SELECT
platform,
CASE
 WHEN ROUND(1.0*SUM(biaya)/SUM(lead),0) <= 45000 THEN 'EFISIEN'
 WHEN ROUND(1.0*SUM(biaya)/SUM(lead),0) <= 55000 THEN 'SEDANG'
 ELSE 'MAHAL' END AS label_cpl
FROM iklan_harian
GROUP BY platform
ORDER BY label_cpl ASC, platform ASC; 

-- === SOAL 12 ===

SELECT
m.platform
FROM platform_master m LEFT JOIN iklan_harian t ON t.platform = m.platform
WHERE t.platform IS NULL; 
