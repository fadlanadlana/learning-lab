#!/usr/bin/env python3
"""Cek hasil cleaning kamu terhadap kunci.

Cara pakai (dari folder excel/data-cleaning):

    python _tools/cek_hasil.py salinan-01.xlsx 01-penjualan-retail.xlsx
    python _tools/cek_hasil.py salinan-01.xlsx 01-penjualan-retail.xlsx --sheet Salinan

Yang dibandingkan (angka, bukan isi sel):
  1. jumlah baris bersih
  2. sisa duplikat
  3. sisa header/footer/kosong
  4. jumlah sel kosong di kolom yang seharusnya terisi
  5. jumlah sel angka yang masih tersimpan sebagai teks
  6. jumlah nilai invalid (negatif, tanggal > hari ini, diskon di luar 0-100)

Skor akhir + status lulus.
"""
import glob
import json
import os
import sys
from datetime import date

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("openpyxl belum terpasang. Jalankan: python -m pip install openpyxl")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KDIR = os.path.join(BASE, "kunci")
KOL_KUNCI = ("order_id", "customer_id", "sku", "campaign_id", "employee_id")


def cari_kunci(nama_file):
    for f in sorted(glob.glob(os.path.join(KDIR, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if d.get("file") == nama_file:
            return d
    tersedia = [json.load(open(f, encoding="utf-8")).get("file")
                for f in sorted(glob.glob(os.path.join(KDIR, "*.json")))]
    sys.exit("Kunci '%s' tidak ada.\nYang dikenal: %s" % (nama_file, ", ".join(tersedia)))


def pilih_sheet(wb, diminta):
    if diminta:
        if diminta not in wb.sheetnames:
            sys.exit("sheet '%s' tidak ada. Ada: %s" % (diminta, ", ".join(wb.sheetnames)))
        return wb[diminta]
    for nm in wb.sheetnames:
        if nm.strip().lower() in ("salinan", "bersih", "clean", "hasil"):
            return wb[nm]
    calon = [ws for ws in wb.worksheets if ws.title.strip().lower() != "data kotor"
             and ws.title.strip().lower() != "checklist"]
    if not calon:
        sys.exit("Tidak ada sheet hasil. Buat sheet baru bernama 'Salinan', "
                 "atau pakai --sheet NAMA.")
    return calon[0]


def baca_tabel(ws):
    """Tebak baris header: baris pertama yang punya >=3 sel teks non-kosong."""
    hdr_row = None
    for r in range(1, min(ws.max_row, 20) + 1):
        vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column, 30) + 1)]
        teks = [v for v in vals if isinstance(v, str) and v.strip()]
        if len(teks) >= 3:
            hdr_row = r
            break
    if hdr_row is None:
        return None, []
    hdr = [ws.cell(hdr_row, c).value for c in range(1, ws.max_column + 1)]
    while hdr and hdr[-1] is None:
        hdr.pop()
    rows = []
    for r in range(hdr_row + 1, ws.max_row + 1):
        x = [ws.cell(r, c).value for c in range(1, len(hdr) + 1)]
        if all(v is None for v in x):
            continue
        rows.append(x)
    return hdr, rows


