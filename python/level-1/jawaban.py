"""Jawaban Python Level 1 — isi fungsi di bawah ini.

Cara pakai:
    cd python/level-1
    unset LD_LIBRARY_PATH      # hanya di Termux
    python3 cek_jawaban.py

Selama sebuah fungsi masih berisi `raise NotImplementedError`, penilai menandainya KOSONG.
Kamu boleh menambah fungsi bantu sendiri di file ini.
"""


def baca_csv(path):
    """SOAL 1: baca CSV -> list of dict, angka bulat jadi int, angka desimal jadi float."""
    raise NotImplementedError


def total_revenue(rows):
    """SOAL 2: jumlahkan kolom revenue. -> int"""
    raise NotImplementedError


def total_qty(rows):
    """SOAL 3: jumlahkan kolom qty. -> int"""
    raise NotImplementedError


def revenue_per_region(rows):
    """SOAL 4: dict {region: total revenue}."""
    raise NotImplementedError


def transaksi_terbesar(rows):
    """SOAL 5: dict baris dengan revenue terbesar."""
    raise NotImplementedError


def id_diskon_minimal(rows, batas):
    """SOAL 6: list id dengan diskon >= batas, urut menaik."""
    raise NotImplementedError


def rata_rata_diskon_kanal(rows, kanal):
    """SOAL 7: rata-rata diskon untuk satu kanal. -> float 4 desimal"""
    raise NotImplementedError


def growth_bulanan(rows, bulan_awal, bulan_akhir):
    """SOAL 8: (revenue akhir - awal) / revenue awal. -> float 4 desimal"""
    raise NotImplementedError


def produk_unik(rows):
    """SOAL 9: list nama produk unik, urut menaik."""
    raise NotImplementedError


def top_produk(rows, n):
    """SOAL 10: list of tuple (produk, total revenue) terbesar, sebanyak n."""
    raise NotImplementedError


def roas_total(kampanye):
    """SOAL 11: total revenue / total biaya dari data kampanye. -> float 2 desimal"""
    raise NotImplementedError


def bersihkan_nama(nama):
    """SOAL 12: rapikan spasi + huruf besar di awal kata. -> str"""
    raise NotImplementedError
