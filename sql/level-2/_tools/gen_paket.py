#!/usr/bin/env python3
"""Generator SQL level 2 (paket-1..paket-3) untuk ~/learning-lab.

Struktur sama dengan level 1:
    sql/level-2/latihan/<set>-soal.md      + <set>-jawaban.sql
    sql/level-2/pendukung/                 penilai + data paket-1
    sql/level-2/<set>/pendukung/           penilai + data set itu
Fokus level 2: subquery, CTE, JOIN bertingkat, window function.
"""
import csv
import os
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> sql/level-2
LEVEL1_DATA = os.path.join(os.path.dirname(BASE), "level-1", "pendukung", "data")

CEK_TEMPLATE = '''#!/usr/bin/env python3
"""Penilai otomatis __JUDUL__.

Cara pakai:  python3 pendukung/cek_jawaban.py
Semua CSV di pendukung/data/ dimuat ke database SQLite sementara, query di
latihan/__SET__-jawaban.sql dijalankan, lalu hasilnya dibandingkan dengan kunci.
"""
import csv
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAMA_SET = "__SET__"
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
TABEL = __TABEL__
MARKER = re.compile(r"^--\\s*=+\\s*SOAL\\s+(\\d+)\\s*=+\\s*$", re.M)

# Tipe kolom wajib dideklarasikan, kalau tidak SQLite memberi TEXT affinity dan
# ORDER BY angka mengurutkan secara abjad.
SKEMA = __SKEMA__

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = __KUNCI__


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
        blok = "\\n".join(l for l in blok.splitlines() if not l.strip().startswith("--"))
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
    return "\\n".join("    %r" % (tuple(r),) for r in rows)


def detail(no):
    if no not in KUNCI:
        print("soal %d tidak ada. pilihan: %s" % (no, ", ".join(map(str, sorted(KUNCI)))))
        return 2
    con = bangun_db()
    jawab = baca_jawaban()
    q, urut = KUNCI[no]
    milik = jawab.get(no, "")
    kunci = con.execute(q).fetchall()
    print("SOAL %d - urutan diuji: %s\\n" % (no, "YA" if urut else "tidak"))
    print("-- query kamu --")
    print(milik if milik else "(kosong: belum ada query di bawah penanda SOAL %d)" % no)
    hasil = None
    if milik:
        try:
            hasil = con.execute(milik).fetchall()
        except Exception as e:
            print("\\n-- hasil kamu --")
            print("ERROR saat dijalankan: %s" % e)
        else:
            print("\\n-- hasil kamu (%d baris) --" % len(hasil))
            print(tabel(hasil))
    print("\\n-- kunci (%d baris) --" % len(kunci))
    print(q)
    print(tabel(kunci))
    if not milik:
        print("\\nKESIMPULAN: soal %d belum diisi - belum ada query di bawah penandanya." % no)
    elif hasil is None:
        print("\\nKESIMPULAN: querymu belum bisa dijalankan (lihat pesan ERROR di atas).")
    else:
        ok, pesan = sama(hasil, kunci, urut)
        print("\\nKESIMPULAN: %s" % ("BENAR" if ok else pesan))
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
    print("Penilai jawaban __JUDUL__ - %d soal\\n" % total)
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
    print("\\nSKOR: %d / %d benar" % (benar, total))
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
'''

JAWABAN_TEMPLATE = """-- Jawaban __JUDUL__
-- Tulis query-mu di bawah tiap penanda. Jangan ubah baris penandanya.
-- Satu soal = satu query, boleh multi-baris, boleh diakhiri titik koma.

__MARKER__
"""

README_TEMPLATE = """# __SET__ - __JUDUL__ (SQL level 2)

Set latihan SQL level 2. Fokus: subquery, CTE, JOIN bertingkat, window function.

## Isi

| Path | Fungsi |
|---|---|
| `../latihan/__SET__-soal.md` | __NSOAL__ soal + hasil yang diharapkan |
| `../latihan/__SET__-jawaban.sql` | **kamu tulis query di sini** |
| `pendukung/cek_jawaban.py` | penilai otomatis |
| `pendukung/data/*.csv` | __TDESC__ |

Soal & jawaban semua set level 2 dikumpulkan di `sql/level-2/latihan/`.

## Cara mengerjakan

```
cd sql/level-2
unset LD_LIBRARY_PATH
python3 __SET__/pendukung/cek_jawaban.py
python3 __SET__/pendukung/cek_jawaban.py --detail 3   # kalau ada yang SALAH
```

## Kriteria lulus

__NSOAL__/__NSOAL__ BENAR. __NM2__-__NM1__ benar = lulus bersyarat.

## Data

__CATATAN__
"""


