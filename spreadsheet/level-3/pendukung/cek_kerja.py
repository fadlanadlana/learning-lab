#!/usr/bin/env python3
"""Penilai otomatis latihan spreadsheet level 3.

Cara pakai (dari folder spreadsheet/level-3):

    python3 pendukung/cek_kerja.py latihan/level-3-dashboard-penjualan-pivot.xlsx
    python3 pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx
    python3 pendukung/cek_kerja.py latihan/level-3-pembersihan-data.xlsx --detail 5

Yang dibaca:
  1. Blok jawaban di sheet 4_Kerja: kolom A = nomor soal, B = kunci baris, C = jawabanmu.
     Blok dicari otomatis dari header "SOAL ... KUNCI BARIS ... JAWABAN".
  2. Khusus workbook pembersihan: tabel bernama DataBersih (atau sheet bernama DataBersih)
     dengan kolom id_transaksi, kota_bersih, nilai.

Nilai di kolom C harus berupa ANGKA/nilai jadi, bukan formula yang belum dihitung.
Kalau kamu memakai formula, salin hasilnya sebagai nilai (Paste Special > Values).
"""
import glob
import json
import os
import re
import sys

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("openpyxl belum terpasang. Jalankan: pip install openpyxl")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # spreadsheet/level-3
KUNCI_DIR = os.path.join(BASE, "pendukung", "kunci")
TOLERANSI = 0.00005


