#!/usr/bin/env python3
"""Generator latihan spreadsheet level 3 (format baru).

Menghasilkan 2 workbook:
  latihan/level-3-dashboard-penjualan-pivot.xlsx   (fokus PivotTable, 240 baris data)
  latihan/level-3-pembersihan-data.xlsx            (fokus Power Query, 120 baris data kotor)
Tiap workbook: 1_Masalah, 2_Data, 3_Soal, 4_Kerja (blok jawaban), 5_Kunci.
Kunci mesin: pendukung/kunci/<nama>.json
"""
import json
import os
import random
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # spreadsheet/level-3
LATIHAN = os.path.join(OUT, "latihan")
PENDUKUNG = os.path.join(OUT, "pendukung")
KUNCI_DIR = os.path.join(PENDUKUNG, "kunci")

JUDUL_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FILL = PatternFill("solid", fgColor="D9E2F3")
KERJA_FILL = PatternFill("solid", fgColor="FFF2CC")
KUNCI_FILL = PatternFill("solid", fgColor="E2EFDA")
JUDUL_FONT = Font(bold=True, color="FFFFFF", size=12)
BOLD = Font(bold=True)
TEBAL = Side(style="thin", color="8EA9DB")
KOTAK = Border(left=TEBAL, right=TEBAL, top=TEBAL, bottom=TEBAL)


def atur_lebar(ws, lebar):
    for i, w in enumerate(lebar, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def judul_sheet(ws, teks, kolom=8):
    ws["A1"] = teks
    ws["A1"].font = JUDUL_FONT
    ws["A1"].fill = JUDUL_FILL
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=kolom)
    ws.row_dimensions[1].height = 24


def tulis_baris(ws, mulai, baris, bold=False, fill=None):
    for j, v in enumerate(baris, start=1):
        c = ws.cell(row=mulai, column=j, value=v)
        if bold:
            c.font = BOLD
        if fill:
            c.fill = fill
        c.border = KOTAK
        c.alignment = Alignment(vertical="top", wrap_text=True)


# ===================================================================== DATA A
REGION = ["Jawa Barat", "Jawa Timur", "Jabodetabek", "Sumatera", "Bali"]
KANAL = ["Marketplace", "Retail", "Distributor", "Website"]
PRODUK = [("PR-01 Kemeja Formal", 285000), ("PR-02 Kaos Polos", 95000),
          ("PR-03 Jaket Bomber", 420000), ("PR-04 Celana Chino", 245000),
          ("PR-05 Sepatu Sneaker", 520000), ("PR-06 Tas Kanvas", 195000)]
DISKON = [0.0, 0.0, 0.05, 0.10, 0.15, 0.20]
TARGET_REGION = {"Jawa Barat": 95000000, "Jawa Timur": 90000000,
                 "Jabodetabek": 120000000, "Sumatera": 60000000, "Bali": 45000000}


def buat_data_penjualan(n=240, seed=7):
    rnd = random.Random(seed)
    bulan_awal = {"2026-08": date(2026, 8, 1), "2026-09": date(2026, 9, 1),
                  "2026-10": date(2026, 10, 1)}
    baris = []
    for i in range(1, n + 1):
        bulan = ["2026-08", "2026-09", "2026-10"][rnd.randrange(3)]
        tgl = bulan_awal[bulan] + timedelta(days=rnd.randrange(27))
        region = rnd.choice(REGION)
        kanal = rnd.choice(KANAL)
        nama, harga = rnd.choice(PRODUK)
        qty = rnd.randint(1, 30)
        diskon = rnd.choice(DISKON)
        revenue = round(qty * harga * (1 - diskon))
        baris.append([i, tgl.isoformat(), bulan, region, kanal, nama, qty, harga, diskon, revenue])
    return baris


HEADER_A = ["id", "tanggal", "bulan", "region", "kanal", "produk", "qty", "harga", "diskon", "revenue"]


