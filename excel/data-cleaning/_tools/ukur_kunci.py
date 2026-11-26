"""Hitung ulang kunci dari file yang sudah jadi — angka TERUKUR, bukan estimasi.

Dipakai sekali setelah gen_dirty_data.py. Menulis ulang kunci/*.json supaya
angka rekonsiliasi bisa dibuktikan persis.
"""
import glob
import json
import os

import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KDIR = os.path.join(BASE, "kunci")

KOL_ANGKA = ("qty", "harga_satuan", "diskon_pct", "total", "umur", "total_belanja",
             "stok", "harga_beli", "impresi", "klik", "biaya", "konversi",
             "revenue", "jam_kerja")
KOL_TANGGAL = ("tanggal", "tanggal_daftar", "tanggal_update")


def hitung(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Data Kotor"]
    hdr = [ws.cell(3, c).value for c in range(1, ws.max_column + 1)]
    rows = [[ws.cell(r, c).value for c in range(1, len(hdr) + 1)]
            for r in range(4, ws.max_row + 1)]

    hasil = {}
    hasil["baris_terbaca"] = len(rows)
    hasil["header_duplikat"] = sum(1 for x in rows if x == hdr)
    hasil["baris_kosong"] = sum(1 for x in rows if all(v is None for v in x))
    hasil["baris_footer"] = sum(
        1 for x in rows
        if str(x[0] or "").strip().upper() in ("TOTAL", "JUMLAH", "GRAND TOTAL"))

    # duplikat baris utuh: hitung kemunculan > 1, jumlahkan kelebihannya
    seen = {}
    for x in rows:
        t = tuple(str(v) for v in x)
        seen[t] = seen.get(t, 0) + 1
    hasil["duplikat"] = sum(c - 1 for c in seen.values() if c > 1)

    # missing per kolom (hanya baris yang benar-benar data)
    data = [x for x in rows
            if not all(v is None for v in x)
            and x != hdr
            and str(x[0] or "").strip().upper() not in ("TOTAL", "JUMLAH", "GRAND TOTAL")]
    hasil["missing_per_kolom"] = {}
    for i, h in enumerate(hdr):
        n = sum(1 for x in data if x[i] is None)
        if n:
            hasil["missing_per_kolom"][h] = n
    hasil["baris_kena_missing"] = sum(
        1 for x in data if any(x[i] is None for i, h in enumerate(hdr)
                               if h in hasil["missing_per_kolom"]))

    # angka tersimpan sebagai teks
    hasil["sel_angka_jadi_teks"] = sum(
        1 for x in data for h in hdr
        if h in KOL_ANGKA and isinstance(x[hdr.index(h)], str) and str(x[hdr.index(h)]).strip())

    # tanggal campur format (string di kolom tanggal)
    hasil["tanggal_jadi_teks"] = sum(
        1 for x in data for h in hdr
        if h in KOL_TANGGAL and isinstance(x[hdr.index(h)], str) and str(x[hdr.index(h)]).strip())

    # variasi teks pada kolom kategori
    hasil["variasi_teks"] = {}
    for h in hdr:
        if h in KOL_ANGKA or h in KOL_TANGGAL or h in ("order_id", "customer_id", "sku",
                                                       "campaign_id", "employee_id",
                                                       "nama", "pelanggan", "email",
                                                       "telepon", "produk", "nama_produk"):
            continue
        vals = [str(x[hdr.index(h)]).strip() for x in data if x[hdr.index(h)] is not None]
        unik = set(vals)
        if len(unik) > 1:
            hasil["variasi_teks"][h] = {"nilai_berbeda": len(unik),
                                        "contoh": sorted(unik)[:8]}

    # rekonsiliasi
    hasil["baris_bersih"] = (hasil["baris_terbaca"] - hasil["header_duplikat"]
                             - hasil["baris_kosong"] - hasil["baris_footer"]
                             - hasil["duplikat"])
    hasil["rekonsiliasi"] = {
        "baris_terbaca": hasil["baris_terbaca"],
        "kurang_header_duplikat": hasil["header_duplikat"],
        "kurang_baris_kosong": hasil["baris_kosong"],
        "kurang_footer": hasil["baris_footer"],
        "kurang_duplikat": hasil["duplikat"],
        "hasil": hasil["baris_bersih"],
    }
    return hasil


def main():
    for path in sorted(glob.glob(os.path.join(BASE, "*.xlsx"))):
        nama = os.path.basename(path)
        kp = os.path.join(KDIR, nama.replace(".xlsx", ".json"))
        k = json.load(open(kp, encoding="utf-8"))
        ukur = hitung(path)
        k.update(ukur)
        json.dump(k, open(kp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, default=str)
        print(f"{nama}")
        print(f"   terbaca {ukur['baris_terbaca']} | header dup {ukur['header_duplikat']} | "
              f"kosong {ukur['baris_kosong']} | footer {ukur['baris_footer']} | "
              f"dup {ukur['duplikat']}  =>  bersih {ukur['baris_bersih']}")
        print(f"   missing/kolom {ukur['missing_per_kolom']}")
        print(f"   angka-as-teks {ukur['sel_angka_jadi_teks']} | tanggal-as-teks {ukur['tanggal_jadi_teks']}")
        print(f"   variasi teks: " + ", ".join(f"{h}={v['nilai_berbeda']}"
                                              for h, v in ukur["variasi_teks"].items()))
        print()


if __name__ == "__main__":
    main()