def tulis_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def tulis_set(s):
    d = os.path.join(BASE, s["paket"])
    latihan = os.path.join(BASE, "latihan")
    pendukung = os.path.join(d, "pendukung")
    os.makedirs(d, exist_ok=True)
    os.makedirs(latihan, exist_ok=True)
    os.makedirs(os.path.join(pendukung, "data"), exist_ok=True)

    if s.get("salin_dari_level1"):
        for t in s["data"]:
            shutil.copy(os.path.join(LEVEL1_DATA, t + ".csv"),
                        os.path.join(pendukung, "data", t + ".csv"))
    else:
        for tabel, (header, rows) in s["data"].items():
            tulis_csv(os.path.join(pendukung, "data", tabel + ".csv"), header, rows)

    # soal.md
    out = ["# Soal SQL Level 2 - %s - %s\n" % (s["paket"].replace("-", " ").title(), s["judul"]),
           "Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):\n",
           "| Tabel | Kolom |", "|---|---|"]
    for tabel, (header, rows) in s["data"].items():
        out.append("| `%s` | %s |" % (tabel, ", ".join(header)))
    out.append("")
    out.append(s["catatan_soal"])
    out.append("")
    out.append("Kerjakan di `%s-jawaban.sql` (satu folder dengan berkas ini) di bawah tiap penanda soal."
               % s["paket"])
    out.append("")
    out.append("---")
    out.append("")
    for no, teks, kunci, urut in s["soal"]:
        out.append("### SOAL %d" % no)
        out.append(teks)
        out.append("")
    open(os.path.join(latihan, s["paket"] + "-soal.md"), "w", encoding="utf-8").write("\n".join(out))

    # jawaban.sql
    markers = "\n\n\n".join("-- === SOAL %d ===" % no for no, _, _, _ in s["soal"])
    open(os.path.join(latihan, s["paket"] + "-jawaban.sql"), "w", encoding="utf-8").write(
        JAWABAN_TEMPLATE.replace("__JUDUL__", s["judul"]).replace("__MARKER__", markers + "\n"))

    # cek_jawaban.py
    tabel_list = "[" + ", ".join('"%s"' % t for t in s["data"]) + "]"
    skema = "{\n"
    for tabel, (header, rows) in s["data"].items():
        skema += '    "%s": {%s},\n' % (tabel, ", ".join('"%s": "%s"' % (c, s["skema"][tabel][c])
                                                         for c in header))
    skema += "}"
    kunci = "{\n"
    for no, teks, k, urut in s["soal"]:
        kunci += "    %d: (%r, %s),\n" % (no, k, urut)
    kunci += "}"
    isi = (CEK_TEMPLATE.replace("__JUDUL__", s["judul"]).replace("__SET__", s["paket"])
           .replace("__TABEL__", tabel_list).replace("__SKEMA__", skema).replace("__KUNCI__", kunci))
    open(os.path.join(pendukung, "cek_jawaban.py"), "w", encoding="utf-8").write(isi)

    # README set
    n = len(s["soal"])
    tdesc = ", ".join("`%s` (%d baris)" % (t, len(rows)) for t, (header, rows) in s["data"].items())
    open(os.path.join(d, "README.md"), "w", encoding="utf-8").write(
        README_TEMPLATE.replace("__SET__", s["paket"]).replace("__JUDUL__", s["judul"])
        .replace("__NSOAL__", str(n)).replace("__NM2__", str(n - 2)).replace("__NM1__", str(n - 1))
        .replace("__TDESC__", "%d tabel: %s" % (len(s["data"]), tdesc))
        .replace("__CATATAN__", s["catatan_data"]))


# ===================================================================== paket-1
# Data sama dengan level-1 (4 tabel penjualan/lead/kampanye) supaya yang dilatih tekniknya.
P1_DATA = {
    "penjualan": (["id", "tanggal", "bulan", "region", "kanal", "produk", "qty", "harga",
                   "diskon", "revenue"], []),
    "kampanye_iklan": (["tanggal", "id_kampanye", "nama_kampanye", "kanal", "impresi", "klik",
                        "biaya", "konversi", "revenue"], []),
    "lead": (["tanggal_masuk", "id_lead", "nama", "kode_sumber", "kota", "status", "nilai"], []),
    "master_sumber": (["kode_sumber", "nama_sumber", "biaya_per_lead"], []),
}
P1_SKEMA = {
    "penjualan": {"id": "INTEGER", "tanggal": "TEXT", "bulan": "TEXT", "region": "TEXT",
                  "kanal": "TEXT", "produk": "TEXT", "qty": "INTEGER", "harga": "INTEGER",
                  "diskon": "REAL", "revenue": "INTEGER"},
    "kampanye_iklan": {"tanggal": "TEXT", "id_kampanye": "TEXT", "nama_kampanye": "TEXT",
                       "kanal": "TEXT", "impresi": "INTEGER", "klik": "INTEGER",
                       "biaya": "INTEGER", "konversi": "INTEGER", "revenue": "INTEGER"},
    "lead": {"tanggal_masuk": "TEXT", "id_lead": "TEXT", "nama": "TEXT", "kode_sumber": "TEXT",
             "kota": "TEXT", "status": "TEXT", "nilai": "INTEGER"},
    "master_sumber": {"kode_sumber": "TEXT", "nama_sumber": "TEXT", "biaya_per_lead": "INTEGER"},
}

