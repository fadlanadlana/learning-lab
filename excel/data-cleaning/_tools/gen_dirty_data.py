"""Generator 5 dataset kotor untuk latihan data cleaning di Excel.

Setiap file: sheet "Data Kotor" (ribuan baris) + sheet "Checklist" (6 area).
Kunci jawaban (jumlah masalah) disimpan terpisah di kunci/*.json — tidak ada di workbook.
"""
import json
import os
import random
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

random.seed(20261126)

OUT = r"D:\learning-lab\excel\data-cleaning"
KUNCI = os.path.join(OUT, "kunci")
N = 2500  # baris bersih per dataset

HIJAU = "1F6F4A"
ABU = "F2F2F2"
KUNING = "FFF2CC"


def pct(n, p):
    return max(1, int(round(n * p)))


def pilih(n, p, skip=()):
    kandidat = [i for i in range(n) if i not in set(skip)]
    return random.sample(kandidat, min(len(kandidat), pct(n, p)))


# ---------------------------------------------------------------- styling
def style_data(ws, ncol):
    ws["A1"].font = Font(bold=True, size=13, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor=HIJAU)
    for c in range(1, ncol + 1):
        cell = ws.cell(3, c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="2E5D4B")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = 17
    thin = Side(style="thin", color="BFBFBF")
    for c in range(1, ncol + 1):
        ws.cell(3, c).border = Border(bottom=thin)


def tulis_data(ws, judul, headers, records, dup_header_after, blank_after, footer=None):
    ws.append([judul])
    ws.append([None] * len(headers))
    ws.append(headers)
    for i, rec in enumerate(records):
        ws.append(list(rec))
        if (i + 1) == dup_header_after:
            ws.append(headers)          # header terduplikasi
        if (i + 1) in blank_after:
            ws.append([None] * len(headers))  # baris kosong
    if footer:
        ws.append(footer)
    style_data(ws, len(headers))
    return ws.max_row


