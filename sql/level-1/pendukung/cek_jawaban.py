#!/usr/bin/env python3
"""Penilai otomatis jalur SQL level 1.

Cara pakai:  python3 pendukung/cek_jawaban.py  (dari folder sql/level-1)
Semua CSV di pendukung/data/ dimuat ke database SQLite sementara, query di
latihan/jawaban.sql dijalankan, lalu hasilnya dibandingkan dengan kunci.
Tidak butuh library tambahan (stdlib saja).
"""
import csv
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))        # .../pendukung
ROOT = os.path.dirname(HERE)                             # folder latihan ini (level-1 / paket-N)
DATA = os.path.join(HERE, "data")
JAWABAN = os.path.join(ROOT, "latihan", "jawaban.sql")
TABEL = ["penjualan", "kampanye_iklan", "lead", "master_sumber"]
MARKER = re.compile(r"^--\s*=+\s*SOAL\s+(\d+)\s*=+\s*$", re.M)

# Tipe kolom wajib dideklarasikan. Tanpa ini SQLite memberi TEXT affinity ke semua kolom,
# sehingga ORDER BY angka mengurutkan secara abjad dan perbandingan seperti diskon >= 0.1
# membandingkan teks ('0' < '0.1' secara string, bukan angka).
SKEMA = {
    "penjualan": {
        "id": "INTEGER", "tanggal": "TEXT", "bulan": "TEXT", "region": "TEXT", "kanal": "TEXT",
        "produk": "TEXT", "qty": "INTEGER", "harga": "INTEGER", "diskon": "REAL", "revenue": "INTEGER",
    },
    "kampanye_iklan": {
        "tanggal": "TEXT", "id_kampanye": "TEXT", "nama_kampanye": "TEXT", "kanal": "TEXT",
        "impresi": "INTEGER", "klik": "INTEGER", "biaya": "INTEGER", "konversi": "INTEGER",
        "revenue": "INTEGER",
    },
    "lead": {
        "tanggal_masuk": "TEXT", "id_lead": "TEXT", "nama": "TEXT", "kode_sumber": "TEXT",
        "kota": "TEXT", "status": "TEXT", "nilai": "INTEGER",
    },
    "master_sumber": {
        "kode_sumber": "TEXT", "nama_sumber": "TEXT", "biaya_per_lead": "INTEGER",
    },
}

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = {
    1: ("SELECT SUM(revenue) FROM penjualan;", False),
    2: ("SELECT region, SUM(qty) AS total_qty FROM penjualan GROUP BY region ORDER BY total_qty DESC;", True),
    3: ("SELECT id, produk, revenue FROM penjualan ORDER BY revenue DESC LIMIT 5;", True),
    4: ("SELECT COUNT(*) FROM penjualan WHERE diskon >= 0.1;", False),
    5: ("SELECT ROUND(AVG(diskon), 4) FROM penjualan WHERE kanal = 'Marketplace';", False),
    6: ("SELECT bulan, SUM(revenue) AS total_revenue FROM penjualan GROUP BY bulan ORDER BY bulan ASC;", True),
    7: ("SELECT region FROM penjualan GROUP BY region HAVING AVG(revenue) > 5000000 ORDER BY region;", True),
    8: ("SELECT COUNT(DISTINCT produk) FROM penjualan;", False),
    9: ("SELECT kanal, SUM(biaya) AS total_biaya, SUM(revenue) AS total_revenue, "
        "ROUND(1.0*SUM(revenue)/SUM(biaya), 2) AS roas FROM kampanye_iklan GROUP BY kanal "
        "ORDER BY roas DESC;", True),
    10: ("SELECT m.nama_sumber, COUNT(*) AS jumlah_won FROM lead l "
         "JOIN master_sumber m ON m.kode_sumber = l.kode_sumber WHERE l.status = 'Won' "
         "GROUP BY m.nama_sumber ORDER BY jumlah_won DESC;", True),
    11: ("SELECT CASE WHEN nilai >= 50000000 THEN 'BESAR' WHEN nilai >= 10000000 THEN 'MENENGAH' "
         "ELSE 'KECIL' END AS kategori, COUNT(*) AS jumlah, SUM(nilai) AS total_nilai FROM lead "
         "GROUP BY kategori ORDER BY kategori;", True),
    12: ("SELECT kanal, ROUND(1.0*SUM(revenue)/SUM(biaya), 2) AS roas FROM kampanye_iklan "
         "GROUP BY kanal ORDER BY roas DESC LIMIT 1;", False),
}


def bangun_db():
    con = sqlite3.connect(":memory:")
    for t in TABEL:
        with open(os.path.join(DATA, t + ".csv"), encoding="utf-8") as f:
            rows = list(csv.reader(f))
        header, isi = rows[0], [r for r in rows[1:] if r and any(x.strip() for x in r)]
        tipe = SKEMA[t]
        kolom = ", ".join('"%s" %s' % (c, tipe[c]) for c in header)
        con.execute("CREATE TABLE %s (%s)" % (t, kolom))
        con.executemany("INSERT INTO %s VALUES (%s)" % (t, ",".join("?" * len(header))), isi)
    con.commit()
    return con


