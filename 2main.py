"""
TuneLog - Music & Mood Library Manager (Terminal App)
Penyimpanan: File teks (.txt) menggunakan modul `os`
Topik: Koleksi (tuple, list, dict, set), Fungsi & Rekursi,
       Searching (Sequential), Sorting (Bubble Sort), Manipulasi String.
"""

import os

# ============================================================
# KONSTANTA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_LAGU = os.path.join(BASE_DIR, "songs.txt")
FILE_LAPORAN = os.path.join(BASE_DIR, "laporan_musik.txt")

LEBAR_LAYAR = 74
HEADER_FILE = "# ID|Judul|Artis|Genre|Mood|Rating\n"
RATING_DEFAULT = 5

MOODS = ("Happy", "Sad", "Calm", "Energetic", "Romantic", "Focused")
GENRES = ("Pop", "Pop Rock", "Indie", "R&B", "Jazz", "Instrumental", "Acoustic")

WARNA = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
}


# ============================================================
# 1. UTILITAS STRING & UI TERMINAL
# ============================================================
def bersihkan_layar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def warnai(teks, kode):
    kode_warna = WARNA.get(kode, "")
    return f"{kode_warna}{teks}{WARNA['RESET']}"


def sanitasi(teks):
    teks = teks.strip()
    teks = teks.replace("|", "/")
    kata_kata = teks.split()
    return " ".join(kata_kata)


def potong(teks, batas):
    teks = str(teks)
    if len(teks) <= batas:
        return teks
    return teks[: batas - 3] + "..."


def konfirmasi(pertanyaan):
    jawaban = input(pertanyaan).strip().lower()
    return jawaban == "y"


def parse_rating(teks):
    """Ubah teks menjadi rating 1-5. Return None kalau tidak valid."""
    teks = teks.strip()
    if not teks.isdigit():
        return None

    angka = int(teks)
    if 1 <= angka <= 5:
        return angka
    return None


def cetak_header(judul, subjudul=""):
    garis = "=" * LEBAR_LAYAR
    print(warnai(garis, "CYAN"))
    print(warnai(judul.center(LEBAR_LAYAR), "BOLD"))
    if subjudul:
        print(warnai(subjudul.center(LEBAR_LAYAR), "YELLOW"))
    print(warnai(garis, "CYAN"))


def pilih_opsi(label, opsi, izinkan_kosong=False):
    daftar_pilihan = []
    for nomor, nama in enumerate(opsi, 1):
        daftar_pilihan.append(f"[{nomor}] {nama}")
    print(f"\n{label}: " + ", ".join(daftar_pilihan))

    if izinkan_kosong:
        prompt = "Pilih nomor/nama (Enter=Semua): "
    else:
        prompt = "Pilih nomor/nama: "

    while True:
        masukan = sanitasi(input(prompt))

        if izinkan_kosong and masukan in ("", "0"):
            return ""

        if masukan.isdigit():
            nomor = int(masukan)
            if 1 <= nomor <= len(opsi):
                return opsi[nomor - 1]

        for item in opsi:
            if masukan.casefold() == item.casefold():
                return item

        print(warnai("Pilihan tidak valid, coba lagi.", "RED"))


def tampilkan_tabel(daftar, judul="DAFTAR LAGU"):
    print(f"\n{warnai(judul, 'BOLD')}")

    if not daftar:
        print(warnai("  [Data lagu kosong / tidak ditemukan]", "YELLOW"))
        return

    garis =       "+----+-----------------------+-------------------+--------------+-----------+--------+"
    judul_kolom = "| ID | Judul Lagu            | Artis             | Genre        | Mood      | Rating |"

    print(garis)
    print(warnai(judul_kolom, "CYAN"))
    print(garis)

    for lagu in daftar:
        bintang = "*" * lagu["rating"] + "-" * (5 - lagu["rating"])
        kolom_id = f"{lagu['id']:>2}"
        kolom_judul = f"{potong(lagu['title'], 21):<21}"
        kolom_artis = f"{potong(lagu['artist'], 17):<17}"
        kolom_genre = f"{potong(lagu['genre'], 12):<12}"
        kolom_mood = f"{lagu['mood']:<9}"
        kolom_rating = f"{bintang:^6}"

        print(
            f"| {kolom_id} | {kolom_judul} | {kolom_artis} | "
            f"{kolom_genre} | {kolom_mood} | {kolom_rating} |"
        )

    print(garis)
    print(f"Total ditampilkan: {warnai(len(daftar), 'GREEN')} lagu")