PAKET1 = {
    "paket": "paket-1",
    "judul": "Subquery, CTE, dan window function pada data penjualan",
    "salin_dari_level1": True,
    "skema": P1_SKEMA,
    "data": P1_DATA,
    "catatan_soal": ("Data sama dengan SQL level 1 (penjualan 60 baris, kampanye_iklan 30, lead 28, "
                     "master_sumber 4), tapi soal-soalnya menuntut subquery, CTE, dan window function. "
                     "SQLite di sini mendukung CTE (`WITH`) dan window function (`OVER`)."),
    "catatan_data": ("Disalin dari `sql/level-1/pendukung/data`. Angka kunci level 2 dihitung dari data "
                     "yang sama, jadi hasil level 1 bisa dipakai sebagai pembanding."),
    "soal": [
        (1, "Jumlah transaksi yang `revenue`-nya di atas rata-rata seluruh transaksi (pakai subquery).\n"
            "Hasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM penjualan WHERE revenue > (SELECT AVG(revenue) FROM penjualan);", False),
        (2, "Produk unik yang pernah terjual di region `Jabodetabek` (pakai IN + subquery), urut A-Z.\n"
            "Hasil: 1 kolom berisi `produk`. Urutan diuji.",
         "SELECT DISTINCT produk FROM penjualan WHERE produk IN "
         "(SELECT produk FROM penjualan WHERE region = 'Jabodetabek') ORDER BY produk;", True),
        (3, "Total revenue per region, hanya region yang totalnya di atas rata-rata total antar-region.\n"
            "Pakai derived table (subquery di FROM) atau CTE.\n"
            "Hasil: kolom `region`, `total_revenue`. Urutan diuji (region A-Z).",
         "WITH t AS (SELECT region, SUM(revenue) AS total_revenue FROM penjualan GROUP BY region) "
         "SELECT region, total_revenue FROM t WHERE total_revenue > (SELECT AVG(total_revenue) FROM t) "
         "ORDER BY region;", True),
        (4, "Nama sumber lead yang punya minimal satu lead berstatus `Won` (pakai EXISTS), urut A-Z.\n"
            "Hasil: 1 kolom berisi `nama_sumber`. Urutan diuji.",
         "SELECT m.nama_sumber FROM master_sumber m WHERE EXISTS "
         "(SELECT 1 FROM lead l WHERE l.kode_sumber = m.kode_sumber AND l.status = 'Won') "
         "ORDER BY m.nama_sumber;", True),
        (5, "Produk yang **tidak pernah** terjual di region `Sumatera` (pakai NOT EXISTS), urut A-Z.\n"
            "Hasil: 1 kolom berisi `produk`. Urutan diuji.",
         "SELECT DISTINCT p.produk FROM penjualan p WHERE NOT EXISTS "
         "(SELECT 1 FROM penjualan x WHERE x.produk = p.produk AND x.region = 'Sumatera') "
         "ORDER BY p.produk;", True),
        (6, "Kanal iklan yang total biayanya di atas rata-rata total biaya antar-kanal, urut biaya menurun.\n"
            "Pakai CTE.\nHasil: kolom `kanal`, `total_biaya`. Urutan diuji.",
         "WITH t AS (SELECT kanal, SUM(biaya) AS total_biaya FROM kampanye_iklan GROUP BY kanal) "
         "SELECT kanal, total_biaya FROM t WHERE total_biaya > (SELECT AVG(total_biaya) FROM t) "
         "ORDER BY total_biaya DESC;", True),
        (7, "Per nama sumber lead: jumlah lead, jumlah lead `Won`, dan total biaya sumber itu "
            "(jumlah lead x `biaya_per_lead`), urut total biaya menurun.\n"
            "Hasil: kolom `nama_sumber`, `jumlah_lead`, `jumlah_won`, `total_biaya`. Urutan diuji.",
         "SELECT m.nama_sumber, COUNT(l.id_lead) AS jumlah_lead, "
         "SUM(CASE WHEN l.status = 'Won' THEN 1 ELSE 0 END) AS jumlah_won, "
         "COUNT(l.id_lead) * m.biaya_per_lead AS total_biaya "
         "FROM master_sumber m JOIN lead l ON l.kode_sumber = m.kode_sumber "
         "GROUP BY m.nama_sumber ORDER BY total_biaya DESC;", True),
        (8, "Transaksi terbesar di tiap region (satu baris per region), pakai ROW_NUMBER().\n"
            "Hasil: kolom `region`, `id`, `revenue`. Urutan diuji (region A-Z).",
         "SELECT region, id, revenue FROM (SELECT region, id, revenue, "
         "ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) AS rn FROM penjualan) "
         "WHERE rn = 1 ORDER BY region;", True),
        (9, "Revenue per bulan beserta total kumulatif sampai bulan itu (window SUM), urut bulan.\n"
            "Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.",
         "WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM penjualan GROUP BY bulan) "
         "SELECT bulan, revenue, SUM(revenue) OVER (ORDER BY bulan) AS kumulatif FROM t "
         "ORDER BY bulan;", True),
        (10, "Revenue per bulan beserta selisih terhadap bulan sebelumnya (pakai LAG), urut bulan.\n"
             "Hasil: kolom `bulan`, `revenue`, `selisih`. Urutan diuji.",
         "WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM penjualan GROUP BY bulan) "
         "SELECT bulan, revenue, revenue - LAG(revenue) OVER (ORDER BY bulan) AS selisih FROM t "
         "ORDER BY bulan;", True),
        (11, "Per region: total revenue dan persentase kontribusinya terhadap total seluruh region "
             "(pakai window SUM di atas agregat), dibulatkan 2 desimal, urut persen menurun.\n"
             "Hasil: kolom `region`, `total_revenue`, `persen`. Urutan diuji.",
         "SELECT region, SUM(revenue) AS total_revenue, "
         "ROUND(100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2) AS persen "
         "FROM penjualan GROUP BY region ORDER BY persen DESC;", True),
        (12, "Jumlah transaksi yang revenue-nya di atas rata-rata **region-nya sendiri** "
             "(subquery berkorelasi), 1 baris.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM penjualan p WHERE p.revenue > "
         "(SELECT AVG(x.revenue) FROM penjualan x WHERE x.region = p.region);", False),
    ],
}