def kunci_a(data):
    from collections import Counter
    total_revenue = sum(r[9] for r in data)
    total_qty = sum(r[6] for r in data)
    per_region = Counter()
    per_bulan = Counter()
    per_kanal = Counter()
    per_produk = Counter()
    for r in data:
        per_region[r[3]] += r[9]
        per_bulan[r[2]] += r[9]
        per_kanal[r[4]] += r[9]
        per_produk[r[5]] += r[9]
    kombinasi = len({(r[3], r[4]) for r in data})
    diskon_mkt = [r[8] for r in data if r[4] == "Marketplace"]
    rata_diskon = sum(diskon_mkt) / len(diskon_mkt)
    growth = (per_bulan["2026-10"] - per_bulan["2026-09"]) / per_bulan["2026-09"] * 100
    region_top = max(per_region, key=per_region.get)
    persen_top = per_region[region_top] / total_revenue * 100
    n_diskon = sum(1 for r in data if r[8] >= 0.1)
    capaian_bali = per_region["Bali"] / TARGET_REGION["Bali"] * 100

    soal = [
        {"no": 1, "teks": "Total revenue seluruh data (240 baris).", "tipe": "angka",
         "baris": [{"kunci": "total_revenue", "nilai": total_revenue}]},
        {"no": 2, "teks": "Total qty seluruh data.", "tipe": "angka",
         "baris": [{"kunci": "total_qty", "nilai": total_qty}]},
        {"no": 3, "teks": "Jumlah baris transaksi.", "tipe": "angka",
         "baris": [{"kunci": "jumlah_transaksi", "nilai": len(data)}]},
        {"no": 4, "teks": "Revenue per region (5 baris, nama region sudah disediakan di blok jawaban).",
         "tipe": "tabel", "baris": [{"kunci": r, "nilai": per_region[r]} for r in REGION]},
        {"no": 5, "teks": "Revenue per bulan (3 baris).", "tipe": "tabel",
         "baris": [{"kunci": b, "nilai": per_bulan[b]} for b in ("2026-08", "2026-09", "2026-10")]},
        {"no": 6, "teks": "Revenue per kanal (4 baris).", "tipe": "tabel",
         "baris": [{"kunci": k, "nilai": per_kanal[k]} for k in KANAL]},
    ]
    soal += [
        {"no": 7, "teks": "Jumlah kombinasi region-kanal yang unik (pasangan berbeda).", "tipe": "angka",
         "baris": [{"kunci": "kombinasi_region_kanal", "nilai": kombinasi}]},
        {"no": 8, "teks": "Nama produk dengan revenue terbesar (tulis persis seperti di data).",
         "tipe": "teks", "baris": [{"kunci": "produk_terlaris",
                                    "nilai": max(per_produk, key=per_produk.get)}]},
        {"no": 9, "teks": "Rata-rata diskon kanal Marketplace dalam bentuk pecahan 4 desimal "
                           "(contoh format: 0,1234), bukan persen.",
         "tipe": "angka", "baris": [{"kunci": "rata_diskon_marketplace", "nilai": round(rata_diskon, 4)}]},
        {"no": 10, "teks": "Pertumbuhan revenue Oktober dibanding September, persen 2 desimal "
                           "(kalau turun, tulis dengan tanda minus).",
         "tipe": "angka", "baris": [{"kunci": "growth_okt_vs_sep", "nilai": round(growth, 2)}]},
        {"no": 11, "teks": "Kontribusi (%) region dengan revenue terbesar terhadap total, 2 desimal.",
         "tipe": "angka", "baris": [{"kunci": "persen_region_teratas", "nilai": round(persen_top, 2)}]},
        {"no": 12, "teks": "Jumlah transaksi dengan diskon minimal 10% (diskon >= 0,10).",
         "tipe": "angka", "baris": [{"kunci": "transaksi_diskon_10", "nilai": n_diskon}]},
        {"no": 13, "teks": "Capaian revenue Bali terhadap target Bali (lihat tabel target di 1_Masalah), "
                           "persen 2 desimal.", "tipe": "angka",
         "baris": [{"kunci": "capaian_target_bali", "nilai": round(capaian_bali, 2)}]},
    ]
    return soal, {"region_top": region_top}


