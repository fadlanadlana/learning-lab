#!/usr/bin/env python3
"""Generator paket soal SQL level 1 (paket-2..paket-5) untuk ~/learning-lab.

Menulis data CSV, soal.md, jawaban.sql, cek_jawaban.py, README.md per paket.
Tema: marketing & sales, dataset baru tiap paket, level 1 (tanpa subquery/window).
"""
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> sql/level-1

CEK_TEMPLATE = '''#!/usr/bin/env python3
"""Penilai otomatis __JUDUL__.

Cara pakai:  python3 cek_jawaban.py            (dari folder __PAKET__)
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
TABEL = __TABEL__
MARKER = re.compile(r"^--\\s*=+\\s*SOAL\\s+(\\d+)\\s*=+\\s*$", re.M)

# Tipe kolom wajib dideklarasikan. Tanpa ini SQLite memberi TEXT affinity ke semua kolom,
# sehingga ORDER BY angka mengurutkan secara abjad dan perbandingan angka jadi perbandingan teks.
SKEMA = __SKEMA__

# ---------------------------------------------------------------- kunci jawaban (jangan diubah)
KUNCI = __KUNCI__


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
        blok = "\\n".join(l for l in blok.splitlines() if not l.strip().startswith("--"))
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
    print("SOAL %d — urutan diuji: %s\\n" % (no, "YA" if urut else "tidak"))
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
    if hasil is None:
        print("\\nKESIMPULAN: querymu belum bisa dijalankan. Kalau kamu menyalin dari cek_jawaban.py,")
        print("jangan salin tanda kutip ganda dan indentasi Python-nya — ambil isi SQL-nya saja.")
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
    print("Penilai jawaban __JUDUL__ — %d soal\\n" % total)
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
-- Setiap query boleh diakhiri titik koma. Satu soal = satu query.

__MARKER__
"""

README_TEMPLATE = """# __PAKET__ — __JUDUL__

Paket soal SQL level 1 (mandiri, data sendiri). Tingkat kesulitan sama dengan `../level-1`:
SELECT, WHERE, ORDER BY, LIMIT, agregasi, GROUP BY, HAVING, satu JOIN, CASE, DISTINCT, LIKE, IN.

## Isi folder

| File | Fungsi |
|---|---|
| `soal.md` | __NSOAL__ soal + hasil yang diharapkan (kolom & urutan) |
| `jawaban.sql` | **kamu tulis query di sini**, di bawah tiap penanda `-- === SOAL n ===` |
| `cek_jawaban.py` | penilai otomatis: CSV -> SQLite, querymu dijalankan, dibandingkan dengan kunci |
| `data/*.csv` | __TDESC__ |

## Cara mengerjakan

```
cd sql/level-1/__PAKET__
unset LD_LIBRARY_PATH            # hanya di Termux; di PC/Linux lewati baris ini
python3 cek_jawaban.py           # jalankan penilai
```

Penilai menampilkan **KOSONG**, **BENAR**, atau **SALAH** per soal, lalu skor.
Database dibangun ulang dari CSV setiap kali dijalankan.

Kalau satu soal tetap SALAH dan kamu tidak tahu sebabnya, periksa detailnya:

```
python3 cek_jawaban.py --detail 11
```

Perintah itu menampilkan query kamu apa adanya, hasil yang keluar, kunci beserta hasil kunci, dan
kesimpulan: isi beda, hanya urutan beda, atau query error.

## Kriteria lulus

__NSOAL__/__NSOAL__ BENAR. __NM2__-__NM1__ benar = lulus bersyarat: perbaiki yang SALAH dulu.

## Yang dinilai

- **Isi hasil** (baris x kolom), bukan nama alias kolom.
- **Urutan baris** hanya diuji pada soal yang meminta `ORDER BY`.
- Angka dibandingkan dengan toleransi 4 desimal.

## Data

__CATATAN__
"""


def tulis_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def tulis_paket(p):
    d = os.path.join(BASE, p["paket"])
    os.makedirs(os.path.join(d, "data"), exist_ok=True)

    for tabel, (header, rows) in p["data"].items():
        tulis_csv(os.path.join(d, "data", tabel + ".csv"), header, rows)

    # soal.md
    out = ["# Soal SQL %s — %s\n" % (p["paket"].replace("-", " ").title(), p["judul"]),
           "Tabel yang tersedia (nama tabel = nama file CSV, tanpa ekstensi):\n",
           "| Tabel | Kolom |", "|---|---|"]
    for tabel, (header, rows) in p["data"].items():
        out.append("| `%s` | %s |" % (tabel, ", ".join(header)))
    out.append("")
    out.append(p["catatan_soal"])
    out.append("")
    out.append("Kerjakan di `jawaban.sql` di bawah tiap penanda soal. Semua soal level 1 cukup dengan "
               "SELECT/WHERE/GROUP BY/JOIN — tidak perlu subquery.")
    out.append("")
    out.append("---")
    out.append("")
    for no, teks, kunci, urut in p["soal"]:
        out.append("### SOAL %d" % no)
        out.append(teks)
        out.append("")
    open(os.path.join(d, "soal.md"), "w", encoding="utf-8").write("\n".join(out))

    # jawaban.sql
    markers = "\n\n\n".join("-- === SOAL %d ===" % no for no, _, _, _ in p["soal"])
    open(os.path.join(d, "jawaban.sql"), "w", encoding="utf-8").write(
        JAWABAN_TEMPLATE.replace("__JUDUL__", p["judul"]).replace("__MARKER__", markers + "\n"))

    # cek_jawaban.py
    tabel_list = "[" + ", ".join('"%s"' % t for t in p["data"]) + "]"
    skema = "{\n"
    for tabel, (header, rows) in p["data"].items():
        skema += '    "%s": {%s},\n' % (tabel, ", ".join('"%s": "%s"' % (c, p["skema"][tabel][c])
                                                         for c in header))
    skema += "}"
    kunci = "{\n"
    for no, teks, k, urut in p["soal"]:
        kunci += "    %d: (%r, %s),\n" % (no, k, urut)
    kunci += "}"
    isi = (CEK_TEMPLATE.replace("__JUDUL__", p["judul"])
           .replace("__PAKET__", p["paket"])
           .replace("__TABEL__", tabel_list)
           .replace("__SKEMA__", skema)
           .replace("__KUNCI__", kunci))
    open(os.path.join(d, "cek_jawaban.py"), "w", encoding="utf-8").write(isi)

    # README.md
    n = len(p["soal"])
    tdesc = ", ".join("`%s` (%d baris)" % (t, len(rows)) for t, (header, rows) in p["data"].items())
    open(os.path.join(d, "README.md"), "w", encoding="utf-8").write(
        README_TEMPLATE.replace("__PAKET__", p["paket"]).replace("__JUDUL__", p["judul"])
        .replace("__NSOAL__", str(n)).replace("__NM2__", str(n - 2)).replace("__NM1__", str(n - 1))
        .replace("__TDESC__", "%d tabel: %s" % (len(p["data"]), tdesc))
        .replace("__CATATAN__", p["catatan_data"]))


# ===================================================================== paket-2
PAKET2 = {
    "paket": "paket-2",
    "judul": "Funnel website per kanal",
    "skema": {
        "trafik": {"tanggal": "TEXT", "bulan": "TEXT", "kanal": "TEXT", "device": "TEXT",
                   "sesi": "INTEGER", "konversi": "INTEGER", "revenue": "INTEGER"},
        "kanal_master": {"kanal": "TEXT", "jenis": "TEXT", "biaya_per_klik": "INTEGER"},
    },
    "data": {
        "trafik": (["tanggal", "bulan", "kanal", "device", "sesi", "konversi", "revenue"], [
            ["2026-08-03", "2026-08", "Google Ads", "Mobile", 420, 12, 3100000],
            ["2026-08-05", "2026-08", "Meta Ads", "Mobile", 380, 9, 1850000],
            ["2026-08-07", "2026-08", "Email", "Desktop", 150, 14, 2750000],
            ["2026-08-09", "2026-08", "Organic Search", "Mobile", 260, 5, 900000],
            ["2026-08-12", "2026-08", "Affiliate", "Desktop", 90, 3, 620000],
            ["2026-08-15", "2026-08", "Google Ads", "Desktop", 210, 8, 2400000],
            ["2026-08-18", "2026-08", "Meta Ads", "Tablet", 120, 2, 480000],
            ["2026-08-22", "2026-08", "Email", "Mobile", 175, 11, 1980000],
            ["2026-09-02", "2026-09", "Google Ads", "Mobile", 460, 15, 3750000],
            ["2026-09-04", "2026-09", "Meta Ads", "Mobile", 410, 10, 2100000],
            ["2026-09-06", "2026-09", "Email", "Desktop", 160, 16, 2980000],
            ["2026-09-09", "2026-09", "Organic Search", "Mobile", 300, 6, 1050000],
            ["2026-09-11", "2026-09", "Affiliate", "Desktop", 110, 4, 780000],
            ["2026-09-14", "2026-09", "Google Ads", "Desktop", 230, 9, 2650000],
            ["2026-09-17", "2026-09", "Meta Ads", "Tablet", 135, 3, 560000],
            ["2026-09-21", "2026-09", "Email", "Mobile", 185, 12, 2200000],
            ["2026-10-01", "2026-10", "Google Ads", "Mobile", 505, 17, 4120000],
            ["2026-10-03", "2026-10", "Meta Ads", "Mobile", 445, 11, 2380000],
            ["2026-10-05", "2026-10", "Email", "Desktop", 170, 18, 3250000],
            ["2026-10-08", "2026-10", "Organic Search", "Mobile", 330, 7, 1180000],
            ["2026-10-10", "2026-10", "Affiliate", "Desktop", 125, 5, 860000],
            ["2026-10-13", "2026-10", "Google Ads", "Desktop", 255, 10, 2900000],
            ["2026-10-16", "2026-10", "Meta Ads", "Tablet", 150, 4, 640000],
            ["2026-10-19", "2026-10", "Email", "Mobile", 200, 13, 2450000],
        ]),
        "kanal_master": (["kanal", "jenis", "biaya_per_klik"], [
            ["Google Ads", "Paid", 1200],
            ["Meta Ads", "Paid", 800],
            ["Affiliate", "Paid", 350],
            ["Email", "Owned", 50],
            ["Organic Search", "Organic", 25],
            ["TikTok Ads", "Paid", 900],
        ]),
    },
    "catatan_soal": ("Catatan: `sesi` = jumlah kunjungan, `konversi` = jumlah transaksi yang terjadi dari "
                     "kunjungan itu. `kanal_master.biaya_per_klik` dipakai untuk menghitung biaya: "
                     "`sesi * biaya_per_klik`. Satu kanal di `kanal_master` belum pernah punya baris trafik."),
    "catatan_data": ("`trafik` berisi 24 baris harian 3 bulan (2026-08 s/d 2026-10) untuk 5 kanal dan 3 device. "
                     "`kanal_master` berisi 6 kanal; `TikTok Ads` sengaja belum punya baris trafik."),
    "soal": [
        (1, "Total `sesi` seluruh tabel `trafik`.\nHasil: 1 kolom, 1 baris.",
         "SELECT SUM(sesi) FROM trafik;", False),
        (2, "Total `sesi` per `device`, urut dari terbesar.\nHasil: kolom `device`, `total_sesi`. Urutan diuji.",
         "SELECT device, SUM(sesi) AS total_sesi FROM trafik GROUP BY device ORDER BY total_sesi DESC;", True),
        (3, "5 baris dengan `revenue` terbesar.\nHasil: kolom `tanggal`, `kanal`, `revenue`. Urutan diuji (revenue menurun).",
         "SELECT tanggal, kanal, revenue FROM trafik ORDER BY revenue DESC LIMIT 5;", True),
        (4, "Jumlah baris trafik yang `revenue`-nya di bawah 1.000.000.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM trafik WHERE revenue < 1000000;", False),
        (5, "Rata-rata `revenue` per `sesi` untuk kanal `Email`, dibulatkan 4 desimal.\n"
            "Hasil: 1 kolom, 1 baris.",
         "SELECT ROUND(1.0*SUM(revenue)/SUM(sesi), 4) FROM trafik WHERE kanal = 'Email';", False),
        (6, "Total `revenue` per `bulan`, urut bulan menaik.\nHasil: kolom `bulan`, `total_revenue`. Urutan diuji.",
         "SELECT bulan, SUM(revenue) AS total_revenue FROM trafik GROUP BY bulan ORDER BY bulan ASC;", True),
        (7, "Kanal yang total `sesi`-nya di atas 1.500 (pakai HAVING), urut nama kanal A-Z.\n"
            "Hasil: 1 kolom berisi `kanal`. Urutan diuji.",
         "SELECT kanal FROM trafik GROUP BY kanal HAVING SUM(sesi) > 1500 ORDER BY kanal;", True),
        (8, "Jumlah `device` unik di tabel `trafik`.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(DISTINCT device) FROM trafik;", False),
        (9, "Per kanal: total biaya (`sesi * biaya_per_klik`), total revenue, dan ROAS "
            "(total revenue / total biaya, dibulatkan 2 desimal).\n"
            "Butuh JOIN ke `kanal_master`.\nHasil: kolom `kanal`, `total_biaya`, `total_revenue`, `roas`. "
            "Urutan diuji (ROAS menurun).",
         "SELECT t.kanal, SUM(t.sesi*m.biaya_per_klik) AS total_biaya, SUM(t.revenue) AS total_revenue, "
         "ROUND(1.0*SUM(t.revenue)/SUM(t.sesi*m.biaya_per_klik), 2) AS roas FROM trafik t "
         "JOIN kanal_master m ON m.kanal = t.kanal GROUP BY t.kanal ORDER BY roas DESC;", True),
        (10, "Total `revenue` untuk kanal berjenis `Paid` saja, urut nama kanal A-Z.\n"
             "Hasil: kolom `kanal`, `total_revenue`. Urutan diuji.",
         "SELECT t.kanal, SUM(t.revenue) AS total_revenue FROM trafik t "
         "JOIN kanal_master m ON m.kanal = t.kanal WHERE m.jenis = 'Paid' "
         "GROUP BY t.kanal ORDER BY t.kanal;", True),
        (11, "Beri label tiap kanal berdasarkan total revenue: `UTAMA` bila >= 15.000.000, `POTENSIAL` bila "
             ">= 8.000.000, sisanya `KECIL`.\n"
             "Hasil: kolom `kanal`, `label`. Urutan diuji (label A-Z, lalu kanal A-Z).",
         "SELECT kanal, CASE WHEN SUM(revenue) >= 15000000 THEN 'UTAMA' WHEN SUM(revenue) >= 8000000 "
         "THEN 'POTENSIAL' ELSE 'KECIL' END AS label FROM trafik GROUP BY kanal "
         "ORDER BY label, kanal;", True),
        (12, "Kanal yang terdaftar di `kanal_master` tapi belum punya satu baris pun di `trafik`.\n"
             "Butuh LEFT JOIN + menyaring baris tanpa pasangan.\n"
             "Hasil: 1 kolom berisi `kanal` — 1 baris.",
         "SELECT m.kanal FROM kanal_master m LEFT JOIN trafik t ON t.kanal = m.kanal "
         "WHERE t.kanal IS NULL;", False),
    ],
}

# ===================================================================== paket-3
PAKET3 = {
    "paket": "paket-3",
    "judul": "Repeat order pelanggan",
    "skema": {
        "pesanan": {"id_pesanan": "TEXT", "tanggal": "TEXT", "bulan": "TEXT", "id_pelanggan": "TEXT",
                    "kota": "TEXT", "kanal": "TEXT", "qty": "INTEGER", "nilai": "INTEGER"},
        "pelanggan": {"id_pelanggan": "TEXT", "nama": "TEXT", "segmen": "TEXT", "kota_domisili": "TEXT"},
        "ongkir": {"kota": "TEXT", "tarif_per_kg": "INTEGER"},
    },
    "data": {
        "pesanan": (["id_pesanan", "tanggal", "bulan", "id_pelanggan", "kota", "kanal", "qty", "nilai"], [
            ["PS-001", "2026-08-02", "2026-08", "P-01", "Jakarta", "Website", 3, 1450000],
            ["PS-002", "2026-08-05", "2026-08", "P-02", "Bandung", "Marketplace", 1, 320000],
            ["PS-003", "2026-08-08", "2026-08", "P-03", "Surabaya", "WhatsApp", 2, 980000],
            ["PS-004", "2026-08-11", "2026-08", "P-04", "Medan", "Marketplace", 1, 275000],
            ["PS-005", "2026-08-14", "2026-08", "P-01", "Jakarta", "Website", 4, 2100000],
            ["PS-006", "2026-08-19", "2026-08", "P-05", "Jakarta", "WhatsApp", 2, 760000],
            ["PS-007", "2026-08-23", "2026-08", "P-06", "Semarang", "Website", 1, 415000],
            ["PS-008", "2026-08-28", "2026-08", "P-07", "Bandung", "Marketplace", 5, 1875000],
            ["PS-009", "2026-09-03", "2026-09", "P-01", "Jakarta", "Website", 2, 1120000],
            ["PS-010", "2026-09-06", "2026-09", "P-03", "Surabaya", "WhatsApp", 3, 1340000],
            ["PS-011", "2026-09-09", "2026-09", "P-08", "Surabaya", "Marketplace", 1, 298000],
            ["PS-012", "2026-09-13", "2026-09", "P-05", "Jakarta", "Website", 6, 3250000],
            ["PS-013", "2026-09-17", "2026-09", "P-02", "Bandung", "WhatsApp", 2, 890000],
            ["PS-014", "2026-09-21", "2026-09", "P-09", "Medan", "Marketplace", 3, 1050000],
            ["PS-015", "2026-09-26", "2026-09", "P-07", "Bandung", "Website", 1, 640000],
            ["PS-016", "2026-09-29", "2026-09", "P-10", "Semarang", "Marketplace", 2, 520000],
            ["PS-017", "2026-10-02", "2026-10", "P-01", "Jakarta", "WhatsApp", 4, 2380000],
            ["PS-018", "2026-10-05", "2026-10", "P-03", "Surabaya", "Website", 2, 1180000],
            ["PS-019", "2026-10-08", "2026-10", "P-09", "Medan", "Marketplace", 1, 340000],
            ["PS-020", "2026-10-12", "2026-10", "P-05", "Jakarta", "WhatsApp", 3, 1560000],
            ["PS-021", "2026-10-16", "2026-10", "P-08", "Surabaya", "Website", 5, 2750000],
            ["PS-022", "2026-10-19", "2026-10", "P-04", "Medan", "WhatsApp", 2, 910000],
            ["PS-023", "2026-10-23", "2026-10", "P-06", "Semarang", "Marketplace", 1, 385000],
            ["PS-024", "2026-10-27", "2026-10", "P-07", "Bandung", "Website", 3, 1690000],
        ]),
        "pelanggan": (["id_pelanggan", "nama", "segmen", "kota_domisili"], [
            ["P-01", "Anisa Putri", "Loyal", "Jakarta"],
            ["P-02", "Budi Hartono", "Baru", "Bandung"],
            ["P-03", "Citra Dewi", "Loyal", "Surabaya"],
            ["P-04", "Dedi Kurniawan", "Baru", "Medan"],
            ["P-05", "Eka Saputra", "Loyal", "Jakarta"],
            ["P-06", "Fitri Handayani", "Baru", "Semarang"],
            ["P-07", "Gunawan Wibowo", "Loyal", "Bandung"],
            ["P-08", "Hana Permata", "Baru", "Surabaya"],
            ["P-09", "Indra Pratama", "Loyal", "Medan"],
            ["P-10", "Joko Susilo", "Baru", "Semarang"],
        ]),
        "ongkir": (["kota", "tarif_per_kg"], [
            ["Jakarta", 18000],
            ["Bandung", 22000],
            ["Surabaya", 25000],
            ["Medan", 32000],
            ["Makassar", 45000],
        ]),
    },
    "catatan_soal": ("Catatan: `kota` di tabel `pesanan` adalah kota pengiriman, bisa beda dengan "
                     "`kota_domisili` pelanggan. `segmen` pelanggan hanya `Loyal` atau `Baru`. "
                     "Satu kota di tabel `ongkir` belum pernah dikirimi pesanan."),
    "catatan_data": ("`pesanan` 24 baris (2026-08 s/d 2026-10) dari 10 pelanggan; `pelanggan` 10 baris; "
                     "`ongkir` 5 kota, `Makassar` sengaja tanpa pesanan."),
    "soal": [
        (1, "Total `nilai` seluruh pesanan.\nHasil: 1 kolom, 1 baris.",
         "SELECT SUM(nilai) FROM pesanan;", False),
        (2, "Jumlah pesanan per `id_pelanggan`, urut jumlah menurun. Kalau jumlahnya sama, urutkan "
            "`id_pelanggan` menaik (A-Z).\nHasil: kolom `id_pelanggan`, `jumlah_pesanan`. Urutan diuji.",
         "SELECT id_pelanggan, COUNT(*) AS jumlah_pesanan FROM pesanan GROUP BY id_pelanggan "
         "ORDER BY jumlah_pesanan DESC, id_pelanggan ASC;", True),
        (3, "3 pelanggan dengan total nilai pesanan terbesar, tampilkan `nama` (dari `pelanggan`, bukan "
            "ID-nya).\nButuh JOIN.\nHasil: kolom `nama`, `total_nilai`. Urutan diuji (total menurun).",
         "SELECT p.nama, SUM(o.nilai) AS total_nilai FROM pesanan o "
         "JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan GROUP BY p.nama "
         "ORDER BY total_nilai DESC LIMIT 3;", True),
        (4, "Jumlah pesanan dengan `nilai` minimal 1.000.000.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM pesanan WHERE nilai >= 1000000;", False),
        (5, "Rata-rata `qty` per pesanan untuk kanal `WhatsApp`, dibulatkan 2 desimal.\n"
            "Hasil: 1 kolom, 1 baris.",
         "SELECT ROUND(AVG(qty), 2) FROM pesanan WHERE kanal = 'WhatsApp';", False),
        (6, "Total `nilai` per `bulan`, urut bulan menaik.\nHasil: kolom `bulan`, `total_nilai`. Urutan diuji.",
         "SELECT bulan, SUM(nilai) AS total_nilai FROM pesanan GROUP BY bulan ORDER BY bulan ASC;", True),
        (7, "Kota pengiriman yang rata-rata nilai pesanannya di atas 900.000 (pakai HAVING), urut kota A-Z.\n"
            "Hasil: 1 kolom berisi `kota`. Urutan diuji.",
         "SELECT kota FROM pesanan GROUP BY kota HAVING AVG(nilai) > 900000 ORDER BY kota;", True),
        (8, "Jumlah kota unik yang pernah menerima pesanan.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(DISTINCT kota) FROM pesanan;", False),
        (9, "Per `segmen` pelanggan: jumlah pesanan dan total nilai, urut total nilai menurun.\n"
            "Butuh JOIN ke `pelanggan`.\nHasil: kolom `segmen`, `jumlah_pesanan`, `total_nilai`. Urutan diuji.",
         "SELECT p.segmen, COUNT(*) AS jumlah_pesanan, SUM(o.nilai) AS total_nilai FROM pesanan o "
         "JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan GROUP BY p.segmen "
         "ORDER BY total_nilai DESC;", True),
        (10, "Total nilai pesanan dari kanal `Marketplace` atau `Website` (pakai IN, bukan dua OR).\n"
             "Hasil: 1 kolom, 1 baris.",
         "SELECT SUM(nilai) FROM pesanan WHERE kanal IN ('Marketplace', 'Website');", False),
        (11, "Jumlah pesanan dari pelanggan yang namanya mengandung `Putri`.\n"
             "Butuh JOIN + LIKE.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM pesanan o JOIN pelanggan p ON p.id_pelanggan = o.id_pelanggan "
         "WHERE p.nama LIKE '%Putri%';", False),
        (12, "Kota yang ada di tabel `ongkir` tapi belum pernah menerima pesanan.\n"
             "Butuh LEFT JOIN + menyaring baris tanpa pasangan.\n"
             "Hasil: 1 kolom berisi `kota` — 1 baris.",
         "SELECT g.kota FROM ongkir g LEFT JOIN pesanan o ON o.kota = g.kota WHERE o.kota IS NULL;", False),
    ],
}

# ===================================================================== paket-4
PAKET4 = {
    "paket": "paket-4",
    "judul": "Biaya iklan dan CPL per platform",
    "skema": {
        "iklan_harian": {"tanggal": "TEXT", "bulan": "TEXT", "platform": "TEXT", "id_iklan": "TEXT",
                         "kreatif": "TEXT", "impresi": "INTEGER", "klik": "INTEGER",
                         "biaya": "INTEGER", "lead": "INTEGER"},
        "platform_master": {"platform": "TEXT", "jenis": "TEXT", "cpl_target": "INTEGER"},
    },
    "data": {
        "iklan_harian": (["tanggal", "bulan", "platform", "id_iklan", "kreatif", "impresi", "klik",
                          "biaya", "lead"], [
            ["2026-08-04", "2026-08", "Google Search", "IK-01", "Search Brand", 12000, 960, 2400000, 48],
            ["2026-08-06", "2026-08", "Meta", "IK-02", "Carousel Promo", 48000, 1440, 1800000, 36],
            ["2026-08-09", "2026-08", "TikTok", "IK-03", "Reels Tutorial", 65000, 1950, 1500000, 42],
            ["2026-08-12", "2026-08", "Meta", "IK-04", "Video Testimoni", 32000, 800, 1200000, 24],
            ["2026-08-16", "2026-08", "Google Search", "IK-05", "Search Generic", 9000, 630, 1600000, 21],
            ["2026-08-20", "2026-08", "TikTok", "IK-06", "Statis Diskon", 41000, 820, 900000, 12],
            ["2026-08-25", "2026-08", "Meta", "IK-02", "Carousel Promo", 52000, 1560, 1950000, 39],
            ["2026-08-29", "2026-08", "TikTok", "IK-03", "Reels Tutorial", 70000, 2100, 1650000, 45],
            ["2026-09-02", "2026-09", "Google Search", "IK-01", "Search Brand", 13500, 1080, 2700000, 54],
            ["2026-09-05", "2026-09", "Meta", "IK-04", "Video Testimoni", 36000, 900, 1350000, 27],
            ["2026-09-09", "2026-09", "TikTok", "IK-06", "Statis Diskon", 44000, 880, 950000, 14],
            ["2026-09-13", "2026-09", "Meta", "IK-02", "Carousel Promo", 56000, 1680, 2100000, 42],
            ["2026-09-18", "2026-09", "Google Search", "IK-05", "Search Generic", 10000, 700, 1750000, 24],
            ["2026-09-22", "2026-09", "TikTok", "IK-03", "Reels Tutorial", 76000, 2280, 1800000, 48],
            ["2026-09-27", "2026-09", "Meta", "IK-07", "Reels Testimoni", 28000, 560, 1050000, 18],
            ["2026-09-30", "2026-09", "Google Search", "IK-01", "Search Brand", 14000, 1120, 2800000, 56],
            ["2026-10-03", "2026-10", "Meta", "IK-02", "Carousel Promo", 60000, 1800, 2250000, 45],
            ["2026-10-07", "2026-10", "TikTok", "IK-03", "Reels Tutorial", 82000, 2460, 1950000, 51],
            ["2026-10-11", "2026-10", "Google Search", "IK-05", "Search Generic", 11000, 770, 1900000, 26],
            ["2026-10-15", "2026-10", "Meta", "IK-04", "Video Testimoni", 40000, 1000, 1500000, 30],
            ["2026-10-19", "2026-10", "TikTok", "IK-06", "Statis Diskon", 47000, 940, 1000000, 15],
            ["2026-10-23", "2026-10", "Google Search", "IK-01", "Search Brand", 15000, 1200, 3000000, 60],
            ["2026-10-26", "2026-10", "Meta", "IK-07", "Reels Testimoni", 31000, 620, 1150000, 20],
            ["2026-10-30", "2026-10", "TikTok", "IK-03", "Reels Tutorial", 88000, 2640, 2100000, 55],
        ]),
        "platform_master": (["platform", "jenis", "cpl_target"], [
            ["Google Search", "Search", 30000],
            ["Meta", "Social", 25000],
            ["TikTok", "Social", 20000],
            ["LinkedIn", "Social", 75000],
        ]),
    },
    "catatan_soal": ("Catatan: `biaya` dalam rupiah, `lead` = jumlah prospek yang masuk. CPL = biaya / lead. "
                     "Satu platform di `platform_master` belum pernah dipakai beriklan."),
    "catatan_data": ("`iklan_harian` 24 baris (2026-08 s/d 2026-10) dari 3 platform dan 7 kreatif; "
                     "`platform_master` 4 baris, `LinkedIn` sengaja tanpa baris iklan."),
    "soal": [
        (1, "Total `biaya` seluruh iklan.\nHasil: 1 kolom, 1 baris.",
         "SELECT SUM(biaya) FROM iklan_harian;", False),
        (2, "Total `impresi` per `platform`, urut dari terbesar.\n"
            "Hasil: kolom `platform`, `total_impresi`. Urutan diuji.",
         "SELECT platform, SUM(impresi) AS total_impresi FROM iklan_harian GROUP BY platform "
         "ORDER BY total_impresi DESC;", True),
        (3, "5 baris dengan `klik` terbanyak.\nHasil: kolom `tanggal`, `kreatif`, `klik`. "
            "Urutan diuji (klik menurun).",
         "SELECT tanggal, kreatif, klik FROM iklan_harian ORDER BY klik DESC LIMIT 5;", True),
        (4, "Jumlah baris iklan yang `lead`-nya di bawah 20.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM iklan_harian WHERE lead < 20;", False),
        (5, "CTR = total klik / total impresi untuk platform `TikTok`, dibulatkan 4 desimal.\n"
            "Hasil: 1 kolom, 1 baris.",
         "SELECT ROUND(1.0*SUM(klik)/SUM(impresi), 4) FROM iklan_harian WHERE platform = 'TikTok';", False),
        (6, "Total `biaya` per `bulan`, urut bulan menaik.\nHasil: kolom `bulan`, `total_biaya`. Urutan diuji.",
         "SELECT bulan, SUM(biaya) AS total_biaya FROM iklan_harian GROUP BY bulan ORDER BY bulan ASC;", True),
        (7, "Kreatif yang total `lead`-nya minimal 100 (pakai HAVING), urut lead menurun.\n"
            "Hasil: kolom `kreatif`, `total_lead`. Urutan diuji.",
         "SELECT kreatif, SUM(lead) AS total_lead FROM iklan_harian GROUP BY kreatif "
         "HAVING SUM(lead) >= 100 ORDER BY total_lead DESC;", True),
        (8, "Jumlah `kreatif` unik yang pernah dipakai.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(DISTINCT kreatif) FROM iklan_harian;", False),
        (9, "Per platform: total biaya, total lead, dan CPL (biaya / lead, dibulatkan 0 desimal).\n"
            "Urut dari CPL termurah.\nHasil: kolom `platform`, `total_biaya`, `total_lead`, `cpl`. "
            "Urutan diuji.",
         "SELECT platform, SUM(biaya) AS total_biaya, SUM(lead) AS total_lead, "
         "ROUND(1.0*SUM(biaya)/SUM(lead), 0) AS cpl FROM iklan_harian GROUP BY platform "
         "ORDER BY cpl ASC;", True),
        (10, "Total `lead` dari platform berjenis `Search` saja.\nButuh JOIN ke `platform_master`.\n"
             "Hasil: 1 kolom, 1 baris.",
         "SELECT SUM(i.lead) FROM iklan_harian i JOIN platform_master m ON m.platform = i.platform "
         "WHERE m.jenis = 'Search';", False),
        (11, "Beri label efisiensi per platform berdasarkan CPL: `EFISIEN` bila CPL <= 45.000, `SEDANG` "
             "bila <= 55.000, sisanya `MAHAL`. Tampilkan platform dan labelnya, urut label A-Z, "
             "lalu platform A-Z.\nHasil: kolom `platform`, `label_cpl`. Urutan diuji.",
         "SELECT platform, CASE WHEN ROUND(1.0*SUM(biaya)/SUM(lead), 0) <= 45000 THEN 'EFISIEN' "
         "WHEN ROUND(1.0*SUM(biaya)/SUM(lead), 0) <= 55000 THEN 'SEDANG' ELSE 'MAHAL' END AS label_cpl "
         "FROM iklan_harian GROUP BY platform ORDER BY label_cpl, platform;", True),
        (12, "Platform yang terdaftar di `platform_master` tapi belum punya satu baris iklan pun.\n"
             "Butuh LEFT JOIN + menyaring baris tanpa pasangan.\n"
             "Hasil: 1 kolom berisi `platform` — 1 baris.",
         "SELECT m.platform FROM platform_master m LEFT JOIN iklan_harian i ON i.platform = m.platform "
         "WHERE i.platform IS NULL;", False),
    ],
}

# ===================================================================== paket-5
PAKET5 = {
    "paket": "paket-5",
    "judul": "Penjualan produk dan status stok",
    "skema": {
        "penjualan_produk": {"tanggal": "TEXT", "bulan": "TEXT", "sku": "TEXT", "qty": "INTEGER",
                             "harga": "INTEGER", "revenue": "INTEGER"},
        "produk": {"sku": "TEXT", "nama_produk": "TEXT", "kategori": "TEXT",
                   "stok_akhir": "INTEGER", "harga_modal": "INTEGER"},
    },
    "data": {
        "penjualan_produk": (["tanggal", "bulan", "sku", "qty", "harga", "revenue"], [
            ["2026-08-03", "2026-08", "SKU-01", 21, 95000, 1995000],
            ["2026-08-06", "2026-08", "SKU-03", 12, 245000, 2940000],
            ["2026-08-10", "2026-08", "SKU-05", 6, 420000, 2520000],
            ["2026-08-14", "2026-08", "SKU-07", 30, 75000, 2250000],
            ["2026-08-18", "2026-08", "SKU-02", 8, 215000, 1720000],
            ["2026-08-22", "2026-08", "SKU-09", 5, 395000, 1975000],
            ["2026-08-27", "2026-08", "SKU-04", 14, 175000, 2450000],
            ["2026-08-30", "2026-08", "SKU-10", 18, 120000, 2160000],
            ["2026-09-04", "2026-09", "SKU-01", 24, 95000, 2280000],
            ["2026-09-08", "2026-09", "SKU-06", 7, 520000, 3640000],
            ["2026-09-12", "2026-09", "SKU-03", 15, 245000, 3675000],
            ["2026-09-16", "2026-09", "SKU-05", 9, 420000, 3780000],
            ["2026-09-20", "2026-09", "SKU-08", 11, 195000, 2145000],
            ["2026-09-24", "2026-09", "SKU-07", 26, 75000, 1950000],
            ["2026-09-28", "2026-09", "SKU-09", 4, 395000, 1580000],
            ["2026-09-30", "2026-09", "SKU-02", 10, 215000, 2150000],
            ["2026-10-05", "2026-10", "SKU-01", 28, 95000, 2660000],
            ["2026-10-09", "2026-10", "SKU-03", 18, 245000, 4410000],
            ["2026-10-13", "2026-10", "SKU-06", 9, 520000, 4680000],
            ["2026-10-17", "2026-10", "SKU-05", 12, 420000, 5040000],
            ["2026-10-21", "2026-10", "SKU-08", 14, 195000, 2730000],
            ["2026-10-24", "2026-10", "SKU-04", 20, 175000, 3500000],
            ["2026-10-28", "2026-10", "SKU-07", 35, 75000, 2625000],
            ["2026-10-31", "2026-10", "SKU-10", 22, 120000, 2640000],
        ]),
        "produk": (["sku", "nama_produk", "kategori", "stok_akhir", "harga_modal"], [
            ["SKU-01", "Kaos Polos Hitam", "Atasan", 120, 55000],
            ["SKU-02", "Kemeja Flanel", "Atasan", 8, 145000],
            ["SKU-03", "Chino Panjang", "Bawahan", 0, 165000],
            ["SKU-04", "Celana Jogger", "Bawahan", 35, 120000],
            ["SKU-05", "Sepatu Sneaker", "Sepatu", 4, 320000],
            ["SKU-06", "Sepatu Formal", "Sepatu", 22, 410000],
            ["SKU-07", "Topi Baseball", "Aksesoris", 90, 45000],
            ["SKU-08", "Tas Kanvas", "Aksesoris", 0, 135000],
            ["SKU-09", "Jaket Bomber", "Atasan", 15, 280000],
            ["SKU-10", "Sabuk Kulit", "Aksesoris", 60, 85000],
            ["SKU-11", "Sandal Kulit", "Sepatu", 12, 210000],
            ["SKU-12", "Rompi Denim", "Atasan", 6, 190000],
        ]),
    },
    "catatan_soal": ("Catatan: tabel `penjualan_produk` **tidak** punya kolom kategori — kategori dan "
                     "nama produk hanya ada di tabel `produk`, jadi soal yang menyebut kategori butuh JOIN. "
                     "Ada SKU di `produk` yang belum pernah terjual."),
    "catatan_data": ("`penjualan_produk` 24 baris (2026-08 s/d 2026-10); `produk` 12 baris, "
                     "`SKU-11` dan `SKU-12` sengaja belum pernah terjual."),
    "soal": [
        (1, "Total `qty` yang terjual.\nHasil: 1 kolom, 1 baris.",
         "SELECT SUM(qty) FROM penjualan_produk;", False),
        (2, "Total `qty` terjual per `kategori`, urut dari terbesar.\nButuh JOIN ke `produk`.\n"
            "Hasil: kolom `kategori`, `total_qty`. Urutan diuji.",
         "SELECT p.kategori, SUM(s.qty) AS total_qty FROM penjualan_produk s "
         "JOIN produk p ON p.sku = s.sku GROUP BY p.kategori ORDER BY total_qty DESC;", True),
        (3, "5 baris dengan `revenue` terbesar.\nHasil: kolom `tanggal`, `sku`, `revenue`. "
            "Urutan diuji (revenue menurun).",
         "SELECT tanggal, sku, revenue FROM penjualan_produk ORDER BY revenue DESC LIMIT 5;", True),
        (4, "Jumlah transaksi dengan `qty` minimal 20.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(*) FROM penjualan_produk WHERE qty >= 20;", False),
        (5, "Rata-rata `harga` per transaksi untuk kategori `Sepatu`, dibulatkan 0 desimal.\n"
            "Butuh JOIN ke `produk`.\nHasil: 1 kolom, 1 baris.",
         "SELECT ROUND(AVG(s.harga), 0) FROM penjualan_produk s JOIN produk p ON p.sku = s.sku "
         "WHERE p.kategori = 'Sepatu';", False),
        (6, "Total `revenue` per `bulan`, urut bulan menaik.\nHasil: kolom `bulan`, `total_revenue`. "
            "Urutan diuji.",
         "SELECT bulan, SUM(revenue) AS total_revenue FROM penjualan_produk GROUP BY bulan "
         "ORDER BY bulan ASC;", True),
        (7, "Kategori dengan total `qty` di atas 80 (pakai HAVING), urut kategori A-Z.\nButuh JOIN.\n"
            "Hasil: 1 kolom berisi `kategori`. Urutan diuji.",
         "SELECT p.kategori FROM penjualan_produk s JOIN produk p ON p.sku = s.sku "
         "GROUP BY p.kategori HAVING SUM(s.qty) > 80 ORDER BY p.kategori;", True),
        (8, "Jumlah SKU unik yang pernah terjual.\nHasil: 1 kolom, 1 baris.",
         "SELECT COUNT(DISTINCT sku) FROM penjualan_produk;", False),
        (9, "Per SKU: `nama_produk` (dari tabel `produk`) dan total `qty` terjual, urut total qty menurun.\n"
            "Hasil: kolom `nama_produk`, `total_qty`. Urutan diuji.",
         "SELECT p.nama_produk, SUM(s.qty) AS total_qty FROM penjualan_produk s "
         "JOIN produk p ON p.sku = s.sku GROUP BY p.nama_produk ORDER BY total_qty DESC;", True),
        (10, "Total `revenue` dari produk berkategori `Aksesoris` saja.\nButuh JOIN.\n"
             "Hasil: 1 kolom, 1 baris.",
         "SELECT SUM(s.revenue) FROM penjualan_produk s JOIN produk p ON p.sku = s.sku "
         "WHERE p.kategori = 'Aksesoris';", False),
        (11, "Beri label stok tiap SKU: `HABIS` bila `stok_akhir` = 0, `TIPIS` bila di bawah 10, "
             "sisanya `AMAN`. Hitung jumlah SKU per label, urut label A-Z.\n"
             "Hasil: kolom `label_stok`, `jumlah_sku`. Urutan diuji.",
         "SELECT CASE WHEN stok_akhir = 0 THEN 'HABIS' WHEN stok_akhir < 10 THEN 'TIPIS' "
         "ELSE 'AMAN' END AS label_stok, COUNT(*) AS jumlah_sku FROM produk "
         "GROUP BY label_stok ORDER BY label_stok;", True),
        (12, "SKU yang terdaftar di `produk` tapi belum pernah terjual sama sekali.\n"
             "Butuh LEFT JOIN + menyaring baris tanpa pasangan.\n"
             "Hasil: 1 kolom berisi `sku`. Urutan diuji (sku A-Z).",
         "SELECT p.sku FROM produk p LEFT JOIN penjualan_produk s ON s.sku = p.sku "
         "WHERE s.sku IS NULL ORDER BY p.sku;", True),
    ],
}


if __name__ == "__main__":
    for p in (PAKET2, PAKET3, PAKET4, PAKET5):
        tulis_paket(p)
        print("dibuat:", os.path.join(BASE, p["paket"]))
