#!/usr/bin/env python3
"""Penilai otomatis Repeat order pelanggan.

Cara pakai:  python3 cek_jawaban.py            (dari folder paket-3)
Semua CSV di data/ dimuat ke database SQLite sementara, query di jawaban.sql dijalankan,
lalu hasilnya dibandingkan dengan kunci. Tidak butuh library tambahan (stdlib saja).
"""
import csv
import os
import re
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
JAWABAN = os.path.join(BASE, "jawaban.sql")
TABEL = ["pesanan", "pelanggan", "ongkir"]
MARKER = re.compile(r"^--\s*=+\s*SOAL\s+(\d+)\s*=+\s*$", re.M)

# Tipe kolom wajib dideklarasikan. Tanpa ini SQLite memberi TEXT affinity ke semua kolom,
# sehingga ORDER BY angka mengurutkan secara abjad dan perbandingan angka jadi perbandingan teks.
SKEMA = {
    "pesanan": {"id_pesanan": "TEXT", "tanggal": "TEXT", "bulan": "TEXT", "id_pelanggan": "TEXT", "kota": "TEXT", "kanal": "TEXT", "qty": "INTEGER", "nilai": "INTEGER"},
    "pelanggan": {"id_pelanggan": "TEXT", "nama": "TEXT", "segmen": "TEXT", "kota_domisili": "TEXT"},
    "ongkir": {"kota": "TEXT", "tarif_per_kg": "INTEGER"},
}

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = {
    1: ('SELECT SUM(nilai) FROM pesanan;', False),
    2: ('SELECT id_pelanggan, COUNT(*) AS jumlah_pesanan FROM pesanan GROUP BY id_pelanggan ORDER BY jumlah_pesanan DESC, id_pelanggan ASC;', True),
    3: ('SELECT p.nama, SUM(o.nilai) AS total_nilai FROM pesanan o JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan GROUP BY p.nama ORDER BY total_nilai DESC LIMIT 3;', True),
    4: ('SELECT COUNT(*) FROM pesanan WHERE nilai >= 1000000;', False),
    5: ("SELECT ROUND(AVG(qty), 2) FROM pesanan WHERE kanal = 'WhatsApp';", False),
    6: ('SELECT bulan, SUM(nilai) AS total_nilai FROM pesanan GROUP BY bulan ORDER BY bulan ASC;', True),
    7: ('SELECT kota FROM pesanan GROUP BY kota HAVING AVG(nilai) > 900000 ORDER BY kota;', True),
    8: ('SELECT COUNT(DISTINCT kota) FROM pesanan;', False),
    9: ('SELECT p.segmen, COUNT(*) AS jumlah_pesanan, SUM(o.nilai) AS total_nilai FROM pesanan o JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan GROUP BY p.segmen ORDER BY total_nilai DESC;', True),
    10: ("SELECT SUM(nilai) FROM pesanan WHERE kanal IN ('Marketplace', 'Website');", False),
    11: ("SELECT COUNT(*) FROM pesanan o JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan WHERE p.nama LIKE '%Putri%';", False),
    12: ('SELECT g.kota FROM ongkir g LEFT JOIN pesanan o ON o.kota = g.kota WHERE o.kota IS NULL;', False),
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
    if urut:
        beda = [i for i in range(len(na)) if na[i] != nb[i]]
        return (not beda), ("baris ke-%d beda: %s vs %s" % (beda[0] + 1, na[beda[0]], nb[beda[0]])
                            if beda else "")
    if sorted(map(str, na)) != sorted(map(str, nb)):
        hanya_a = [r for r in na if str(r) not in [str(x) for x in nb]][:2]
        hanya_b = [r for r in nb if str(r) not in [str(x) for x in na]][:2]
        return False, "isi beda. punyamu %s | kunci %s" % (hanya_a, hanya_b)
    return True, ""


def main():
    con = bangun_db()
    jawab = baca_jawaban()
    benar = 0
    total = len(KUNCI)
    print("Penilai jawaban Repeat order pelanggan — %d soal\n" % total)
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