# ===================================================================== DATA B
KOTA_BERSIH = ["Jakarta", "Bandung", "Surabaya", "Medan", "Semarang"]
VARIAN_KOTA = {
    "Jakarta": ["Jakarta", "JAKARTA", " jakarta ", "Jakarta  ", "jakarta"],
    "Bandung": ["Bandung", " bandung", "BANDUNG ", "Bandung", "Bandung  "],
    "Surabaya": ["Surabaya", "surabaya ", "SURABAYA", " Surabaya", "Surabaya"],
    "Medan": ["Medan", "MEDAN ", " medan", "Medan", "Medan "],
    "Semarang": ["Semarang", "SEMARANG", " semarang ", "Semarang", "Semarang "],
}
NAMA_KOTOR = ["andi saputra", "SITI AMINAH", " Budi Santoso", "dewi lestari ",
              "EKA PRATAMA", "  Fajar Nugroho", "rina kartika", "AGUS SETIAWAN ",
              "Maya Puspita", " yoga pratama"]


def buat_data_kotor(n_unik=100, n_duplikat=20, seed=11):
    rnd = random.Random(seed)
    baris = []
    for i in range(1, n_unik + 1):
        kota = rnd.choice(VARIAN_KOTA[rnd.choice(KOTA_BERSIH)])
        bulan = ["2026-08", "2026-09", "2026-10"][rnd.randrange(3)]
        tgl = date(int(bulan[:4]), int(bulan[5:]), rnd.randint(1, 28))
        kanal = rnd.choice(KANAL)
        nilai = rnd.randrange(150000, 3500000, 50000)
        baris.append([f"TRX-{i:04d}", tgl.isoformat(), rnd.choice(NAMA_KOTOR), kota, kanal, nilai])
    # 30 baris nilainya disimpan sebagai teks dengan pemisah ribuan
    for idx in rnd.sample(range(len(baris)), 30):
        baris[idx][5] = "{:,}".format(baris[idx][5]).replace(",", ".")
    # 20 baris duplikat: salinan persis dari baris yang sudah ada
    duplikat = [list(baris[i]) for i in rnd.sample(range(len(baris)), n_duplikat)]
    semua = baris + duplikat
    rnd.shuffle(semua)
    return semua


HEADER_B = ["id_transaksi", "tanggal", "nama_pelanggan", "kota", "kanal", "nilai"]


def parse_nilai(v):
    if isinstance(v, str):
        return int(v.replace(".", "").replace(" ", ""))
    return int(v)


def bersih_kota(v):
    return " ".join(str(v).split()).title()


def kunci_b(data):
    from collections import Counter
    ids = [r[0] for r in data]
    unik = list(dict.fromkeys(ids))
    baris_unik = {}
    for r in data:
        baris_unik.setdefault(r[0], r)
    total_semua = sum(parse_nilai(r[5]) for r in data)
    n_teks = sum(1 for r in data if isinstance(r[5], str))
    n_jakarta = sum(1 for r in data if "JAKARTA" in str(r[3]).upper())
    n_spasi = sum(1 for r in data if str(r[3]) != str(r[3]).strip())
    bersih = [[r[0], bersih_kota(r[3]), parse_nilai(r[5])] for r in baris_unik.values()]
    total_bersih = sum(b[2] for b in bersih)
    kota_unik = len({b[1] for b in bersih})
    gt_sejuta = sum(1 for b in bersih if b[2] > 1000000)
    rata = total_bersih / len(bersih)

    soal = [
        {"no": 1, "teks": "Jumlah baris di 2_Data (data mentah apa adanya).", "tipe": "angka",
         "baris": [{"kunci": "baris_mentah", "nilai": len(data)}]},
        {"no": 2, "teks": "Jumlah id_transaksi unik.", "tipe": "angka",
         "baris": [{"kunci": "id_unik", "nilai": len(unik)}]},
        {"no": 3, "teks": "Jumlah baris duplikat (baris mentah dikurangi id unik).", "tipe": "angka",
         "baris": [{"kunci": "baris_duplikat", "nilai": len(data) - len(unik)}]},
        {"no": 4, "teks": "Jumlah sel di kolom nilai yang tersimpan sebagai TEKS, bukan angka.",
         "tipe": "angka", "baris": [{"kunci": "nilai_berupa_teks", "nilai": n_teks}]},
        {"no": 5, "teks": "Total nilai seluruh 120 baris setelah teks dikonversi ke angka.",
         "tipe": "angka", "baris": [{"kunci": "total_nilai_semua", "nilai": total_semua}]},
        {"no": 6, "teks": "Jumlah baris yang kotanya mengandung 'jakarta' (abaikan huruf besar/kecil "
                          "dan spasi).", "tipe": "angka",
         "baris": [{"kunci": "baris_kota_jakarta", "nilai": n_jakarta}]},
        {"no": 7, "teks": "Jumlah baris yang kota-nya punya spasi berlebih di awal/akhir.",
         "tipe": "angka", "baris": [{"kunci": "baris_kota_spasi", "nilai": n_spasi}]},
        {"no": 8, "teks": "Jumlah baris di tabel DataBersih (setelah duplikat dibuang).", "tipe": "angka",
         "baris": [{"kunci": "baris_bersih", "nilai": len(bersih)}]},
        {"no": 9, "teks": "Total nilai di tabel DataBersih.", "tipe": "angka",
         "baris": [{"kunci": "total_nilai_bersih", "nilai": total_bersih}]},
        {"no": 10, "teks": "Jumlah kota unik di DataBersih setelah dibersihkan (TRIM + PROPER).",
         "tipe": "angka", "baris": [{"kunci": "kota_unik_bersih", "nilai": kota_unik}]},
        {"no": 11, "teks": "Jumlah baris DataBersih dengan nilai di atas 1.000.000.", "tipe": "angka",
         "baris": [{"kunci": "baris_nilai_gt_1jt", "nilai": gt_sejuta}]},
        {"no": 12, "teks": "Rata-rata nilai di DataBersih, bulatkan 0 desimal.", "tipe": "angka",
         "baris": [{"kunci": "rata_nilai_bersih", "nilai": round(rata, 0)}]},
    ]
    return soal, {"bersih": sorted(bersih)}


