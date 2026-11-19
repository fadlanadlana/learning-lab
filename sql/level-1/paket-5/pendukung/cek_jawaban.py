#!/usr/bin/env python3
"""Penilai otomatis Penjualan produk dan status stok.

Cara pakai:  python3 pendukung/cek_jawaban.py  (dari folder paket-5)
Semua CSV di pendukung/data/ dimuat ke database SQLite sementara, query di latihan/jawaban.sql
dijalankan, lalu hasilnya dibandingkan dengan kunci. Tidak butuh library tambahan (stdlib saja).
"""
import csv
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))        # .../pendukung
ROOT = os.path.dirname(HERE)                             # folder paket (paket-N)
DATA = os.path.join(HERE, "data")
JAWABAN = os.path.join(ROOT, "latihan", "jawaban.sql")
TABEL = ["penjualan_produk", "produk"]
MARKER = re.compile(r"^--\s*=+\s*SOAL\s+(\d+)\s*=+\s*$", re.M)

# Tipe kolom wajib dideklarasikan. Tanpa ini SQLite memberi TEXT affinity ke semua kolom,
# sehingga ORDER BY angka mengurutkan secara abjad dan perbandingan angka jadi perbandingan teks.
SKEMA = {
    "penjualan_produk": {"tanggal": "TEXT", "bulan": "TEXT", "sku": "TEXT", "qty": "INTEGER", "harga": "INTEGER", "revenue": "INTEGER"},
    "produk": {"sku": "TEXT", "nama_produk": "TEXT", "kategori": "TEXT", "stok_akhir": "INTEGER", "harga_modal": "INTEGER"},
}

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = {
    1: ('SELECT SUM(qty) FROM penjualan_produk;', False),
    2: ('SELECT p.kategori, SUM(s.qty) AS total_qty FROM penjualan_produk s JOIN produk p ON p.sku = s.sku GROUP BY p.kategori ORDER BY total_qty DESC;', True),
    3: ('SELECT tanggal, sku, revenue FROM penjualan_produk ORDER BY revenue DESC LIMIT 5;', True),
    4: ('SELECT COUNT(*) FROM penjualan_produk WHERE qty >= 20;', False),
    5: ("SELECT ROUND(AVG(s.harga), 0) FROM penjualan_produk s JOIN produk p ON p.sku = s.sku WHERE p.kategori = 'Sepatu';", False),
    6: ('SELECT bulan, SUM(revenue) AS total_revenue FROM penjualan_produk GROUP BY bulan ORDER BY bulan ASC;', True),
    7: ('SELECT p.kategori FROM penjualan_produk s JOIN produk p ON p.sku = s.sku GROUP BY p.kategori HAVING SUM(s.qty) > 80 ORDER BY p.kategori;', True),
    8: ('SELECT COUNT(DISTINCT sku) FROM penjualan_produk;', False),
    9: ('SELECT p.nama_produk, SUM(s.qty) AS total_qty FROM penjualan_produk s JOIN produk p ON p.sku = s.sku GROUP BY p.nama_produk ORDER BY total_qty DESC;', True),
    10: ("SELECT SUM(s.revenue) FROM penjualan_produk s JOIN produk p ON p.sku = s.sku WHERE p.kategori = 'Aksesoris';", False),
    11: ("SELECT CASE WHEN stok_akhir = 0 THEN 'HABIS' WHEN stok_akhir < 10 THEN 'TIPIS' ELSE 'AMAN' END AS label_stok, COUNT(*) AS jumlah_sku FROM produk GROUP BY label_stok ORDER BY label_stok;", True),
    12: ('SELECT p.sku FROM produk p LEFT JOIN penjualan_produk s ON s.sku = p.sku WHERE s.sku IS NULL ORDER BY p.sku;', True),
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
    if hasil is None:
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
    print("Penilai jawaban Penjualan produk dan status stok — %d soal\n" % total)
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
