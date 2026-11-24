#!/usr/bin/env python3
"""Penilai otomatis Kunjungan pelanggan per kanal (window function).

Cara pakai:  python3 pendukung/cek_jawaban.py
Semua CSV di pendukung/data/ dimuat ke database SQLite sementara, query di
latihan/paket-3-jawaban.sql dijalankan, lalu hasilnya dibandingkan dengan kunci.
"""
import csv
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAMA_SET = "paket-3"
DATA = os.path.join(HERE, "data")


def _cari_latihan(mulai):
    """Semua soal & jawaban ada di satu folder latihan/ bersama, di atas pendukung/."""
    d = mulai
    for _ in range(4):
        kandidat = os.path.join(d, "latihan")
        if os.path.isdir(kandidat):
            return kandidat
        d = os.path.dirname(d)
    raise SystemExit("folder latihan tidak ditemukan di atas %s" % mulai)


LATIHAN = _cari_latihan(HERE)
JAWABAN = os.path.join(LATIHAN, NAMA_SET + "-jawaban.sql")
TABEL = ["kunjungan", "pelanggan"]
MARKER = re.compile(r"^--\s*=+\s*SOAL\s+(\d+)\s*=+\s*$", re.M)

# Tipe kolom wajib dideklarasikan, kalau tidak SQLite memberi TEXT affinity dan
# ORDER BY angka mengurutkan secara abjad.
SKEMA = {
    "kunjungan": {"tanggal": "TEXT", "bulan": "TEXT", "id_pelanggan": "TEXT", "kanal": "TEXT", "sesi": "INTEGER", "revenue": "INTEGER"},
    "pelanggan": {"id_pelanggan": "TEXT", "nama": "TEXT", "kota": "TEXT"},
}

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = {
    1: ('SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal ORDER BY total_revenue DESC;', True),
    2: ('WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan) SELECT bulan, revenue, SUM(revenue) OVER (ORDER BY bulan) AS kumulatif FROM t ORDER BY bulan;', True),
    3: ('WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan) SELECT bulan, revenue, ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY bulan)) / LAG(revenue) OVER (ORDER BY bulan), 2) AS growth_persen FROM t ORDER BY bulan;', True),
    4: ('WITH t AS (SELECT bulan, kanal, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan, kanal) SELECT bulan, kanal, revenue, RANK() OVER (PARTITION BY bulan ORDER BY revenue DESC) AS peringkat FROM t ORDER BY bulan, peringkat;', True),
    5: ('SELECT id_pelanggan, bulan, revenue FROM (SELECT id_pelanggan, bulan, revenue, ROW_NUMBER() OVER (PARTITION BY id_pelanggan ORDER BY revenue DESC) AS rn FROM kunjungan) WHERE rn = 1 ORDER BY id_pelanggan;', True),
    6: ('SELECT kanal, bulan, revenue, ROUND(AVG(revenue) OVER (PARTITION BY kanal), 0) AS rata_kanal FROM kunjungan ORDER BY kanal, bulan, revenue DESC;', True),
    7: ('WITH t AS (SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal) SELECT kanal, total_revenue, DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS peringkat FROM t ORDER BY peringkat;', True),
    8: ('WITH t AS (SELECT bulan, kanal, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan, kanal) SELECT bulan, kanal, revenue, FIRST_VALUE(kanal) OVER (PARTITION BY bulan ORDER BY revenue DESC) AS kanal_top FROM t ORDER BY bulan, revenue DESC;', True),
    9: ('SELECT id_pelanggan, bulan, revenue, SUM(revenue) OVER (PARTITION BY id_pelanggan ORDER BY bulan) AS kumulatif FROM kunjungan ORDER BY id_pelanggan, bulan;', True),
    10: ('SELECT id_pelanggan, bulan, revenue, revenue - LAG(revenue) OVER (PARTITION BY id_pelanggan ORDER BY bulan) AS selisih FROM kunjungan ORDER BY id_pelanggan, bulan;', True),
    11: ('SELECT kanal, COUNT(DISTINCT id_pelanggan) AS jumlah_pelanggan FROM kunjungan GROUP BY kanal ORDER BY jumlah_pelanggan DESC, kanal ASC;', True),
    12: ('WITH t AS (SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal) SELECT kanal, total_revenue FROM t WHERE total_revenue > (SELECT AVG(total_revenue) FROM t) ORDER BY total_revenue DESC;', True),
}


def bangun_db():
    con = sqlite3.connect(":memory:")
    for t in TABEL:
        with open(os.path.join(DATA, t + ".csv"), encoding="utf-8") as f:
            rows = list(csv.reader(f))
        header, isi = rows[0], [r for r in rows[1:] if r and any(x.strip() for x in r)]
        kolom = ", ".join('"%s" %s' % (c, SKEMA[t][c]) for c in header)
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
        out[nomor] = blok.strip().rstrip(";").strip()
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


def ursorted(na, nb):
    return sorted(map(str, na)) == sorted(map(str, nb))


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
            return False, ("isi sudah benar, hanya URUTAN yang beda - soal ini menguji ORDER BY. "
                           "baris ke-%d punyamu %s, kunci %s" % (beda[0] + 1, na[beda[0]], nb[beda[0]]))
        return True, ""
    hanya_a = [r for r in na if str(r) not in [str(x) for x in nb]][:2]
    hanya_b = [r for r in nb if str(r) not in [str(x) for x in na]][:2]
    return False, "isi beda. punyamu %s | kunci %s" % (hanya_a, hanya_b)


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
    print("SOAL %d - urutan diuji: %s\n" % (no, "YA" if urut else "tidak"))
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
        print("\nKESIMPULAN: soal %d belum diisi - belum ada query di bawah penandanya." % no)
    elif hasil is None:
        print("\nKESIMPULAN: querymu belum bisa dijalankan (lihat pesan ERROR di atas).")
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
    print("Penilai jawaban Kunjungan pelanggan per kanal (window function) - %d soal\n" % total)
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
        print("STATUS: LULUS SEMPURNA")
    elif benar >= total - 2:
        print("STATUS: LULUS BERSYARAT - perbaiki yang SALAH")
    else:
        print("STATUS: BELUM LULUS - ulangi soal yang SALAH")
    con.close()
    return 0 if benar == total else 1


if __name__ == "__main__":
    sys.exit(main())