# ===================================================================== WORKBOOK
def tulis_workbook(nama_file, judul, masalah, data_header, data_baris, soal, catatan_kerja,
                   target_tabel=None, data_kotor=False):
    wb = Workbook()

    # ---- 1_Masalah
    ws = wb.active
    ws.title = "1_Masalah"
    judul_sheet(ws, "1. Masalah & Tujuan - %s" % judul)
    atur_lebar(ws, [26, 95])
    r = 3
    ws.cell(row=r, column=1, value="Konteks").font = BOLD
    for par in masalah["konteks"]:
        c = ws.cell(row=r, column=2, value=par)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Pertanyaan bisnis").font = BOLD
    for q in masalah["pertanyaan"]:
        c = ws.cell(row=r, column=2, value=q)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Tujuan latihan").font = BOLD
    for t in masalah["tujuan"]:
        c = ws.cell(row=r, column=2, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Tool yang dilatih").font = BOLD
    c = ws.cell(row=r, column=2, value=masalah["tool"])
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 2
    if target_tabel:
        ws.cell(row=r, column=1, value="Target revenue per region").font = BOLD
        r += 1
        tulis_baris(ws, r, ["Region", "Target (Rp)"], bold=True, fill=HEAD_FILL)
        r += 1
        for k, v in target_tabel.items():
            tulis_baris(ws, r, [k, v])
            r += 1
        ws.cell(row=r, column=2, value="Dipakai untuk soal capaian target.").font = Font(italic=True)

    # ---- 2_Data
    ws = wb.create_sheet("2_Data")
    judul_sheet(ws, "2. Data - jangan diubah (ini data mentah)", len(data_header))
    for j, h in enumerate(data_header, start=1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = BOLD
        c.fill = HEAD_FILL
        c.border = KOTAK
    for i, baris in enumerate(data_baris, start=4):
        for j, v in enumerate(baris, start=1):
            ws.cell(row=i, column=j, value=v)
    ws.freeze_panes = "A4"
    atur_lebar(ws, [14, 12, 22, 14, 14, 22, 8, 11, 9, 12][:len(data_header)] +
               [14] * max(0, len(data_header) - 10))
    ws.auto_filter.ref = "A3:%s%d" % (get_column_letter(len(data_header)), 3 + len(data_baris))

    # ---- 3_Soal
    ws = wb.create_sheet("3_Soal")
    judul_sheet(ws, "3. Soal - jawab di sheet 4_Kerja, blok A1", 5)
    atur_lebar(ws, [8, 78, 22, 26, 16])
    tulis_baris(ws, 3, ["No", "Pertanyaan", "Bentuk jawaban", "Letak jawaban", "Nilai di 5_Kunci"],
                bold=True, fill=HEAD_FILL)
    r = 4
    for s in soal:
        bentuk = {"angka": "satu angka", "teks": "teks", "tabel": "%d baris angka" % len(s["baris"])}[s["tipe"]]
        label = ", ".join(b["kunci"] for b in s["baris"]) if len(s["baris"]) > 1 else s["baris"][0]["kunci"]
        tulis_baris(ws, r, [s["no"], s["teks"], bentuk, "4_Kerja: " + label, "lihat 5_Kunci"])
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    ws.cell(row=r, column=2, value=catatan_kerja).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    ws.row_dimensions[r].height = 60

    # ---- 4_Kerja (blok jawaban)
    ws = wb.create_sheet("4_Kerja")
    judul_sheet(ws, "4. Kerja - tempat pivot/Power Query + blok jawaban (kolom C diisi kamu)", 6)
    tulis_baris(ws, 3, ["SOAL", "KUNCI BARIS", "JAWABAN", "CATATAN"], bold=True, fill=KERJA_FILL)
    r = 4
    for s in soal:
        for b in s["baris"]:
            ws.cell(row=r, column=1, value=s["no"]).border = KOTAK
            ws.cell(row=r, column=2, value=b["kunci"]).border = KOTAK
            c = ws.cell(row=r, column=3)
            c.border = KOTAK
            c.fill = PatternFill("solid", fgColor="FFFFFF")
            ws.cell(row=r, column=4, value="").border = KOTAK
            r += 1
    atur_lebar(ws, [8, 26, 18, 40])
    baris_catatan = r + 1
    ws.cell(row=baris_catatan, column=1,
            value=("Isi kolom C. Jangan pindahkan blok A3:C%d - penilai membaca dari situ. "
                   "Taruh pivot table / hasil Power Query di sebelah kanan blok (mulai kolom F) "
                   "atau di sheet baru." % (r - 1))).font = Font(italic=True)
    ws.merge_cells(start_row=baris_catatan, start_column=1, end_row=baris_catatan, end_column=6)

    # ---- 5_Kunci
    ws = wb.create_sheet("5_Kunci")
    judul_sheet(ws, "5. Kunci - buka setelah selesai mengerjakan", 4)
    tulis_baris(ws, 3, ["SOAL", "KUNCI BARIS", "NILAI YANG DIHARAPKAN"], bold=True, fill=KUNCI_FILL)
    r = 4
    for s in soal:
        for b in s["baris"]:
            tulis_baris(ws, r, [s["no"], b["kunci"], b["nilai"]])
            r += 1

    wb.save(os.path.join(LATIHAN, nama_file))
    return nama_file


def main():
    os.makedirs(LATIHAN, exist_ok=True)
    os.makedirs(KUNCI_DIR, exist_ok=True)

    # ---------- A: pivot
    data_a = buat_data_penjualan()
    soal_a, extra_a = kunci_a(data_a)
    masalah_a = {
        "konteks": [
            "Kamu analis di perusahaan retail fashion. Manajemen minta ringkasan kinerja penjualan "
            "3 bulan terakhir (Agustus-Oktober 2026) dari 240 transaksi yang tercatat.",
            "Data mentah ada di sheet 2_Data. Belum ada ringkasan apa pun.",
            "Manajemen tidak mau membaca tabel transaksi; mereka mau angka ringkas per region, "
            "per bulan, per kanal, plus beberapa turunan (pertumbuhan, kontribusi, capaian target).",
        ],
        "pertanyaan": [
            "Berapa total revenue dan total qty 3 bulan ini?",
            "Region mana yang menyumbang revenue terbesar, dan berapa kontribusinya?",
            "Bagaimana tren bulanan, dan berapa pertumbuhan Oktober dibanding September?",
            "Kanal mana yang paling produktif, dan bagaimana sebaran region x kanal?",
            "Apakah revenue Bali mencapai target yang ditetapkan?",
        ],
        "tujuan": [
            "Membuat PivotTable dari 240 baris data dan membaca hasilnya dengan benar.",
            "Menurunkan angka turunan (growth, kontribusi %, capaian target) dari hasil pivot.",
            "Membiasakan diri: eksplorasi dengan pivot dulu, baru tulis angka ke blok jawaban.",
        ],
        "tool": "PivotTable (Insert > PivotTable). Boleh juga pakai SUMIFS/COUNTIFS sebagai pembanding, "
                "tapi pivot yang utama.",
    }
    f_a = tulis_workbook(
        "level-3-dashboard-penjualan-pivot.xlsx",
        "Dashboard Penjualan (PivotTable)",
        masalah_a, HEADER_A, data_a, soal_a,
        catatan_kerja=("Cara kerja yang disarankan: (1) buat PivotTable dari 2_Data, (2) susun baris = region "
                       "dan bulan, kolom = kanal, nilai = sum of revenue, (3) untuk growth dan kontribusi "
                       "pakai rumus di luar pivot atau pivot 'show values as % of grand total', "
                       "(4) salin angka akhirnya ke kolom C blok jawaban sebagai NILAI (Paste Special > Values), "
                       "bukan formula yang belum dihitung."),
        target_tabel=TARGET_REGION)
    kunci_a_json = {"file": f_a, "judul": "Dashboard Penjualan (PivotTable)", "soal": soal_a,
                    "catatan": extra_a}
    json.dump(kunci_a_json, open(os.path.join(KUNCI_DIR, "dashboard-penjualan.json"), "w",
                                 encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---------- B: power query
    data_b = buat_data_kotor()
    soal_b, extra_b = kunci_b(data_b)
    masalah_b = {
        "konteks": [
            "Data ekspor dari sistem kasir selalu kotor: ada baris dobel, nama kota berantakan "
            "(spasi berlebih, huruf besar-kecil campur), dan sebagian nilai tersimpan sebagai teks "
            "dengan pemisah ribuan.",
            "Ada 120 baris di sheet 2_Data. Yang benar hanya 100 transaksi.",
            "Tugasmu membersihkan data itu, lalu menjawab beberapa angka dari data bersih.",
        ],
        "pertanyaan": [
            "Berapa baris yang sebenarnya duplikat, dan berapa transaksi unik?",
            "Berapa nilai yang tersimpan sebagai teks, dan berapa total nilai sebenarnya?",
            "Setelah dibersihkan, ada berapa kota unik dan berapa rata-rata nilai transaksi?",
        ],
        "tujuan": [
            "Memakai Power Query: hapus duplikat, TRIM, PROPER, ubah tipe data.",
            "Mengukur tingkat kekotoran data sebelum dibersihkan (duplikat, spasi, tipe salah).",
            "Menghasilkan satu tabel bersih yang bisa dipakai ulang, bukan hasil salin-tempel.",
        ],
        "tool": "Power Query (Data > From Table/Range). Hasil bersih harus jadi tabel bernama "
                "DataBersih dengan kolom: id_transaksi, kota_bersih, nilai.",
    }
    f_b = tulis_workbook(
        "level-3-pembersihan-data.xlsx",
        "Pembersihan Data (Power Query)",
        masalah_b, HEADER_B, data_b, soal_b,
        catatan_kerja=("Cara kerja yang disarankan: (1) Data > From Table/Range pada 2_Data, (2) Remove Duplicates "
                       "berdasarkan id_transaksi, (3) Transform > Format > Trim dan Capitalize Each Word pada kota, "
                       "(4) ganti '.' pada kolom nilai lalu ubah tipe jadi Whole Number, "
                       "(5) Close & Load To > tabel baru, beri nama tabel DataBersih, "
                       "kolom hasil: id_transaksi, kota_bersih, nilai. "
                       "Penilai mencari tabel bernama DataBersih; kalau tidak ada, sheet bernama DataBersih."))
    kunci_b_json = {"file": f_b, "judul": "Pembersihan Data (Power Query)", "soal": soal_b,
                    "bersih": extra_b["bersih"]}
    json.dump(kunci_b_json, open(os.path.join(KUNCI_DIR, "pembersihan-data.json"), "w",
                                 encoding="utf-8"), ensure_ascii=False, indent=1)

    print("dibuat:", f_a, "|", len(data_a), "baris data,", len(soal_a), "soal")
    print("dibuat:", f_b, "|", len(data_b), "baris data,", len(soal_b), "soal")
    print("kunci   :", KUNCI_DIR)


if __name__ == "__main__":
    main()