def baca_jawaban():
    if not os.path.exists(JAWABAN):
        return {}
    teks = open(JAWABAN, encoding="utf-8").read()
    pos = [(m.start(), int(m.group(1))) for m in MARKER.finditer(teks)]
    pos.append((len(teks), None))
    out = {}
    for i in range(len(pos) - 1):
        awal, nomor = pos[i]
        akhir = pos[i + 1][0]
        blok = teks[awal:akhir]
        blok = MARKER.sub("", blok, count=1)
        blok = "\n".join(l for l in blok.splitlines() if not l.strip().startswith("--"))
        blok = blok.strip().rstrip(";").strip()
        out[nomor] = blok
    return out


def norm(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return round(float(v), 4)
    s = str(v).strip()
    try:
        return round(float(s), 4)
    except ValueError:
        return s


def sama(a, b, urut):
    if len(a) != len(b):
        return False, "jumlah baris beda (%d vs %d)" % (len(a), len(b))
    if a and len(a[0]) != len(b[0]):
        return False, "jumlah kolom beda (%d vs %d)" % (len(a[0]), len(b[0]))
    na = [[norm(x) for x in row] for row in a]
    nb = [[norm(x) for x in row] for row in b]
    if ursorted(na, nb):
        if urut:
            beda = [i for i in range(len(na)) if na[i] != nb[i]]
            if not beda:
                return True, ""
            return False, ("isi sudah benar, hanya URUTAN yang beda — soal ini menguji ORDER BY. "
                           "baris ke-%d punyamu %s, kunci %s" % (beda[0] + 1, na[beda[0]], nb[beda[0]]))
        return True, ""
    hanya_a = [r for r in na if str(r) not in [str(x) for x in nb]][:2]
    hanya_b = [r for r in nb if str(r) not in [str(x) for x in na]][:2]
    return False, "isi beda. punyamu %s | kunci %s" % (hanya_a, hanya_b)


def ursorted(na, nb):
    return sorted(map(str, na)) == sorted(map(str, nb))


def tabel(rows):
    if not rows:
        return "(tidak ada baris)"
    return "\n".join("    %r" % (tuple(r),) for r in rows)


def detail(no):
    if no not in KUNCI:
        print("soal %d tidak ada. pilihan: %s" % (no, ", ".join(map(str, sorted(KUNCI)))))
        return 2
    con = bangun_db()
    jawab = baca_jawaban()
    q, urut = KUNCI[no]
    milik = jawab.get(no, "")
    kunci = con.execute(q).fetchall()
    print("SOAL %d — urutan diuji: %s\n" % (no, "YA" if urut else "tidak"))
    print("-- query kamu --")
    print(milik if milik else "(kosong: belum ada query di bawah penanda SOAL %d)" % no)
    hasil = None
    if milik:
        try:
            hasil = con.execute(milik).fetchall()
        except Exception as e:
            print("\n-- hasil kamu --")
            print("ERROR saat dijalankan: %s" % e)
        else:
            print("\n-- hasil kamu (%d baris) --" % len(hasil))
            print(tabel(hasil))
    print("\n-- kunci (%d baris) --" % len(kunci))
    print(q)
    print(tabel(kunci))
    if not milik:
        print("\nKESIMPULAN: soal %d belum diisi — belum ada query di bawah penandanya." % no)
    elif hasil is None:
        print("\nKESIMPULAN: querymu belum bisa dijalankan. Kalau kamu menyalin dari cek_jawaban.py,")
        print("jangan salin tanda kutip ganda dan indentasi Python-nya — ambil isi SQL-nya saja.")
    else:
        ok, pesan = sama(hasil, kunci, urut)
        print("\nKESIMPULAN: %s" % ("BENAR" if ok else pesan))
    con.close()
    return 0


def main():
    arg = sys.argv[1:]
    if arg and arg[0] in ("-d", "--detail"):
        if len(arg) > 1 and arg[1].isdigit():
            return detail(int(arg[1]))
        print("pakai: python3 cek_jawaban.py --detail NOMOR")
        return 2
    con = bangun_db()
    jawab = baca_jawaban()
    benar = 0
    total = len(KUNCI)
    print("Penilai jawaban SQL level 1 — %d soal\n" % total)
    for no in sorted(KUNCI):
        q, urut = KUNCI[no]
        milik = jawab.get(no, "")
        if not milik:
            print("%2d. KOSONG   (belum diisi)" % no)
            continue
        try:
            hasil = con.execute(milik).fetchall()
        except Exception as e:
            print("%2d. SALAH    query error: %s" % (no, str(e)[:90]))
            continue
        kunci = con.execute(q).fetchall()
        ok, pesan = sama(hasil, kunci, urut)
        if ok:
            benar += 1
            print("%2d. BENAR    (%d baris)" % (no, len(hasil)))
        else:
            print("%2d. SALAH    %s" % (no, pesan))
    print("\nSKOR: %d / %d benar" % (benar, total))
    if benar == total:
        print("STATUS: LULUS SEMPURNA - lanjut ke sql/level-2")
    elif benar >= total - 2:
        print("STATUS: LULUS BERSYARAT - perbaiki yang SALAH")
    else:
        print("STATUS: BELUM LULUS - ulangi soal yang SALAH")
    con.close()
    return 0 if benar == total else 1


if __name__ == "__main__":
    sys.exit(main())