# ---------------------------------------------------------------- checklist
def tulis_checklist(ws, judul, konteks, sections, nraw):
    ws["A1"] = "CHECKLIST DATA CLEANING — " + judul
    ws["A1"].font = Font(bold=True, size=14, color=HIJAU)
    ws["A2"] = konteks
    ws["A2"].font = Font(italic=True, size=10)
    ws["A3"] = "Isi kolom Status. Jangan ubah data mentah — kerjakan di sheet baru (Salinan)."
    ws["A3"].font = Font(italic=True, size=9, color="808080")

    hdr = ["No", "Area", "Yang Dicek", "Status", "Catatan / temuan"]
    for c, h in enumerate(hdr, 1):
        cell = ws.cell(5, c, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=HIJAU)
        cell.alignment = Alignment(horizontal="center")
    for col, w in zip("ABCDE", [6, 26, 62, 15, 34]):
        ws.column_dimensions[col].width = w

    r = 6
    no = 0
    area_rows = []
    for area, items in sections:
        ws.cell(r, 1, "")
        a = ws.cell(r, 2, area)
        a.font = Font(bold=True)
        a.fill = PatternFill("solid", fgColor=ABU)
        ws.cell(r, 3, "—").fill = PatternFill("solid", fgColor=ABU)
        for c in range(1, 6):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=ABU)
        r += 1
        for item in items:
            no += 1
            ws.cell(r, 1, no).alignment = Alignment(horizontal="center")
            ws.cell(r, 2, area).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 3, item).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 4, "Belum").alignment = Alignment(horizontal="center")
            ws.cell(r, 3).fill = PatternFill("solid", fgColor=KUNING)
            r += 1
        area_rows.append((area, r))

    last = r - 1
    dv = DataValidation(type="list", formula1='"Belum,OK,Ada masalah,N/A"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(f"D6:D{last}")

    r += 1
    ws.cell(r, 2, "RINGKASAN").font = Font(bold=True, size=11)
    r += 1
    ws.cell(r, 2, "Total item")
    ws.cell(r, 3, no)
    r += 1
    ws.cell(r, 2, "OK")
    ws.cell(r, 3, f'=COUNTIF($D$6:$D${last},"OK")')
    r += 1
    ws.cell(r, 2, "Ada masalah")
    ws.cell(r, 3, f'=COUNTIF($D$6:$D${last},"Ada masalah")')
    r += 1
    ws.cell(r, 2, "Belum dicek")
    ws.cell(r, 3, f'=COUNTIF($D$6:$D${last},"Belum")')

    r += 2
    ws.cell(r, 2, "REKONSILIASI").font = Font(bold=True, size=11)
    ws.cell(r, 3, "Isi angka hasil hitunganmu sendiri").font = Font(italic=True, size=9, color="808080")
    rek = [
        ("(+) Baris terbaca di sheet Data Kotor", f"=COUNTA('Data Kotor'!A4:A{max(nraw, 4)})"),
        ("(-) baris header duplikat + baris kosong + footer", None),
        ("(-) duplikat dibuang", None),
        ("(-) baris invalid / dikarantina", None),
        ("(=) baris bersih hasil akhir", None),
        ("SELISIH (harus 0)", None),
    ]
    start = r + 1
    for i, (label, val) in enumerate(rek):
        ws.cell(start + i, 2, label)
        if val is not None:
            ws.cell(start + i, 3, val)
        ws.cell(start + i, 3).fill = PatternFill("solid", fgColor=KUNING)
    ws.cell(start + 5, 3,
            f'=IF(C{start}-C{start+1}-C{start+2}-C{start+3}-C{start+4}=0,"BALANCE","ADA SELISIH")')
    ws.cell(start + 5, 3).fill = PatternFill("solid", fgColor="D9EAD3")
    ws.cell(start + 5, 4).value = None

    ws.cell(start + 7, 2, "Sumber data: latihan pribadi — learning-lab").font = Font(size=8, color="808080")


# ---------------------------------------------------------------- 1. PENJUALAN RETAIL
def build_penjualan():
    kota_bersih = ["Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Makassar"]
    kanal_bersih = ["Marketplace", "Retail", "Website", "Distributor"]
    produk = ["Kaos Polos", "Kemeja Batik", "Celana Chino", "Jaket Hoodie",
              "Sepatu Sneaker", "Tas Ransel", "Topi Baseball", "Sandal Kulit"]

    recs = []
    for i in range(N):
        tgl = date(2026, 1, 1) + timedelta(days=random.randint(0, 270))
        qty = random.randint(1, 12)
        harga = random.choice([75000, 125000, 185000, 250000, 320000, 450000])
        disk = random.choice([0, 0, 0, 5, 10, 15])
        total = round(qty * harga * (1 - disk / 100))
        recs.append([
            f"ORD-{20260000 + i + 1}",
            tgl,
            f"Pelanggan {i+1}",
            random.choice(kota_bersih),
            random.choice(kanal_bersih),
            random.choice(produk),
            qty, harga, disk, total,
        ])

    k = {"missing": {}, "angka_teks": 0, "teks": 0, "invalid": 0, "duplikat": 0, "struktur": {}}

    # --- Missing Values
    idx = pilih(N, 0.045)
    for i in idx:
        recs[i][3] = None
    k["missing"]["kota"] = len(idx)
    idx = pilih(N, 0.03, skip=set(idx))
    for i in idx:
        recs[i][8] = None
    k["missing"]["diskon_pct"] = len(idx)
    idx = pilih(N, 0.025)
    for i in idx:
        recs[i][9] = None
    k["missing"]["total"] = len(idx)

    # --- Standardise Numbers: angka jadi teks
    idx = pilih(N, 0.08)
    for i in idx:
        recs[i][7] = f"{recs[i][7]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.05)
    for i in idx:
        recs[i][6] = f"{recs[i][6]} pcs"
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        if recs[i][9] is not None:
            recs[i][9] = "Rp " + f"{int(recs[i][9]):,}".replace(",", ".")
    k["angka_teks"] += len(idx)

    # --- Standardise Text
    varian = {
        "Jakarta": ["JAKARTA", "jakarta", " Jakarta", "DKI Jakarta", "Jakarta "],
        "Bandung": ["BANDUNG", "bandung ", "Kota Bandung"],
        "Surabaya": ["SURABAYA", " surabaya", "Sby"],
        "Medan": ["MEDAN", "medan ", "Kota Medan"],
        "Semarang": ["SEMARANG", "semarang", " Smg"],
        "Makassar": ["MAKASSAR", "makassar ", "Ujung Pandang"],
    }
    idx = pilih(N, 0.10)
    for i in idx:
        if recs[i][3] in varian:
            recs[i][3] = random.choice(varian[recs[i][3]])
    k["teks"] += len(idx)
    varian_kanal = {
        "Marketplace": ["MARKETPLACE", "marketplace ", "Market Place", "MP"],
        "Retail": ["RETAIL", "retail", "Ritel", "Retail "],
        "Website": ["WEBSITE", "website ", "Web", "Situs"],
        "Distributor": ["DISTRIBUTOR", "distributor ", "Distribusi"],
    }
    idx = pilih(N, 0.07)
    for i in idx:
        if recs[i][4] in varian_kanal:
            recs[i][4] = random.choice(varian_kanal[recs[i][4]])
    k["teks"] += len(idx)

    # --- Fix Invalid Values
    idx = pilih(N, 0.015)
    for i in idx:
        recs[i][6] = random.choice([-1, -3, 0])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.012)
    for i in idx:
        recs[i][8] = random.choice([120, 150, -10])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.010)
    for i in idx:
        recs[i][1] = date(2099, random.randint(1, 12), random.randint(1, 28))
    k["invalid"] += len(idx)
    idx = pilih(N, 0.008)
    for i in idx:
        recs[i][7] = 0
    k["invalid"] += len(idx)

    # --- Filter Data: duplikat
    dup = []
    for i in pilih(N, 0.022):
        recs.append(list(recs[i]))
        dup.append(i)
    random.shuffle(recs)
    k["duplikat"] = len(dup)

    headers = ["order_id", "tanggal", "pelanggan", "kota", "kanal", "produk",
               "qty", "harga_satuan", "diskon_pct", "total"]
    k["struktur"] = {"dup_header_setelah": 7, "baris_kosong": [410, 1180, 1990], "footer": True}
    k["baris_bersih"] = N
    return "Data Penjualan Retail (kotor)", headers, recs, k, dict(
        dup_header_after=7, blank_after={410, 1180, 1990},
        footer=["TOTAL", None, None, None, None, None, None, None, None, "=SUM(J4:J2500)"])