# ============================================================
# 2. FILE I/O (.txt dengan modul os)
# ============================================================
def muat_lagu():
    if not os.path.exists(FILE_LAGU):
        with open(FILE_LAGU, "w", encoding="utf-8") as file:
            file.write(HEADER_FILE)
        return []

    daftar = []

    with open(FILE_LAGU, "r", encoding="utf-8") as file:
        for baris in file:
            baris = baris.strip()

            if not baris or baris.startswith("#"):
                continue

            kolom = baris.split("|")
            print(kolom)
            if len(kolom) != 6:
                continue
            if not kolom[0].strip().isdigit():
                continue

            if kolom[5].strip().isdigit():
                rating = int(kolom[5])
            else:
                rating = RATING_DEFAULT
            rating = max(1, min(5, rating))

            lagu = {
                "id": int(kolom[0]),
                "title": kolom[1].strip(),
                "artist": kolom[2].strip(),
                "genre": kolom[3].strip(),
                "mood": kolom[4].strip(),
                "rating": rating,
            }
            daftar.append(lagu)


    return daftar


def simpan_lagu(daftar):
    terurut = bubble_sort(daftar, "id")

    with open(FILE_LAGU, "w", encoding="utf-8") as file:
        file.write(HEADER_FILE)

        for lagu in terurut:
            baris = (
                f"{lagu['id']}|{lagu['title']}|{lagu['artist']}|"
                f"{lagu['genre']}|{lagu['mood']}|{lagu['rating']}\n"
            )
            file.write(baris)


# ============================================================
# 3. SEARCHING, SORTING (MANUAL), & REKURSI
# ============================================================
def cari_by_id(daftar, target_id):
    for lagu in daftar:
        if lagu["id"] == target_id:
            return lagu
    return None


def lagu_sudah_ada(daftar, judul, artis):
    for lagu in daftar:
        judul_sama = lagu["title"].casefold() == judul.casefold()
        artis_sama = lagu["artist"].casefold() == artis.casefold()
        if judul_sama and artis_sama:
            return True
    return False


def sequential_search(daftar, kata="", mood=""):
    kata = kata.strip().casefold()
    hasil = []

    for lagu in daftar:
        if kata:
            ada_di_judul = kata in lagu["title"].casefold()
            ada_di_artis = kata in lagu["artist"].casefold()
            cocok_kata = ada_di_judul or ada_di_artis
        else:
            cocok_kata = True

        if mood:
            cocok_mood = lagu["mood"].casefold() == mood.casefold()
        else:
            cocok_mood = True

        if cocok_kata and cocok_mood:
            hasil.append(lagu)

    return hasil


def nilai_urut(lagu, kunci):
    """Ambil nilai untuk pembanding sorting (string di-casefold)."""
    nilai = lagu[kunci]
    if isinstance(nilai, str):
        return nilai.casefold()
    return nilai


def bubble_sort(daftar, kunci="title", menurun=False):
    hasil = daftar[:]
    n = len(hasil)

    for i in range(n):
        for j in range(0, n - i - 1):
            a = nilai_urut(hasil[j], kunci)
            b = nilai_urut(hasil[j + 1], kunci)

            if menurun:
                harus_tukar = a < b
            else:
                harus_tukar = a > b

            if harus_tukar:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]

    return hasil


def total_rating_rekursif(daftar, indeks=0):
    if indeks >= len(daftar):
        return 0
    return daftar[indeks]["rating"] + total_rating_rekursif(daftar, indeks + 1)


# ============================================================
# 4. FITUR CRUD, PENCARIAN, SORTING, & STATISTIK
# ============================================================
def tambah_lagu(daftar):
    cetak_header("TAMBAH LAGU BARU (CREATE)")

    judul = sanitasi(input("Judul Lagu : "))
    artis = sanitasi(input("Nama Artis : "))

    if not judul or not artis:
        print(warnai("Judul dan artis tidak boleh kosong!", "RED"))
        return

    if lagu_sudah_ada(daftar, judul, artis):
        print(warnai("Lagu tersebut sudah terdaftar!", "RED"))
        return

    genre = pilih_opsi("Genre", GENRES)
    mood = pilih_opsi("Mood", MOODS)

    rating = parse_rating(input("Rating (1-5) [default 5]: "))
    if rating is None:
        rating = RATING_DEFAULT

    id_terbesar = 0
    for lagu in daftar:
        if lagu["id"] > id_terbesar:
            id_terbesar = lagu["id"]
    id_baru = id_terbesar + 1

    lagu_baru = {
        "id": id_baru,
        "title": judul,
        "artist": artis,
        "genre": genre,
        "mood": mood,
        "rating": rating,
    }
    daftar.append(lagu_baru)
    simpan_lagu(daftar)

    print(warnai(f"Berhasil! '{judul}' disimpan dengan ID #{id_baru}.", "GREEN"))