def cari_kunci(path_workbook):
    nama = os.path.basename(path_workbook)
    for f in sorted(glob.glob(os.path.join(KUNCI_DIR, "*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        if data.get("file") == nama:
            return data, f
    tersedia = [json.load(open(f, encoding="utf-8")).get("file") for f in
                sorted(glob.glob(os.path.join(KUNCI_DIR, "*.json")))]
    sys.exit("Kunci untuk '%s' tidak ada.\nBerkas yang dikenal: %s" % (nama, ", ".join(tersedia)))


def ke_angka(v):
    """Terima angka atau teks '1.234.567' / '1234567,5'."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("Rp", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def sama(a, b, tipe):
    if tipe == "teks":
        return str(a).strip().lower() == str(b).strip().lower()
    x, y = ke_angka(a), ke_angka(b)
    if x is None or y is None:
        return False
    return abs(x - y) <= max(TOLERANSI, abs(y) * 1e-9)


def baca_blok(ws):
    """Cari header blok jawaban, kembalikan dict {(soal, kunci): nilai} dan info baris."""
    header_row = None
    for r in range(1, min(ws.max_row, 60) + 1):
        a = str(ws.cell(row=r, column=1).value or "").strip().upper()
        c = str(ws.cell(row=r, column=3).value or "").strip().upper()
        b = str(ws.cell(row=r, column=2).value or "").strip().upper()
        if a == "SOAL" and b == "KUNCI BARIS" and "JAWABAN" in c:
            header_row = r
            break
    if header_row is None:
        return None
    hasil = {}
    for r in range(header_row + 1, ws.max_row + 1):
        a = ws.cell(row=r, column=1).value
        b = ws.cell(row=r, column=2).value
        if a is None and b is None:
            continue
        try:
            soal = int(str(a).strip())
        except (TypeError, ValueError):
            continue
        kunci = str(b or "").strip()
        hasil[(soal, kunci)] = ws.cell(row=r, column=3).value
    return hasil


def cari_tabel_bersih(wb):
    """Kembalikan (judul_sheet, header, rows) dari tabel DataBersih."""
    from openpyxl.utils import range_boundaries
    for ws in wb.worksheets:
        for nama, ref in getattr(ws, "tables", {}).items():
            if str(nama).strip().lower() != "databersih":
                continue
            c0, r0, c1, r1 = range_boundaries(str(ref))
            if c0 is None or r0 is None or c1 is None or r1 is None:
                continue
            min_col, min_row, max_col, max_row = int(c0), int(r0), int(c1), int(r1)
            header = [ws.cell(row=min_row, column=c).value for c in range(min_col, max_col + 1)]
            rows = [[ws.cell(row=r, column=c).value for c in range(min_col, max_col + 1)]
                    for r in range(min_row + 1, max_row + 1)]
            return ws.title + " (tabel %s, %s)" % (nama, ref), header, rows
    for ws in wb.worksheets:
        if ws.title.strip().lower() == "databersih":
            header = [c.value for c in ws[1]]
            rows = [[c.value for c in row] for row in ws.iter_rows(min_row=2) if any(c.value is not None for c in row)]
            return ws.title + " (sheet)", header, rows
    return None, None, None


def bandingkan_bersih(header, rows, kunci_bersih):
    kolom = {str(h).strip().lower(): i for i, h in enumerate(header) if h is not None}
    butuh = ["id_transaksi", "kota_bersih", "nilai"]
    kurang = [k for k in butuh if k not in kolom]
    if kurang:
        return False, "kolom wajib tidak ada: %s (ada: %s)" % (kurang, list(kolom))
    dapat = []
    for r in rows:
        if r is None or all(v is None for v in r):
            continue
        ident = str(r[kolom["id_transaksi"]]).strip()
        kota = str(r[kolom["kota_bersih"]]).strip()
        nilai = ke_angka(r[kolom["nilai"]])
        dapat.append((ident, kota, nilai))
    harap = [(str(a), str(b), float(c)) for a, b, c in kunci_bersih]
    if len(dapat) != len(harap):
        return False, "jumlah baris beda: punyamu %d, seharusnya %d" % (len(dapat), len(harap))
    set_dapat = {(a, b, None if c is None else round(c, 2)) for a, b, c in dapat}
    set_harap = {(a, b, round(c, 2)) for a, b, c in harap}
    if set_dapat == set_harap:
        return True, ""
    beda = sorted(set_harap - set_dapat)[:3]
    lebih = sorted(set_dapat - set_harap)[:3]
    return False, "isi beda. contoh seharusnya %s | punyamu %s" % (beda, lebih)


def main():
    arg = [a for a in sys.argv[1:]]
    detail_no = None
    if "--detail" in arg:
        i = arg.index("--detail")
        try:
            detail_no = int(arg[i + 1])
        except (IndexError, ValueError):
            sys.exit("pakai: --detail NOMOR")
        del arg[i:i + 2]
    if not arg:
        sys.exit(__doc__)
    path = arg[0]
    if not os.path.exists(path):
        sys.exit("berkas tidak ada: %s" % path)

    kunci, _ = cari_kunci(path)
    wb = load_workbook(path, data_only=True)
    if "4_Kerja" not in wb.sheetnames:
        sys.exit("sheet 4_Kerja tidak ada. Sheet yang ada: %s" % ", ".join(wb.sheetnames))
    blok = baca_blok(wb["4_Kerja"])
    if blok is None:
        sys.exit("blok jawaban tidak ditemukan di 4_Kerja (butuh header SOAL | KUNCI BARIS | JAWABAN).")

    soal_list = kunci["soal"]
    hasil = {}
    for s in soal_list:
        status = True
        pesan = []
        for b in s["baris"]:
            v = blok.get((s["no"], b["kunci"]))
            if v is None or (isinstance(v, str) and not v.strip()):
                status = False
                pesan.append("%s: belum diisi" % b["kunci"])
                continue
            if not sama(v, b["nilai"], "teks" if isinstance(b["nilai"], str) else "angka"):
                status = False
                pesan.append("%s: punyamu %r, seharusnya %r" % (b["kunci"], v, b["nilai"]))
        hasil[s["no"]] = (status, pesan)

    print("Penilai %s - %d soal\n" % (kunci["judul"], len(soal_list)))
    benar = 0
    for s in soal_list:
        status, pesan = hasil[s["no"]]
        if status:
            benar += 1
            print("%2d. BENAR" % s["no"])
        else:
            print("%2d. SALAH    %s" % (s["no"], "; ".join(pesan[:2])))
        if detail_no == s["no"]:
            print("\n    soal   : %s" % s["teks"])
            for b in s["baris"]:
                print("    %-26s kamu=%-14r kunci=%r" % (b["kunci"], blok.get((s["no"], b["kunci"])),
                                                         b["nilai"]))
            print()

    # ---- khusus workbook pembersihan data
    if kunci.get("bersih"):
        judul, header, rows = cari_tabel_bersih(wb)
        if judul is None:
            print("\nDATA BERSIH: tidak ditemukan tabel/sheet bernama DataBersih")
            ok_bersih = False
        else:
            ok, pesan = bandingkan_bersih(header, rows or [], kunci["bersih"])
            ok_bersih = ok
            print("\nDATA BERSIH: %s (%s, %d baris)" % ("BENAR" if ok else "SALAH", judul,
                                                       len(rows or [])))
            if not ok:
                print("   %s" % pesan)
    else:
        ok_bersih = True

    total = len(soal_list)
    print("\nSKOR: %d / %d soal benar" % (benar, total))
    if kunci.get("bersih"):
        print("TABEL BERSIH: %s" % ("BENAR" if ok_bersih else "SALAH"))
    if benar == total and ok_bersih:
        print("STATUS: LULUS SEMPURNA")
    elif benar >= total - 2 and ok_bersih:
        print("STATUS: LULUS BERSYARAT - perbaiki yang SALAH")
    else:
        print("STATUS: BELUM LULUS - ulangi soal yang SALAH")
    return 0 if (benar == total and ok_bersih) else 1


if __name__ == "__main__":
    sys.exit(main())