# ---------------------------------------------------------------- 2. PELANGGAN CRM
def build_pelanggan():
    depan = ["Budi", "Siti", "Andi", "Rina", "Fajar", "Dewi", "Agus", "Putri",
             "Hendra", "Maya", "Rizki", "Nur", "Bayu", "Lestari", "Yusuf", "Intan"]
    belakang = ["Santoso", "Aminah", "Pratama", "Kartika", "Nugroho", "Wijaya",
                "Saputra", "Handayani", "Siregar", "Purnama", "Halim", "Utami"]
    kota = ["Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Yogyakarta", "Makassar"]
    segmen = ["Bronze", "Silver", "Gold", "Platinum"]

    recs = []
    for i in range(N):
        nm = f"{random.choice(depan)} {random.choice(belakang)}"
        recs.append([
            f"CUST-{i+1:05d}",
            nm,
            f"{nm.split()[0].lower()}{i+1}@mail.com",
            f"08{random.randint(100000000, 999999999)}",
            random.choice(kota),
            date(2024, 1, 1) + timedelta(days=random.randint(0, 800)),
            random.choice(segmen),
            random.randint(18, 65),
            random.randint(0, 40) * 250000,
        ])

    k = {"missing": {}, "angka_teks": 0, "teks": 0, "invalid": 0, "duplikat": 0, "struktur": {}}

    idx = pilih(N, 0.05)
    for i in idx:
        recs[i][2] = None
    k["missing"]["email"] = len(idx)
    idx = pilih(N, 0.035, skip=set(idx))
    for i in idx:
        recs[i][3] = None
    k["missing"]["telepon"] = len(idx)
    idx = pilih(N, 0.02)
    for i in idx:
        recs[i][6] = None
    k["missing"]["segmen"] = len(idx)

    idx = pilih(N, 0.07)
    for i in idx:
        recs[i][7] = f"{recs[i][7]} tahun"
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        recs[i][8] = "Rp " + f"{recs[i][8]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)
    # tanggal campur format
    fmt = ["%d/%m/%Y", "%d-%b-%Y", "%Y.%m.%d", "%m/%d/%Y"]
    idx = pilih(N, 0.12)
    for i in idx:
        recs[i][5] = recs[i][5].strftime(fmt[i % 4])
    k["angka_teks"] += len(idx)

    idx = pilih(N, 0.12)
    for i in idx:
        recs[i][1] = random.choice([recs[i][1].upper(), recs[i][1].lower(),
                                    " " + recs[i][1] + " ", recs[i][1] + "  "])
    k["teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        if recs[i][2]:
            recs[i][2] = recs[i][2].upper()
    k["teks"] += len(idx)
    varian_kota = {"Jakarta": ["JAKARTA", "DKI Jakarta", "jakarta "],
                   "Bandung": ["BANDUNG", "Kota Bandung"],
                   "Yogyakarta": ["JOGJA", "YOGYAKARTA", "yogyakarta "],
                   "Surabaya": ["SURABAYA", "Sby"]}
    idx = pilih(N, 0.08)
    for i in idx:
        if recs[i][4] in varian_kota:
            recs[i][4] = random.choice(varian_kota[recs[i][4]])
    k["teks"] += len(idx)
    varian_seg = {"Bronze": ["BRONZE", "bronze ", "Perunggu"],
                  "Gold": ["GOLD", "Gold ", "Emas"],
                  "Silver": ["SILVER", "silver"],
                  "Platinum": ["PLATINUM", "platinum ", "Plat"]}
    idx = pilih(N, 0.05)
    for i in idx:
        if recs[i][6] in varian_seg:
            recs[i][6] = random.choice(varian_seg[recs[i][6]])
    k["teks"] += len(idx)

    idx = pilih(N, 0.015)
    for i in idx:
        recs[i][7] = random.choice([0, -5, 150, 999])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.012)
    for i in idx:
        if recs[i][2]:
            recs[i][2] = recs[i][2].replace("@", "_at_")
    k["invalid"] += len(idx)
    idx = pilih(N, 0.010)
    for i in idx:
        recs[i][3] = f"08{random.randint(1, 999)}"
    k["invalid"] += len(idx)
    idx = pilih(N, 0.008)
    for i in idx:
        recs[i][5] = date(2099, 1, 1)
    k["invalid"] += len(idx)

    dup = []
    for i in pilih(N, 0.020):
        recs.append(list(recs[i]))
        dup.append(i)
    random.shuffle(recs)
    k["duplikat"] = len(dup)

    headers = ["customer_id", "nama", "email", "telepon", "kota", "tanggal_daftar",
               "segmen", "umur", "total_belanja"]
    k["struktur"] = {"dup_header_setelah": 9, "baris_kosong": [520, 1310, 2140], "footer": True}
    k["baris_bersih"] = N
    return "Data Pelanggan CRM (kotor)", headers, recs, k, dict(
        dup_header_after=9, blank_after={520, 1310, 2140},
        footer=["TOTAL", None, None, None, None, None, None, None, "=SUM(I4:I2500)"])