def pilih_lagu_by_id(daftar, pertanyaan):
    """Minta ID dari user lalu kembalikan lagunya (None kalau tidak ketemu)."""
    id_inp = input(pertanyaan).strip()

    if not id_inp.isdigit():
        return None
    return cari_by_id(daftar, int(id_inp))


def edit_lagu(daftar):
    cetak_header("EDIT DATA LAGU (UPDATE)")
    tampilkan_tabel(bubble_sort(daftar, "id"))

    lagu = pilih_lagu_by_id(daftar, "\nMasukkan ID Lagu yang diedit: ")
    if not lagu:
        print(warnai("Lagu tidak ditemukan.", "RED"))
        return

    print("Kosongkan jika tidak ingin mengubah nilai lama.")

    judul_baru = sanitasi(input(f"Judul [{lagu['title']}]: "))
    if judul_baru:
        lagu["title"] = judul_baru

    artis_baru = sanitasi(input(f"Artis [{lagu['artist']}]: "))
    if artis_baru:
        lagu["artist"] = artis_baru

    if konfirmasi(f"Ubah Genre [{lagu['genre']}]? (y/N): "):
        lagu["genre"] = pilih_opsi("Genre", GENRES)

    if konfirmasi(f"Ubah Mood [{lagu['mood']}]? (y/N): "):
        lagu["mood"] = pilih_opsi("Mood", MOODS)

    rating_baru = parse_rating(input(f"Rating [{lagu['rating']}] (1-5): "))
    if rating_baru is not None:
        lagu["rating"] = rating_baru

    simpan_lagu(daftar)
    print(warnai("Data lagu berhasil diperbarui!", "GREEN"))


def hapus_lagu(daftar):
    cetak_header("HAPUS LAGU (DELETE)")
    tampilkan_tabel(bubble_sort(daftar, "id"))

    lagu = pilih_lagu_by_id(daftar, "\nMasukkan ID Lagu yang dihapus: ")
    if not lagu:
        print(warnai("Lagu tidak ditemukan.", "RED"))
        return

    if konfirmasi(f"Yakin hapus '{lagu['title']}'? (y/N): "):
        daftar.remove(lagu)
        simpan_lagu(daftar)
        print(warnai("Lagu berhasil dihapus!", "GREEN"))


def menu_cari(daftar):
    kata = input("Kata kunci judul/artis (Enter=semua): ")
    mood = pilih_opsi("Filter Mood", MOODS, izinkan_kosong=True)

    hasil = sequential_search(daftar, kata, mood)
    tampilkan_tabel(hasil, "HASIL PENCARIAN")


def menu_urutkan(daftar):
    kriteria = ("title", "artist", "mood", "rating")

    daftar_kriteria = []
    for nomor, nama in enumerate(kriteria, 1):
        daftar_kriteria.append(f"[{nomor}] {nama}")
    print("Urutkan berdasar: " + ", ".join(daftar_kriteria))

    pilihan = input("Pilih (1-4): ").strip()
    if not pilihan.isdigit():
        return

    nomor = int(pilihan)
    if not 1 <= nomor <= len(kriteria):
        return

    menurun = konfirmasi("Urutan Descending (Z->A / 5->1)? (y/N): ")
    hasil = bubble_sort(daftar, kriteria[nomor - 1], menurun)
    tampilkan_tabel(hasil, "HASIL PENGURUTAN")


def cari_dan_urut(daftar):
    cetak_header("CARI & URUTKAN LAGU")
    print("  [1] Cari Lagu (Kata Kunci / Filter Mood)")
    print("  [2] Urutkan Lagu (Bubble Sort Manual)")

    pilihan = input("Pilih (1-2): ").strip()

    if pilihan == "1":
        menu_cari(daftar)
    elif pilihan == "2":
        menu_urutkan(daftar)


