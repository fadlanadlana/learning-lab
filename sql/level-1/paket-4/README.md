# paket-4 — Biaya iklan dan CPL per platform

Paket soal SQL level 1 (mandiri, data sendiri). Tingkat kesulitan sama dengan `../level-1`:
SELECT, WHERE, ORDER BY, LIMIT, agregasi, GROUP BY, HAVING, satu JOIN, CASE, DISTINCT, LIKE, IN.

## Isi folder

| File | Fungsi |
|---|---|
| `soal.md` | 12 soal + hasil yang diharapkan (kolom & urutan) |
| `jawaban.sql` | **kamu tulis query di sini**, di bawah tiap penanda `-- === SOAL n ===` |
| `cek_jawaban.py` | penilai otomatis: CSV -> SQLite, querymu dijalankan, dibandingkan dengan kunci |
| `data/*.csv` | 2 tabel: `iklan_harian` (24 baris), `platform_master` (4 baris) |

## Cara mengerjakan

```
cd sql/level-1/paket-4
unset LD_LIBRARY_PATH            # hanya di Termux; di PC/Linux lewati baris ini
python3 cek_jawaban.py           # jalankan penilai
```

Penilai menampilkan **KOSONG**, **BENAR**, atau **SALAH** per soal, lalu skor.
Database dibangun ulang dari CSV setiap kali dijalankan.

## Kriteria lulus

12/12 BENAR. 10-11 benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris x kolom), bukan nama alias kolom.
- **Urutan baris** hanya diuji pada soal yang meminta `ORDER BY`.
- Angka dibandingkan dengan toleransi 4 desimal.

## Data

`iklan_harian` 24 baris (2026-08 s/d 2026-10) dari 3 platform dan 7 kreatif; `platform_master` 4 baris, `LinkedIn` sengaja tanpa baris iklan.