# ---------------------------------------------------------------- 3. INVENTORI
def build_inventori():
    kategori = ["Elektronik", "Pakaian", "Makanan", "Alat Tulis", "Rumah Tangga"]
    gudang = ["Gudang A", "Gudang B", "Gudang C"]
    satuan = ["pcs", "unit", "buah", "box", "lusin"]

    recs = []
    for i in range(N):
        recs.append([
            f"SKU-{i+1:05d}",
            f"Produk {random.choice(['Alpha','Beta','Gamma','Delta'])} {i+1}",
            random.choice(kategori),
            random.randint(0, 500),
            random.choice(satuan),
            random.choice([12500, 25000, 47000, 89000, 150000]),
            random.choice(gudang),
            date(2026, 1, 1) + timedelta(days=random.randint(0, 300)),
        ])

    k = {"missing": {}, "angka_teks": 0, "teks": 0, "invalid": 0, "duplikat": 0, "struktur": {}}

    idx = pilih(N, 0.04)
    for i in idx:
        recs[i][2] = None
    k["missing"]["kategori"] = len(idx)
    idx = pilih(N, 0.03, skip=set(idx))
    for i in idx:
        recs[i][4] = None
    k["missing"]["satuan"] = len(idx)
    idx = pilih(N, 0.025)
    for i in idx:
        recs[i][5] = None
    k["missing"]["harga_beli"] = len(idx)

    idx = pilih(N, 0.08)
    for i in idx:
        recs[i][3] = f"{recs[i][3]} unit"
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        if recs[i][5] is not None:
            recs[i][5] = f"{recs[i][5]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)

    idx = pilih(N, 0.10)
    for i in idx:
        recs[i][4] = random.choice(["PCS", "Pcs", "Unit", "UNIT", "buah "])
    k["teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        recs[i][0] = recs[i][0].lower()
    k["teks"] += len(idx)
    idx = pilih(N, 0.05)
    for i in idx:
        recs[i][1] = " " + recs[i][1] + " "
    k["teks"] += len(idx)
    varian_kat = {"Elektronik": ["ELEKTRONIK", "elektronik", "Electronics"],
                  "Pakaian": ["PAKAIAN", "pakaian ", "Fashion"],
                  "Makanan": ["MAKANAN", "makanan", "Food"],
                  "Rumah Tangga": ["RUMAH TANGGA", "rumah tangga ", "Home Living"]}
    idx = pilih(N, 0.06)
    for i in idx:
        if recs[i][2] in varian_kat:
            recs[i][2] = random.choice(varian_kat[recs[i][2]])
    k["teks"] += len(idx)

    idx = pilih(N, 0.018)
    for i in idx:
        recs[i][3] = random.choice([-5, -20, -1])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.012)
    for i in idx:
        recs[i][5] = random.choice([-15000, 0])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.008)
    for i in idx:
        recs[i][3] = random.choice([999999, 500000])
    k["invalid"] += len(idx)

    dup = []
    for i in pilih(N, 0.020):
        recs.append(list(recs[i]))
        dup.append(i)
    random.shuffle(recs)
    k["duplikat"] = len(dup)

    headers = ["sku", "nama_produk", "kategori", "stok", "satuan", "harga_beli",
               "gudang", "tanggal_update"]
    k["struktur"] = {"dup_header_setelah": 6, "baris_kosong": [380, 1120, 2050], "footer": True}
    k["baris_bersih"] = N
    return "Data Inventori Gudang (kotor)", headers, recs, k, dict(
        dup_header_after=6, blank_after={380, 1120, 2050},
        footer=["TOTAL", None, None, "=SUM(D4:D2500)", None, None, None, None])