# ===================================================================== paket-2 & 3
PAKET2 = {
    "paket": "paket-2",
    "judul": "Pesanan, item pesanan, dan produk (JOIN bertingkat)",
    "skema": {
        "pesanan": {"id_pesanan": "TEXT", "tanggal": "TEXT", "bulan": "TEXT",
                    "id_pelanggan": "TEXT", "kota": "TEXT", "status": "TEXT"},
        "item_pesanan": {"id_pesanan": "TEXT", "sku": "TEXT", "qty": "INTEGER", "harga": "INTEGER"},
        "produk": {"sku": "TEXT", "nama_produk": "TEXT", "kategori": "TEXT",
                   "harga_modal": "INTEGER"},
    },
    "data": {
        "pesanan": (["id_pesanan", "tanggal", "bulan", "id_pelanggan", "kota", "status"], [
            ["PS-01", "2026-08-03", "2026-08", "C-01", "Jakarta", "Selesai"],
            ["PS-02", "2026-08-07", "2026-08", "C-02", "Bandung", "Selesai"],
            ["PS-03", "2026-08-11", "2026-08", "C-03", "Surabaya", "Batal"],
            ["PS-04", "2026-08-15", "2026-08", "C-01", "Jakarta", "Selesai"],
            ["PS-05", "2026-08-20", "2026-08", "C-04", "Medan", "Proses"],
            ["PS-06", "2026-08-26", "2026-08", "C-05", "Jakarta", "Selesai"],
            ["PS-07", "2026-09-02", "2026-09", "C-02", "Bandung", "Selesai"],
            ["PS-08", "2026-09-06", "2026-09", "C-03", "Surabaya", "Selesai"],
            ["PS-09", "2026-09-10", "2026-09", "C-06", "Semarang", "Batal"],
            ["PS-10", "2026-09-14", "2026-09", "C-01", "Jakarta", "Selesai"],
            ["PS-11", "2026-09-19", "2026-09", "C-04", "Medan", "Selesai"],
            ["PS-12", "2026-09-23", "2026-09", "C-05", "Jakarta", "Proses"],
            ["PS-13", "2026-09-28", "2026-09", "C-02", "Bandung", "Selesai"],
            ["PS-14", "2026-10-02", "2026-10", "C-03", "Surabaya", "Selesai"],
            ["PS-15", "2026-10-06", "2026-10", "C-06", "Semarang", "Selesai"],
            ["PS-16", "2026-10-11", "2026-10", "C-01", "Jakarta", "Selesai"],
            ["PS-17", "2026-10-15", "2026-10", "C-04", "Medan", "Batal"],
            ["PS-18", "2026-10-19", "2026-10", "C-05", "Jakarta", "Selesai"],
            ["PS-19", "2026-10-23", "2026-10", "C-02", "Bandung", "Selesai"],
            ["PS-20", "2026-10-28", "2026-10", "C-03", "Surabaya", "Selesai"],
        ]),
        "item_pesanan": (["id_pesanan", "sku", "qty", "harga"], [
            ["PS-01", "SKU-A", 3, 95000], ["PS-01", "SKU-G", 2, 55000],
            ["PS-02", "SKU-C", 1, 245000],
            ["PS-03", "SKU-E", 1, 520000],
            ["PS-04", "SKU-B", 2, 215000],
            ["PS-05", "SKU-D", 2, 165000],
            ["PS-06", "SKU-A", 5, 95000], ["PS-06", "SKU-H", 1, 195000],
            ["PS-07", "SKU-E", 1, 520000], ["PS-07", "SKU-G", 3, 55000],
            ["PS-08", "SKU-C", 2, 245000], ["PS-08", "SKU-D", 1, 165000],
            ["PS-09", "SKU-F", 4, 120000],
            ["PS-10", "SKU-A", 2, 95000], ["PS-10", "SKU-B", 1, 215000],
            ["PS-11", "SKU-E", 2, 520000],
            ["PS-12", "SKU-H", 2, 195000],
            ["PS-13", "SKU-C", 3, 245000],
            ["PS-14", "SKU-B", 2, 215000], ["PS-14", "SKU-G", 1, 55000],
            ["PS-15", "SKU-D", 4, 165000],
            ["PS-16", "SKU-A", 6, 95000], ["PS-16", "SKU-C", 1, 245000],
            ["PS-16", "SKU-G", 2, 55000],
            ["PS-17", "SKU-F", 2, 120000],
            ["PS-18", "SKU-E", 1, 520000], ["PS-18", "SKU-H", 2, 195000],
            ["PS-19", "SKU-B", 3, 215000],
            ["PS-20", "SKU-A", 2, 95000], ["PS-20", "SKU-F", 3, 120000],
        ]),
        "produk": (["sku", "nama_produk", "kategori", "harga_modal"], [
            ["SKU-A", "Kaos Basic", "Atasan", 45000],
            ["SKU-B", "Kemeja Linen", "Atasan", 120000],
            ["SKU-C", "Chino Slim", "Bawahan", 150000],
            ["SKU-D", "Jogger Sport", "Bawahan", 95000],
            ["SKU-E", "Sneaker Urban", "Sepatu", 300000],
            ["SKU-F", "Sandal Slide", "Sepatu", 80000],
            ["SKU-G", "Topi Bordir", "Aksesoris", 35000],
            ["SKU-H", "Tas Selempang", "Aksesoris", 110000],
            ["SKU-I", "Rompi Outdoor", "Atasan", 175000],
        ]),
    },
    "catatan_soal": ("Catatan: satu pesanan punya banyak baris di `item_pesanan`, dan nama/kategori/harga modal "
                     "produk hanya ada di `produk`. Nilai satu pesanan = SUM(qty x harga). Status pesanan: "
                     "`Selesai`, `Batal`, `Proses` — soal yang menyebut revenue/pendapatan berarti hanya `Selesai`. "
                     "Satu SKU belum pernah terjual."),
    "catatan_data": ("`pesanan` 20 baris (2026-08 s/d 2026-10), `item_pesanan` 30 baris, `produk` 9 baris. "
                     "15 pesanan berstatus Selesai, 3 Batal, 2 Proses. `SKU-I` tidak pernah terjual."),
    "soal": [
        (1, "Total pendapatan (SUM(qty x harga)) dari pesanan berstatus `Selesai`.\nButuh JOIN 2 tabel.\n"
            "Hasil: 1 kolom, 1 baris.",
         "SELECT SUM(i.qty * i.harga) FROM item_pesanan i "
         "JOIN pesanan p ON p.id_pesanan = i.id_pesanan WHERE p.status = 'Selesai';", False),
        (2, "Pendapatan per kategori produk dari pesanan `Selesai`, urut menurun.\nButuh JOIN 3 tabel.\n"
            "Hasil: kolom `kategori`, `revenue`. Urutan diuji.",
         "SELECT pr.kategori, SUM(i.qty * i.harga) AS revenue FROM item_pesanan i "
         "JOIN pesanan p ON p.id_pesanan = i.id_pesanan JOIN produk pr ON pr.sku = i.sku "
         "WHERE p.status = 'Selesai' GROUP BY pr.kategori ORDER BY revenue DESC;", True),
        (3, "Jumlah SKU berbeda di tiap pesanan `Selesai`, urut jumlah menurun lalu `id_pesanan` menaik.\n"
            "Hasil: kolom `id_pesanan`, `jumlah_sku`. Urutan diuji.",
         "SELECT p.id_pesanan, COUNT(DISTINCT i.sku) AS jumlah_sku FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.id_pesanan ORDER BY jumlah_sku DESC, p.id_pesanan ASC;", True),
        (4, "Pesanan `Selesai` yang nilainya di atas rata-rata nilai pesanan `Selesai` (pakai CTE + subquery), "
            "urut nilai menurun.\nHasil: kolom `id_pesanan`, `nilai`. Urutan diuji.",
         "WITH t AS (SELECT p.id_pesanan, SUM(i.qty * i.harga) AS nilai FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.id_pesanan) SELECT id_pesanan, nilai FROM t "
         "WHERE nilai > (SELECT AVG(nilai) FROM t) ORDER BY nilai DESC;", True),
        (5, "SKU yang belum pernah muncul di `item_pesanan` sama sekali (pakai NOT EXISTS), urut A-Z.\n"
            "Hasil: 1 kolom berisi `sku`. Urutan diuji.",
         "SELECT pr.sku FROM produk pr WHERE NOT EXISTS "
         "(SELECT 1 FROM item_pesanan i WHERE i.sku = pr.sku) ORDER BY pr.sku;", True),
        (6, "Margin kotor per kategori = SUM(qty x (harga - harga_modal)) dari pesanan `Selesai`, "
            "urut menurun.\nButuh JOIN 3 tabel.\nHasil: kolom `kategori`, `margin`. Urutan diuji.",
         "SELECT pr.kategori, SUM(i.qty * (i.harga - pr.harga_modal)) AS margin FROM item_pesanan i "
         "JOIN pesanan p ON p.id_pesanan = i.id_pesanan JOIN produk pr ON pr.sku = i.sku "
         "WHERE p.status = 'Selesai' GROUP BY pr.kategori ORDER BY margin DESC;", True),
        (7, "Pelanggan yang total belanjanya (pesanan `Selesai`) di atas rata-rata pelanggan, urut menurun.\n"
            "Pakai CTE.\nHasil: kolom `id_pelanggan`, `total_belanja`. Urutan diuji.",
         "WITH t AS (SELECT p.id_pelanggan, SUM(i.qty * i.harga) AS total_belanja FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.id_pelanggan) SELECT id_pelanggan, total_belanja FROM t "
         "WHERE total_belanja > (SELECT AVG(total_belanja) FROM t) ORDER BY total_belanja DESC;", True),
        (8, "2 produk terlaris (qty terbanyak) di tiap kategori dari pesanan `Selesai`, pakai ROW_NUMBER().\n"
            "Urut kategori A-Z, lalu qty menurun.\nHasil: kolom `kategori`, `nama_produk`, `total_qty`. "
            "Urutan diuji.",
         "WITH t AS (SELECT pr.kategori, pr.nama_produk, SUM(i.qty) AS total_qty FROM item_pesanan i "
         "JOIN pesanan p ON p.id_pesanan = i.id_pesanan JOIN produk pr ON pr.sku = i.sku "
         "WHERE p.status = 'Selesai' GROUP BY pr.kategori, pr.nama_produk) "
         "SELECT kategori, nama_produk, total_qty FROM (SELECT *, "
         "ROW_NUMBER() OVER (PARTITION BY kategori ORDER BY total_qty DESC) AS rn FROM t) "
         "WHERE rn <= 2 ORDER BY kategori, total_qty DESC;", True),
        (9, "Pendapatan per bulan dari pesanan `Selesai` beserta total kumulatifnya, urut bulan.\n"
            "Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.",
         "WITH t AS (SELECT p.bulan, SUM(i.qty * i.harga) AS revenue FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.bulan) SELECT bulan, revenue, SUM(revenue) OVER (ORDER BY bulan) AS kumulatif "
         "FROM t ORDER BY bulan;", True),
        (10, "Rata-rata nilai pesanan `Selesai` per kota, beserta selisihnya dari rata-rata nasional "
             "(bulatkan 0 desimal), urut kota A-Z.\n"
             "Hasil: kolom `kota`, `rata_kota`, `selisih`. Urutan diuji.",
         "WITH pv AS (SELECT p.id_pesanan, p.kota, SUM(i.qty * i.harga) AS nilai FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.id_pesanan, p.kota), k AS (SELECT kota, AVG(nilai) AS rata_kota FROM pv "
         "GROUP BY kota) SELECT kota, ROUND(rata_kota, 0) AS rata_kota, "
         "ROUND(rata_kota - (SELECT AVG(nilai) FROM pv), 0) AS selisih FROM k ORDER BY kota;", True),
        (11, "Pesanan `Selesai` yang berisi lebih dari satu SKU: `id_pesanan` dan total qty-nya, "
             "urut total qty menurun lalu `id_pesanan` menaik.\n"
             "Hasil: kolom `id_pesanan`, `total_qty`. Urutan diuji.",
         "SELECT p.id_pesanan, SUM(i.qty) AS total_qty FROM pesanan p "
         "JOIN item_pesanan i ON i.id_pesanan = p.id_pesanan WHERE p.status = 'Selesai' "
         "GROUP BY p.id_pesanan HAVING COUNT(DISTINCT i.sku) > 1 "
         "ORDER BY total_qty DESC, p.id_pesanan ASC;", True),
        (12, "Kontribusi tiap kategori terhadap total pendapatan `Selesai`, dalam persen 2 desimal, "
             "urut persen menurun (pakai window SUM di atas agregat).\n"
             "Hasil: kolom `kategori`, `revenue`, `persen`. Urutan diuji.",
         "WITH t AS (SELECT pr.kategori, SUM(i.qty * i.harga) AS revenue FROM item_pesanan i "
         "JOIN pesanan p ON p.id_pesanan = i.id_pesanan JOIN produk pr ON pr.sku = i.sku "
         "WHERE p.status = 'Selesai' GROUP BY pr.kategori) "
         "SELECT kategori, revenue, ROUND(100.0 * revenue / SUM(revenue) OVER (), 2) AS persen "
         "FROM t ORDER BY persen DESC;", True),
    ],
}

