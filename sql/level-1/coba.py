#!/usr/bin/env python3
"""Coba query SQL langsung tanpa mengubah jawaban.sql.

Pakai (dari folder sql/level-1):
    python3 coba.py "SELECT * FROM penjualan LIMIT 5"
    python3 coba.py "SELECT region, SUM(revenue) FROM penjualan GROUP BY region"

Semua CSV di data/ dimuat ke database SQLite di memori (tabel: penjualan, kampanye_iklan,
lead, master_sumber), lalu query-mu dijalankan dan hasilnya dicetak sebagai tabel sederhana.
"""
import csv
import os
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
TABEL = ["penjualan", "kampanye_iklan", "lead", "master_sumber"]

# Tipe kolom diambil dari cek_jawaban.py supaya coba.py dan penilai memakai skema yang sama.
# Tanpa tipe, SQLite memberi TEXT affinity dan angka terurut seperti teks.
sys.path.insert(0, BASE)
from cek_jawaban import SKEMA  # noqa: E402


def bangun():
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


def cetak(header, rows):
    if not rows:
        print("(tidak ada baris)")
        return
    kolom = header or ["kolom%d" % (i + 1) for i in range(len(rows[0]))]
    isi = [[("" if v is None else ("%.2f" % v if isinstance(v, float) else str(v))) for v in r] for r in rows]
    lebar = [max(len(str(kolom[i])), *(len(r[i]) for r in isi)) for i in range(len(kolom))]
    garis = "+".join("-" * (w + 2) for w in lebar)
    print(garis)
    print("| " + " | ".join(str(kolom[i]).ljust(lebar[i]) for i in range(len(kolom))) + " |")
    print(garis)
    for r in isi:
        print("| " + " | ".join(r[i].ljust(lebar[i]) for i in range(len(kolom))) + " |")
    print(garis)
    print("%d baris" % len(rows))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Tabel:", ", ".join(TABEL))
        return 1
    q = " ".join(sys.argv[1:])
    con = bangun()
    try:
        cur = con.execute(q)
        rows = cur.fetchall()
        header = [d[0] for d in cur.description] if cur.description else []
    except Exception as e:
        print("ERROR:", e)
        return 1
    cetak(header, rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())