# ---------------------------------------------------------------- 4. KAMPANYE MARKETING
def build_kampanye():
    platform = ["Meta", "Google", "TikTok", "LinkedIn"]

    recs = []
    for i in range(N):
        imp = random.randint(2000, 90000)
        klik = int(imp * random.uniform(0.008, 0.06))
        biaya = klik * random.randint(800, 4500)
        konv = int(klik * random.uniform(0.01, 0.09))
        rev = konv * random.randint(150000, 900000)
        recs.append([
            f"CMP-{i+1:05d}",
            date(2026, 1, 1) + timedelta(days=random.randint(0, 280)),
            random.choice(platform),
            imp, klik, biaya, konv, rev,
        ])

    k = {"missing": {}, "angka_teks": 0, "teks": 0, "invalid": 0, "duplikat": 0, "struktur": {}}

    idx = pilih(N, 0.04)
    for i in idx:
        recs[i][2] = None
    k["missing"]["platform"] = len(idx)
    idx = pilih(N, 0.03, skip=set(idx))
    for i in idx:
        recs[i][5] = None
    k["missing"]["biaya"] = len(idx)
    idx = pilih(N, 0.02)
    for i in idx:
        recs[i][4] = None
    k["missing"]["klik"] = len(idx)

    idx = pilih(N, 0.08)
    for i in idx:
        recs[i][3] = f"{recs[i][3]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.07)
    for i in idx:
        if recs[i][5] is not None:
            recs[i][5] = "Rp " + f"{recs[i][5]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.05)
    for i in idx:
        recs[i][7] = f"Rp {recs[i][7]:,}".replace(",", ".")
    k["angka_teks"] += len(idx)
    fmt = ["%d/%m/%Y", "%d-%b-%Y", "%Y.%m.%d"]
    idx = pilih(N, 0.10)
    for i in idx:
        recs[i][1] = recs[i][1].strftime(fmt[i % 3])
    k["angka_teks"] += len(idx)

    varian_p = {"Meta": ["META", "meta ", "Facebook", "FB", "Facebook Ads"],
                "Google": ["GOOGLE", "google ", "Google Ads", "Adwords"],
                "TikTok": ["TIKTOK", "tiktok ", "Tik Tok", "TT"],
                "LinkedIn": ["LINKEDIN", "linkedin ", "Linked In", "LI"]}
    idx = pilih(N, 0.10)
    for i in idx:
        if recs[i][2] in varian_p:
            recs[i][2] = random.choice(varian_p[recs[i][2]])
    k["teks"] += len(idx)
    idx = pilih(N, 0.04)
    for i in idx:
        recs[i][0] = " " + recs[i][0] + " "
    k["teks"] += len(idx)

    idx = pilih(N, 0.015)
    for i in idx:
        if isinstance(recs[i][3], int):
            recs[i][4] = recs[i][3] + random.randint(100, 5000)
    k["invalid"] += len(idx)
    idx = pilih(N, 0.012)
    for i in idx:
        if isinstance(recs[i][4], int):
            recs[i][6] = recs[i][4] + random.randint(1, 100)
    k["invalid"] += len(idx)
    idx = pilih(N, 0.010)
    for i in idx:
        if isinstance(recs[i][7], int):
            recs[i][7] = -abs(recs[i][7])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.008)
    for i in idx:
        recs[i][1] = date(2099, 6, 1)
    k["invalid"] += len(idx)

    dup = []
    for i in pilih(N, 0.022):
        recs.append(list(recs[i]))
        dup.append(i)
    random.shuffle(recs)
    k["duplikat"] = len(dup)

    headers = ["campaign_id", "tanggal", "platform", "impresi", "klik",
               "biaya", "konversi", "revenue"]
    k["struktur"] = {"dup_header_setelah": 8, "baris_kosong": [450, 1250, 2080], "footer": True}
    k["baris_bersih"] = N
    return "Data Kampanye Marketing (kotor)", headers, recs, k, dict(
        dup_header_after=8, blank_after={450, 1250, 2080},
        footer=["TOTAL", None, None, "=SUM(D4:D2500)", "=SUM(E4:E2500)", None, "=SUM(G4:G2500)", "=SUM(H4:H2500)"])