def hitung_distribusi_mood(daftar):
    hitung = {}
    for mood in MOODS:
        hitung[mood] = 0

    for lagu in daftar:
        mood = lagu["mood"]
        hitung[mood] = hitung.get(mood, 0) + 1

    return hitung


def hitung_artis_unik(daftar):
    artis_unik = set()
    for lagu in daftar:
        artis_unik.add(lagu["artist"])
    return artis_unik


def ekspor_laporan(daftar, jumlah_artis, rata_rating, hitung_mood):
    with open(FILE_LAPORAN, "w", encoding="utf-8") as file:
        file.write("=== LAPORAN STATISTIK TuneLog ===\n")
        file.write(
            f"Total Lagu: {len(daftar)} | Artis Unik: {jumlah_artis} | "
            f"Rata-rata Rating: {rata_rating:.2f}/5\n\n"
        )

        for mood, jumlah in hitung_mood.items():
            file.write(f"- {mood:<10}: {jumlah} lagu\n")

    print(warnai(f"Laporan disimpan ke {FILE_LAPORAN}", "GREEN"))


def statistik_mood(daftar):
    cetak_header("STATISTIK MOOD & EKSPOR LAPORAN (.txt)")

    if not daftar:
        print(warnai("Koleksi lagu masih kosong.", "YELLOW"))
        return

    artis_unik = hitung_artis_unik(daftar)
    rata_rating = total_rating_rekursif(daftar) / len(daftar)
    hitung_mood = hitung_distribusi_mood(daftar)

    print(f"  Total Lagu       : {len(daftar)} lagu")
    print(f"  Artis Unik       : {len(artis_unik)} artis")
    print(f"  Rata-rata Rating : {rata_rating:.2f} / 5.00 (Rekursif)\n")

    print("Distribusi Mood:")
    maks = max(hitung_mood.values())
    if maks == 0:
        maks = 1

    for mood, jumlah in hitung_mood.items():
        panjang_bar = int((jumlah / maks) * 24)
        bar = "#" * panjang_bar
        persen = jumlah / len(daftar) * 100
        print(
            f"  {mood:<10} | {warnai(bar.ljust(24), 'CYAN')} | "
            f"{jumlah:>2} lagu ({persen:5.1f}%)"
        )

    if konfirmasi("\nEkspor statistik ke 'laporan_musik.txt'? (y/N): "):
        ekspor_laporan(daftar, len(artis_unik), rata_rating, hitung_mood)


# ============================================================
# 5. PROGRAM UTAMA
# ============================================================
MENU_UTAMA = (
    ("1", "Tampilkan Semua Lagu (Read)"),
    ("2", "Tambah Lagu Baru (Create)"),
    ("3", "Cari & Urutkan Lagu (Search & Sort)"),
    ("4", "Edit Data Lagu (Update)"),
    ("5", "Hapus Lagu (Delete)"),
    ("6", "Statistik Mood & Ekspor (.txt)"),
    ("0", "Keluar"),
)


def tampilkan_menu(jumlah_lagu):
    bersihkan_layar()
    cetak_header("TuneLog - MUSIC & MOOD MANAGER", f"Database: songs.txt ({jumlah_lagu} lagu)")

    for kode, keterangan in MENU_UTAMA:
        print(f"  [{warnai(kode, 'CYAN')}] {keterangan}")

    print("=" * LEBAR_LAYAR)


def main():
    if os.name == "nt":
        os.system("")  # Aktifkan dukungan warna ANSI di Windows

    daftar = muat_lagu()

    while True:
        tampilkan_menu(len(daftar))
        pilihan = input("Pilih menu (0-6): ").strip()
        bersihkan_layar()

        if pilihan == "1":
            tampilkan_tabel(bubble_sort(daftar, "id"), "KOLEKSI LAGU BERDASARKAN MOOD")
        elif pilihan == "2":
            tambah_lagu(daftar)
        elif pilihan == "3":
            cari_dan_urut(daftar)
        elif pilihan == "4":
            edit_lagu(daftar)
        elif pilihan == "5":
            hapus_lagu(daftar)
        elif pilihan == "6":
            statistik_mood(daftar)
        elif pilihan == "0":
            print(warnai("Terima kasih telah menggunakan TuneLog!", "GREEN"))
            break
        else:
            print(warnai("Pilihan tidak valid!", "RED"))

        input(warnai("\nTekan [Enter] untuk lanjut...", "CYAN"))


if __name__ == "__main__":
    main()