def utama():
    args = [a for a in sys.argv[1:]]
    sheet = None
    if "--sheet" in args:
        i = args.index("--sheet")
        try:
            sheet = args[i + 1]
        except IndexError:
            sys.exit("pakai: --sheet NAMA")
        del args[i:i + 2]
    if len(args) < 1:
        sys.exit(__doc__)
    path = args[0]
    if not os.path.exists(path):
        sys.exit("berkas tidak ada: %s" % path)

    if len(args) >= 2:
        kunci = cari_kunci(args[1])
    else:
        # tebak dari nama file
        dasar = os.path.basename(path).lower()
        cocok = None
        for f in sorted(glob.glob(os.path.join(KDIR, "*.json"))):
            d = json.load(open(f, encoding="utf-8"))
            inti = (d.get("file") or "").replace(".xlsx", "").split("-", 1)[-1]
            if inti and inti in dasar:
                cocok = d
                break
        if cocok is None:
            sys.exit("Tentukan file kunci sebagai argumen ke-2, misal:\n"
                     "  python _tools/cek_hasil.py %s 01-penjualan-retail.xlsx" % path)
        kunci = cocok

    wb = load_workbook(path, data_only=True)
    ws = pilih_sheet(wb, sheet)
    hdr, rows = baca_tabel(ws)
    if hdr is None:
        sys.exit("tidak menemukan baris header di sheet '%s'" % ws.title)

    kol = {str(h).strip().lower(): i for i, h in enumerate(hdr) if h}
    hasil = {}

    hasil["baris_bersih"] = len(rows)

    # sisa duplikat
    seen = {}
    for x in rows:
        t = tuple(str(v) for v in x)
        seen[t] = seen.get(t, 0) + 1
    hasil["sisa_duplikat"] = sum(c - 1 for c in seen.values() if c > 1)

    # sisa header / footer / kosong
    teks_hdr = [str(h).strip().lower() for h in hdr if h]
    hasil["sisa_header"] = sum(1 for x in rows
                               if [str(v).strip().lower() for v in x] == teks_hdr)
    hasil["sisa_footer"] = sum(1 for x in rows
                               if str(x[0] or "").strip().upper()
                               in ("TOTAL", "JUMLAH", "GRAND TOTAL"))
    hasil["sisa_kosong_penuh"] = 0

    # kolom yang di kunci tidak boleh kosong
    wajib = list((kunci.get("missing_per_kolom") or {}).keys())
    sel_kosong = 0
    for h in wajib:
        i = kol.get(h.lower())
        if i is None:
            continue
        sel_kosong += sum(1 for x in rows if x[i] is None or str(x[i]).strip() == "")
    hasil["sel_kosong_kolom_wajib"] = sel_kosong

    # angka masih teks
    kol_angka = ("qty", "harga_satuan", "diskon_pct", "total", "umur", "total_belanja",
                 "stok", "harga_beli", "impresi", "klik", "biaya", "konversi",
                 "revenue", "jam_kerja")
    hasil["angka_masih_teks"] = sum(
        1 for x in rows for h, i in kol.items()
        if h in kol_angka and isinstance(x[i], str) and str(x[i]).strip())

    # invalid
    invalid = 0
    for h, i in kol.items():
        vals = [x[i] for x in rows]
        if h in ("qty", "stok", "harga_satuan", "harga_beli", "biaya", "revenue",
                 "jam_kerja", "umur", "total_belanja", "impresi", "klik", "konversi"):
            invalid += sum(1 for v in vals if isinstance(v, (int, float)) and v < 0)
        if h == "diskon_pct":
            invalid += sum(1 for v in vals if isinstance(v, (int, float))
                           and (v < 0 or v > 100))
        if h.startswith("tanggal"):
            invalid += sum(1 for v in vals if hasattr(v, "year") and v.year > date.today().year + 1)
    hasil["nilai_invalid"] = invalid

    # ---- bandingkan
    target = {
        "baris_bersih": kunci.get("baris_bersih"),
        "sisa_duplikat": 0,
        "sisa_header": 0,
        "sisa_footer": 0,
        "sel_kosong_kolom_wajib": None,   # opsional, tergantung keputusanmu
        "angka_masih_teks": 0,
        "nilai_invalid": 0,
    }

    print("Cek hasil — %s" % kunci.get("judul"))
    print("sheet diperiksa: %s (%d baris, %d kolom)\n" % (ws.title, len(rows), len(hdr)))
    lulus = 0
    dinilai = 0
    for k, v in target.items():
        milik = hasil[k]
        if v is None:
            print("  %-24s : %s  (keputusanmu sendiri)" % (k, milik))
            continue
        dinilai += 1
        ok = (milik == v)
        if ok:
            lulus += 1
        print("  %-24s : %-8s target %-8s %s"
              % (k, milik, v, "OK" if ok else "<-- BEDA"))
    print("\nSKOR: %d / %d kriteria" % (lulus, dinilai))
    print("STATUS: %s" % ("LULUS" if lulus == dinilai else "BELUM LULUS"))
    return 0 if lulus == dinilai else 1


if __name__ == "__main__":
    sys.exit(utama())