# ---------------------------------------------------------------- 5. KEHADIRAN
def build_kehadiran():
    depan = ["Budi", "Siti", "Andi", "Rina", "Fajar", "Dewi", "Agus", "Putri"]
    belakang = ["Santoso", "Aminah", "Pratama", "Kartika", "Nugroho", "Wijaya"]
    dept = ["IT", "Finance", "HR", "Operations", "Marketing"]
    status = ["Hadir", "Terlambat", "Izin", "Sakit"]

    recs = []
    for i in range(N):
        masuk = random.randint(7, 9)
        keluar = random.randint(16, 19)
        jam = keluar - masuk
        recs.append([
            f"EMP-{random.randint(1, 120):04d}",
            f"{random.choice(depan)} {random.choice(belakang)}",
            random.choice(dept),
            date(2026, 1, 1) + timedelta(days=random.randint(0, 250)),
            f"{masuk:02d}:00", f"{keluar:02d}:00", jam,
            random.choice(status),
        ])

    k = {"missing": {}, "angka_teks": 0, "teks": 0, "invalid": 0, "duplikat": 0, "struktur": {}}

    idx = pilih(N, 0.04)
    for i in idx:
        recs[i][5] = None
    k["missing"]["jam_keluar"] = len(idx)
    idx = pilih(N, 0.03, skip=set(idx))
    for i in idx:
        recs[i][2] = None
    k["missing"]["departemen"] = len(idx)
    idx = pilih(N, 0.025)
    for i in idx:
        recs[i][6] = None
    k["missing"]["jam_kerja"] = len(idx)

    idx = pilih(N, 0.08)
    for i in idx:
        recs[i][6] = f"{recs[i][6]} jam"
    k["angka_teks"] += len(idx)
    fmtw = ["{h}.00", "{h} AM", "{h}:00", "{h}.00 WIB"]
    idx = pilih(N, 0.10)
    for i in idx:
        if recs[i][4]:
            hh = recs[i][4][:2].lstrip("0") or "0"
            recs[i][4] = fmtw[i % 4].format(h=hh)
    k["angka_teks"] += len(idx)
    idx = pilih(N, 0.07)
    for i in idx:
        if recs[i][3] and not isinstance(recs[i][3], str):
            recs[i][3] = recs[i][3].strftime(["%d/%m/%Y", "%d-%b-%Y", "%Y.%m.%d"][i % 3])
    k["angka_teks"] += len(idx)

    varian_d = {"IT": ["it", "IT ", "Information Technology"],
                "Finance": ["FINANCE", "finance ", "Keuangan"],
                "HR": ["hr", "HR ", "Human Resource"],
                "Operations": ["OPERATIONS", "operations", "Operasional"],
                "Marketing": ["MARKETING", "marketing ", "Pemasaran"]}
    idx = pilih(N, 0.09)
    for i in idx:
        if recs[i][2] in varian_d:
            recs[i][2] = random.choice(varian_d[recs[i][2]])
    k["teks"] += len(idx)
    idx = pilih(N, 0.06)
    for i in idx:
        recs[i][1] = random.choice([recs[i][1].upper(), recs[i][1].lower(), " " + recs[i][1]])
    k["teks"] += len(idx)
    varian_s = {"Hadir": ["HADIR", "hadir", "Present"],
                "Terlambat": ["TERLAMBAT", "terlambat ", "Late"],
                "Izin": ["IZIN", "izin", "Permission"],
                "Sakit": ["SAKIT", "sakit ", "Sick"]}
    idx = pilih(N, 0.05)
    for i in idx:
        if recs[i][7] in varian_s:
            recs[i][7] = random.choice(varian_s[recs[i][7]])
    k["teks"] += len(idx)

    idx = pilih(N, 0.015)
    for i in idx:
        recs[i][6] = random.choice([-3, 0, 30])
    k["invalid"] += len(idx)
    idx = pilih(N, 0.012)
    for i in idx:
        recs[i][4], recs[i][5] = "18:00", "08:00"
    k["invalid"] += len(idx)
    idx = pilih(N, 0.008)
    for i in idx:
        recs[i][3] = date(2099, 3, 3)
    k["invalid"] += len(idx)

    # duplikat per karyawan+tanggal
    dup = []
    for i in pilih(N, 0.020):
        recs.append(list(recs[i]))
        dup.append(i)
    random.shuffle(recs)
    k["duplikat"] = len(dup)

    headers = ["employee_id", "nama", "departemen", "tanggal", "jam_masuk",
               "jam_keluar", "jam_kerja", "status"]
    k["struktur"] = {"dup_header_setelah": 5, "baris_kosong": [600, 1400, 2200], "footer": True}
    k["baris_bersih"] = N
    return "Data Kehadiran Karyawan (kotor)", headers, recs, k, dict(
        dup_header_after=5, blank_after={600, 1400, 2200},
        footer=["TOTAL", None, None, None, None, None, "=SUM(G4:G2500)", None])


