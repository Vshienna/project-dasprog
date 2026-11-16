jml = int(input("Masukan Jumlah tiket Anda: "))
jmlnew = jml
while jmlnew>0:
    print("=====================================")
    print("Tiket Ke-", jmlnew)
    print("Masukan biodata anda")
    nama = str(input("Nama: "))
    umur = int(input("Umur: "))
    if umur < 5:
       Harga = 0
       ket = "Balita"
    elif umur >= 5 and umur <= 16:
       Harga = 20000
       ket = "Pelajar"
    elif umur >= 17 and umur <= 30:
       Harga = 30000
       ket = "Dewasa"
    if jml>=4:
       HargaNEW = Harga - (Harga * 0.1)
       print("Harga Tiket Anda: Rp.", HargaNEW)
    else:
       HargaNEW = Harga
       print("Harga Tiket Anda: Rp.", Harga)
    print("Kategori:", ket)
    jmlnew -= 1
print("****************************************")
print("Total Harga: Rp.", HargaNEW * (jml))