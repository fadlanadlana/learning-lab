-- Jawaban Repeat order pelanggan
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

-- === SOAL 1 ===
SELECT
SUM(nilai) AS total_pesanan
FROM pesanan;

-- === SOAL 2 ===
SELECT
id_pelanggan,
COUNT(id_pelanggan) AS jumlah_pesanan
FROM pesanan
GROUP BY id_pelanggan
ORDER BY jumlah_pesanan DESC, id_pelanggan ASC;

-- === SOAL 3 ===
SELECT m.nama,
SUM (t.nilai) AS total_nilai
FROM pesanan t
JOIN pelanggan m ON t.id_pelanggan = m.id_pelanggan
GROUP BY m.nama
ORDER BY total_nilai DESC
LIMIT 3;

-- === SOAL 4 ===
SELECT
COUNT(nilai) AS jumlah_pesanan
FROM pesanan
WHERE nilai >= 1000000;

-- === SOAL 5 ===
SELECT
ROUND(AVG(qty),2) AS avg_qtywa
FROM pesanan
WHERE kanal = 'WhatsApp'; 

-- === SOAL 6 ===
SELECT
bulan,
SUM(nilai) AS total_nilai
FROM pesanan
GROUP BY bulan
ORDER BY bulan ASC;

-- === SOAL 7 ===
SELECT kota
FROM pesanan
GROUP BY kota
HAVING AVG(nilai) >= 900000
ORDER BY kota ASC;

-- === SOAL 8 ===
SELECT
COUNT(DISTINCT kota) AS unq_kota
FROM pesanan;

-- === SOAL 9 ===
SELECT
m.segmen,
COUNT (t.id_pesanan) AS jumlah_pesanan,
SUM (t.nilai) AS total_nilai
FROM pesanan t 
JOIN pelanggan m ON t.id_pelanggan = m.id_pelanggan
GROUP BY segmen
ORDER BY total_nilai DESC;

-- === SOAL 10 ===
SELECT
SUM(nilai) AS total_nilai
FROM pesanan
WHERE kanal IN ('Marketplace' , 'Website');

-- === SOAL 11 ===
SELECT
COUNT(*) AS jumlah_pesanan
FROM pesanan t
JOIN pelanggan m ON t.id_pelanggan = m.id_pelanggan
WHERE m.nama LIKE '%Putri%';

-- === SOAL 12 ===
SELECT g.kota
FROM ongkir g LEFT JOIN pesanan o ON o.kota = g.kota
WHERE o.kota IS NULL;