# ---------------------------------------------------------------- checklist per dataset
def sections_umum(entitas, kolom_wajib, kolom_angka, kolom_teks, aturan_invalid):
    return [
        ("Fix rows and columns", [
            "Ada baris judul di atas nama kolom? Header seharusnya jadi baris pertama.",
            "Ada baris nama kolom yang terduplikasi di tengah data? Hapus.",
            "Ada baris kosong di antara data? Hapus, jangan biarkan memutus range.",
            "Ada baris TOTAL/footer di bawah data? Itu bukan data — hapus dulu.",
            "Nama kolom unik, tanpa spasi berlebih, tanpa karakter tersembunyi?",
            f"Satu baris = satu {entitas}? Tidak ada baris yang hanya berisi sisa/pecahan.",
            f"Tipe kolom benar: {kolom_angka} = angka, tanggal = tanggal (bukan teks).",
            "Range data tidak punya kolom kosong di tengah (kolom hantu).",
        ]),
        ("Missing Values", [
            f"Kolom wajib kosong: {kolom_wajib}. Hitung jumlahnya per kolom.",
            "Sudah hitung persentase kosong tiap kolom sebelum memutuskan tindakan?",
            "Keputusan per kolom sudah ditetapkan: hapus baris / isi default / biarkan berlabel?",
            "Baris yang dihapus karena kosong sudah dicatat jumlahnya?",
            "Kolom opsional yang kosong tidak dianggap error (jangan hapus berlebihan).",
        ]),
        ("Standardise Numbers", [
            f"Angka tersimpan sebagai teks di {kolom_angka}? (contoh: \"1.500.000\", \"3 pcs\")",
            "Pemisah ribuan dan desimal konsisten (jangan campur titik dan koma)?",
            "Simbol mata uang (Rp) menempel di angka? Pisahkan ke kolom/format saja.",
            "Satuan menempel di nilai angka? Pisahkan jadi kolom satuan.",
            "Persen disimpan sebagai teks (\"15%\") bukan angka 0,15?",
            "Konversi teks -> angka dilakukan dengan VALUE / Paste Special Multiply.",
        ]),
        ("Standardise Text", [
            "Ada spasi berlebih di awal/akhir nilai? TRIM.",
            "Kapitalisasi tidak konsisten (JAKARTA / jakarta / Jakarta)? PROPER/UPPER.",
            f"Variasi penulisan pada {kolom_teks} (singkatan, nama lain, salah ketik)?",
            "Ada karakter tak terlihat (non-breaking space, tab) selain spasi biasa?",
            "Nilai kategori sudah cocok persis dengan daftar acuan (bukan mirip)?",
            "Singkatan vs kepanjangan sudah dipilih satu bentuk baku?",
        ]),
        ("Fix Invalid Values", [
            "Ada nilai negatif di kolom yang seharusnya tidak boleh negatif?",
            "Ada tanggal di masa depan (mis. 2099) atau tanggal mustahil?",
            "Ada angka 0 pada kolom yang secara bisnis tidak boleh 0?",
            aturan_invalid,
            "Ada outlier ekstrem (jauh di luar wajar)? Sudah diperiksa bukan salah input?",
            "Nilai invalid: diperbaiki, dikarantina, atau dihapus? Sudah diputuskan?",
        ]),
        ("Filter Data", [
            "Duplikat baris utuh (semua kolom sama) sudah dihapus?",
            f"Duplikat berdasarkan kunci unik {entitas} sudah diperiksa?",
            "Baris uji / dummy / contoh sudah dibuang?",
            "Filter sudah diterapkan sebelum menghitung, bukan setelah?",
            "Rekonsiliasi: baris awal - dibuang = baris bersih. Selisih harus 0.",
            "Hasil bersih disimpan di sheet BARU, data mentah tetap utuh.",
        ]),
    ]