# ===================================================================== paket-3
PAKET3 = {
    "paket": "paket-3",
    "judul": "Kunjungan pelanggan per kanal (window function)",
    "skema": {
        "kunjungan": {"tanggal": "TEXT", "bulan": "TEXT", "id_pelanggan": "TEXT", "kanal": "TEXT",
                      "sesi": "INTEGER", "revenue": "INTEGER"},
        "pelanggan": {"id_pelanggan": "TEXT", "nama": "TEXT", "kota": "TEXT"},
    },
    "data": {
        "kunjungan": (["tanggal", "bulan", "id_pelanggan", "kanal", "sesi", "revenue"], [
            ["2026-08-04", "2026-08", "PL-01", "Google", 12, 1450000],
            ["2026-09-06", "2026-09", "PL-01", "Google", 14, 1620000],
            ["2026-10-08", "2026-10", "PL-01", "Email", 9, 980000],
            ["2026-08-09", "2026-08", "PL-02", "Meta", 20, 2100000],
            ["2026-09-11", "2026-09", "PL-02", "Meta", 22, 2450000],
            ["2026-10-13", "2026-10", "PL-02", "Meta", 18, 1980000],
            ["2026-08-15", "2026-08", "PL-03", "Email", 7, 620000],
            ["2026-09-17", "2026-09", "PL-03", "Google", 11, 1340000],
            ["2026-10-19", "2026-10", "PL-03", "Google", 13, 1580000],
            ["2026-08-21", "2026-08", "PL-04", "Organic", 16, 880000],
            ["2026-09-23", "2026-09", "PL-04", "Organic", 18, 940000],
            ["2026-10-25", "2026-10", "PL-04", "Email", 12, 1120000],
            ["2026-08-05", "2026-08", "PL-05", "Google", 25, 3200000],
            ["2026-09-07", "2026-09", "PL-05", "Email", 19, 2400000],
            ["2026-10-09", "2026-10", "PL-05", "Google", 28, 3750000],
            ["2026-08-12", "2026-08", "PL-06", "Meta", 9, 760000],
            ["2026-09-14", "2026-09", "PL-06", "Meta", 10, 810000],
            ["2026-10-16", "2026-10", "PL-06", "Organic", 14, 1050000],
            ["2026-08-18", "2026-08", "PL-07", "Email", 21, 2900000],
            ["2026-09-20", "2026-09", "PL-07", "Google", 23, 3100000],
            ["2026-10-22", "2026-10", "PL-07", "Email", 24, 3300000],
            ["2026-08-24", "2026-08", "PL-08", "Organic", 13, 690000],
            ["2026-09-26", "2026-09", "PL-08", "Email", 15, 870000],
            ["2026-10-28", "2026-10", "PL-08", "Meta", 17, 1230000],
        ]),
        "pelanggan": (["id_pelanggan", "nama", "kota"], [
            ["PL-01", "Rani Anggraini", "Jakarta"],
            ["PL-02", "Sigit Pratama", "Bandung"],
            ["PL-03", "Tika Marlina", "Surabaya"],
            ["PL-04", "Umar Hidayat", "Medan"],
            ["PL-05", "Vina Oktavia", "Jakarta"],
            ["PL-06", "Wahyu Saputra", "Semarang"],
            ["PL-07", "Yuni Astuti", "Bandung"],
            ["PL-08", "Zaki Ramadhan", "Surabaya"],
        ]),
    },
    "catatan_soal": ("Catatan: tiap baris `kunjungan` = satu pelanggan pada satu bulan lewat satu kanal. "
                     "Setiap pelanggan punya tepat satu baris per bulan (3 bulan). Fokus set ini: "
                     "window function (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `SUM/AVG OVER`, `FIRST_VALUE`)."),
    "catatan_data": ("`kunjungan` 24 baris (8 pelanggan x 3 bulan), `pelanggan` 8 baris. Total revenue "
                     "41.120.000."),
    "soal": [
        (1, "Total revenue per kanal, urut menurun.\nHasil: kolom `kanal`, `total_revenue`. Urutan diuji.",
         "SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal "
         "ORDER BY total_revenue DESC;", True),
        (2, "Revenue per bulan beserta total kumulatifnya (window SUM), urut bulan.\n"
            "Hasil: kolom `bulan`, `revenue`, `kumulatif`. Urutan diuji.",
         "WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan) "
         "SELECT bulan, revenue, SUM(revenue) OVER (ORDER BY bulan) AS kumulatif FROM t "
         "ORDER BY bulan;", True),
        (3, "Pertumbuhan revenue bulanan dalam persen dibanding bulan sebelumnya (pakai LAG), "
            "dibulatkan 2 desimal, urut bulan.\n"
            "Hasil: kolom `bulan`, `revenue`, `growth_persen`. Urutan diuji.",
         "WITH t AS (SELECT bulan, SUM(revenue) AS revenue FROM kunjungan GROUP BY bulan) "
         "SELECT bulan, revenue, ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY bulan)) "
         "/ LAG(revenue) OVER (ORDER BY bulan), 2) AS growth_persen FROM t ORDER BY bulan;", True),
        (4, "Peringkat kanal berdasarkan revenue di tiap bulan (pakai RANK), urut bulan lalu peringkat.\n"
            "Hasil: kolom `bulan`, `kanal`, `revenue`, `peringkat`. Urutan diuji.",
         "WITH t AS (SELECT bulan, kanal, SUM(revenue) AS revenue FROM kunjungan "
         "GROUP BY bulan, kanal) SELECT bulan, kanal, revenue, "
         "RANK() OVER (PARTITION BY bulan ORDER BY revenue DESC) AS peringkat FROM t "
         "ORDER BY bulan, peringkat;", True),
        (5, "Kunjungan dengan revenue terbesar milik tiap pelanggan (satu baris per pelanggan, "
            "pakai ROW_NUMBER), urut `id_pelanggan` A-Z.\n"
            "Hasil: kolom `id_pelanggan`, `bulan`, `revenue`. Urutan diuji.",
         "SELECT id_pelanggan, bulan, revenue FROM (SELECT id_pelanggan, bulan, revenue, "
         "ROW_NUMBER() OVER (PARTITION BY id_pelanggan ORDER BY revenue DESC) AS rn FROM kunjungan) "
         "WHERE rn = 1 ORDER BY id_pelanggan;", True),
        (6, "Tiap baris kunjungan beserta rata-rata revenue kanalnya (pakai AVG OVER PARTITION), "
            "dibulatkan 0 desimal.\n"
            "Urut kanal A-Z, lalu bulan, lalu revenue menurun.\n"
            "Hasil: kolom `kanal`, `bulan`, `revenue`, `rata_kanal`. Urutan diuji.",
         "SELECT kanal, bulan, revenue, ROUND(AVG(revenue) OVER (PARTITION BY kanal), 0) AS rata_kanal "
         "FROM kunjungan ORDER BY kanal, bulan, revenue DESC;", True),
        (7, "Peringkat rapat (DENSE_RANK) kanal berdasarkan total revenue, urut peringkat.\n"
            "Hasil: kolom `kanal`, `total_revenue`, `peringkat`. Urutan diuji.",
         "WITH t AS (SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal) "
         "SELECT kanal, total_revenue, DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS peringkat "
         "FROM t ORDER BY peringkat;", True),
        (8, "Revenue per bulan per kanal, plus nama kanal dengan revenue terbesar di bulan itu "
            "(pakai FIRST_VALUE), urut bulan lalu revenue menurun.\n"
            "Hasil: kolom `bulan`, `kanal`, `revenue`, `kanal_top`. Urutan diuji.",
         "WITH t AS (SELECT bulan, kanal, SUM(revenue) AS revenue FROM kunjungan "
         "GROUP BY bulan, kanal) SELECT bulan, kanal, revenue, "
         "FIRST_VALUE(kanal) OVER (PARTITION BY bulan ORDER BY revenue DESC) AS kanal_top "
         "FROM t ORDER BY bulan, revenue DESC;", True),
        (9, "Total revenue kumulatif tiap pelanggan per bulan (SUM OVER PARTITION BY pelanggan), "
            "urut `id_pelanggan` lalu bulan.\n"
            "Hasil: kolom `id_pelanggan`, `bulan`, `revenue`, `kumulatif`. Urutan diuji.",
         "SELECT id_pelanggan, bulan, revenue, SUM(revenue) OVER "
         "(PARTITION BY id_pelanggan ORDER BY bulan) AS kumulatif FROM kunjungan "
         "ORDER BY id_pelanggan, bulan;", True),
        (10, "Selisih revenue tiap pelanggan dibanding bulannya yang lalu (LAG per pelanggan), "
             "urut `id_pelanggan` lalu bulan.\n"
             "Hasil: kolom `id_pelanggan`, `bulan`, `revenue`, `selisih`. Urutan diuji.",
         "SELECT id_pelanggan, bulan, revenue, revenue - LAG(revenue) OVER "
         "(PARTITION BY id_pelanggan ORDER BY bulan) AS selisih FROM kunjungan "
         "ORDER BY id_pelanggan, bulan;", True),
        (11, "Jumlah pelanggan unik per kanal, urut jumlah menurun lalu kanal A-Z.\n"
             "Hasil: kolom `kanal`, `jumlah_pelanggan`. Urutan diuji.",
         "SELECT kanal, COUNT(DISTINCT id_pelanggan) AS jumlah_pelanggan FROM kunjungan "
         "GROUP BY kanal ORDER BY jumlah_pelanggan DESC, kanal ASC;", True),
        (12, "Kanal yang total revenue-nya di atas rata-rata antar-kanal (pakai subquery), urut menurun.\n"
             "Hasil: kolom `kanal`, `total_revenue`. Urutan diuji.",
         "WITH t AS (SELECT kanal, SUM(revenue) AS total_revenue FROM kunjungan GROUP BY kanal) "
         "SELECT kanal, total_revenue FROM t WHERE total_revenue > (SELECT AVG(total_revenue) FROM t) "
         "ORDER BY total_revenue DESC;", True),
    ],
}


if __name__ == "__main__":
    for s in (PAKET1, PAKET2, PAKET3):
        tulis_set(s)
        print("dibuat:", os.path.join(BASE, s["paket"]))
