#!/usr/bin/env python3
"""Penilai otomatis jalur Python level 1.

Cara pakai (dari folder python/level-1):
    python3 cek_jawaban.py

Fungsi di jawaban.py dipanggil satu per satu lalu dibandingkan dengan kunci yang dihitung di
file ini dari data/ (stdlib saja, tanpa pandas).
"""
import csv
import importlib.util
import os
import sys
import traceback

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")


def _konversi(v):
    s = v.strip()
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return v


def muat(nama):
    with open(os.path.join(DATA, nama), encoding="utf-8") as f:
        return [{k: _konversi(v) for k, v in row.items()} for row in csv.DictReader(f)]


PENJUALAN = muat("penjualan.csv")
KAMPANYE = muat("kampanye_iklan.csv")
LEAD = muat("lead.csv")

# ---------------------------------------------------------------- kunci
def k_revenue_per_region():
    d = {}
    for r in PENJUALAN:
        d[r["region"]] = d.get(r["region"], 0) + r["revenue"]
    return d


def k_top_produk(n):
    tot = {}
    for r in PENJUALAN:
        tot[r["produk"]] = tot.get(r["produk"], 0) + r["revenue"]
    return sorted(tot.items(), key=lambda kv: -kv[1])[:n]


KUNCI = {
    1: ("baca_csv", (os.path.join(DATA, "penjualan.csv"),),
        {"id": 1, "tanggal": "2026-08-01", "bulan": "2026-08", "region": "Jawa Barat",
         "kanal": "Distributor", "produk": "PR-02 Kaos Polos", "qty": 21, "harga": 95000,
         "diskon": 0, "revenue": 1995000}),
    2: ("total_revenue", (PENJUALAN,), sum(r["revenue"] for r in PENJUALAN)),
    3: ("total_qty", (PENJUALAN,), sum(r["qty"] for r in PENJUALAN)),
    4: ("revenue_per_region", (PENJUALAN,), k_revenue_per_region()),
    5: ("transaksi_terbesar", (PENJUALAN,), max(PENJUALAN, key=lambda r: r["revenue"])),
    6: ("id_diskon_minimal", (PENJUALAN, 0.1),
        sorted(r["id"] for r in PENJUALAN if r["diskon"] >= 0.1)),
    7: ("rata_rata_diskon_kanal", (PENJUALAN, "Marketplace"),
        round(sum(r["diskon"] for r in PENJUALAN if r["kanal"] == "Marketplace")
              / sum(1 for r in PENJUALAN if r["kanal"] == "Marketplace"), 4)),
    8: ("growth_bulanan", (PENJUALAN, "2026-09", "2026-10"),
        round((sum(r["revenue"] for r in PENJUALAN if r["bulan"] == "2026-10")
               - sum(r["revenue"] for r in PENJUALAN if r["bulan"] == "2026-09"))
              / sum(r["revenue"] for r in PENJUALAN if r["bulan"] == "2026-09"), 4)),
    9: ("produk_unik", (PENJUALAN,), sorted({r["produk"] for r in PENJUALAN})),
    10: ("top_produk", (PENJUALAN, 3), k_top_produk(3)),
    11: ("roas_total", (KAMPANYE,),
         round(sum(r["revenue"] for r in KAMPANYE) / sum(r["biaya"] for r in KAMPANYE), 2)),
    12: ("bersihkan_nama", ("  RINA  kartika ",), "Rina Kartika"),
}


def samakan(a, b, jalur=""):
    """Bandingkan dua nilai dengan toleransi angka 4 desimal. -> (bool, pesan)"""
    if isinstance(a, float) or isinstance(b, float):
        try:
            if abs(float(a) - float(b)) < 1e-4:
                return True, ""
            return False, "%s: %s vs kunci %s" % (jalur or "nilai", a, b)
        except (TypeError, ValueError):
            return False, "%s: tipe beda (%s vs %s)" % (jalur or "nilai", type(a).__name__, type(b).__name__)
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            hilang = set(b) - set(a)
            return False, "%s: kunci tidak cocok (kurang %s)" % (jalur or "dict", sorted(hilang)[:3])
        for k in b:
            ok, p = samakan(a[k], b[k], "%s.%s" % (jalur or "dict", k))
            if not ok:
                return False, p
        return True, ""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False, "%s: panjang beda (%d vs %d)" % (jalur or "list", len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            ok, p = samakan(x, y, "%s[%d]" % (jalur or "list", i))
            if not ok:
                return False, p
        return True, ""
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        return False, "%s: tipe beda (%s vs %s)" % (jalur or "nilai", type(a).__name__, type(b).__name__)
    if a == b:
        return True, ""
    return False, "%s: %r vs kunci %r" % (jalur or "nilai", a, b)


def main():
    path = os.path.join(BASE, "jawaban.py")
    spec = importlib.util.spec_from_file_location("jawaban", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        print("GAGAL memuat jawaban.py:\n" + traceback.format_exc())
        return 1

    benar = 0
    total = len(KUNCI)
    print("Penilai jawaban Python level 1 — %d soal\n" % total)
    for no in sorted(KUNCI):
        nama, args, kunci = KUNCI[no]
        fn = getattr(mod, nama, None)
        if fn is None:
            print("%2d. SALAH    fungsi %s() tidak ada" % (no, nama))
            continue
        try:
            hasil = fn(*args)
        except NotImplementedError:
            print("%2d. KOSONG   %s() belum diisi" % (no, nama))
            continue
        except Exception as e:
            print("%2d. SALAH    %s() error: %s" % (no, nama, str(e)[:80]))
            continue
        # soal 1 diperiksa per baris pertama saja
        if no == 1:
            hasil = hasil[0] if isinstance(hasil, list) and hasil else hasil
        ok, pesan = samakan(hasil, kunci)
        if ok:
            benar += 1
            print("%2d. BENAR    %s()" % (no, nama))
        else:
            print("%2d. SALAH    %s(): %s" % (no, nama, pesan[:110]))
    print("\nSKOR: %d / %d benar" % (benar, total))
    if benar == total:
        print("STATUS: LULUS SEMPURNA - lanjut ke python/level-2 (pandas)")
    elif benar >= total - 2:
        print("STATUS: LULUS BERSYARAT - perbaiki yang SALAH")
    else:
        print("STATUS: BELUM LULUS - ulangi soal yang SALAH")
    return 0 if benar == total else 1


if __name__ == "__main__":
    sys.exit(main())