# ---------------------------------------------------------------- main
def buat_file(nomor, nama_file, hasil):
    judul, headers, recs, k, opt = hasil
    wb = Workbook()
    ws = wb.active
    ws.title = "Data Kotor"
    nraw = tulis_data(ws, judul, headers, recs,
                      opt["dup_header_after"], opt["blank_after"], opt["footer"])
    ws.freeze_panes = None

    entitas = {"order_id": "transaksi", "customer_id": "pelanggan",
               "sku": "baris stok", "campaign_id": "kampanye",
               "employee_id": "kehadiran"}[headers[0]]
    kol_wajib = ", ".join(k["missing"].keys()) or "-"
    kol_angka = ", ".join([h for h in headers if h in
                           ("qty", "harga_satuan", "diskon_pct", "total", "umur",
                            "total_belanja", "stok", "harga_beli", "impresi", "klik",
                            "biaya", "konversi", "revenue", "jam_kerja")])
    kol_teks = ", ".join([h for h in headers if h in
                          ("kota", "kanal", "segmen", "kategori", "satuan", "platform",
                           "departemen", "status")])
    aturan = {
        "order_id": "Diskon di luar 0-100% atau qty negatif = invalid.",
        "customer_id": "Umur di luar 17-100, email tanpa @, telepon < 10 digit = invalid.",
        "sku": "Stok atau harga beli negatif = invalid.",
        "campaign_id": "Klik > impresi, atau konversi > klik = mustahil.",
        "employee_id": "Jam keluar < jam masuk, atau jam kerja > 24 = invalid.",
    }[headers[0]]

    wsc = wb.create_sheet("Checklist")
    tulis_checklist(wsc,
                    judul.replace(" (kotor)", ""),
                    f"Target: {N} baris bersih. Sheet 'Data Kotor' sengaja berisi 6 jenis masalah "
                    f"(struktur, missing, angka, teks, invalid, duplikat).",
                    sections_umum(entitas, kol_wajib, kol_angka, kol_teks, aturan),
                    nraw)

    path = os.path.join(OUT, nama_file)
    wb.save(path)

    k["file"] = nama_file
    k["judul"] = judul
    k["baris_data_mentah_di_file"] = nraw
    k["kolom"] = headers
    with open(os.path.join(KUNCI, nama_file.replace(".xlsx", ".json")), "w", encoding="utf-8") as f:
        json.dump(k, f, ensure_ascii=False, indent=2, default=str)
    return path, nraw, k


def main():
    os.makedirs(KUNCI, exist_ok=True)
    jobs = [
        ("01-penjualan-retail.xlsx", build_penjualan()),
        ("02-pelanggan-crm.xlsx", build_pelanggan()),
        ("03-inventori-gudang.xlsx", build_inventori()),
        ("04-kampanye-marketing.xlsx", build_kampanye()),
        ("05-kehadiran-karyawan.xlsx", build_kehadiran()),
    ]
    print(f"{'FILE':<32} {'BARIS':>7} {'MISSING':>8} {'ANGKA/TEKS':>11} {'TEKS':>6} {'INVALID':>8} {'DUP':>5}")
    print("-" * 84)
    for nama, hasil in jobs:
        p, nraw, k = buat_file(0, nama, hasil)
        miss = sum(k["missing"].values())
        print(f"{nama:<32} {nraw:>7} {miss:>8} {k['angka_teks']:>11} "
              f"{k['teks']:>6} {k['invalid']:>8} {k['duplikat']:>5}")
        print(f"   -> {os.path.getsize(p)/1024:.0f} KB")


if __name__ == "__main__":
    main()
