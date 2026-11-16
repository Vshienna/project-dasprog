#Soal 1
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def deret_fibonacci(batas, i=0):
    print(fibonacci(i), end=' ')
    if i < batas - 1:
        deret_fibonacci(batas, i + 1)
jumlah = int(input('Mau tampilkan berapa angka fibonacci? '))
deret_fibonacci(jumlah)
print()

#Soal 2
def pangkat(a, b):
    if b == 0:
        return 1
    return a * pangkat(a, b - 1)

angka = int(input('Masukkan angka: '))
eksponen = int(input('Masukkan pangkat (0 atau lebih): '))

print(f'{angka} pangkat {eksponen} = {pangkat(angka, eksponen)}')

#Soal 3
def faktorial(n):
    if n <= 1:
        return 1
    return n * faktorial(n - 1)
angka = int(input('Masukkan angka: '))

print(f'{angka}! = {faktorial(angka)}')

#Soal 4
def maksimum(data, i=0):
    if i == len(data) - 1:
        return data[i]
    max_sisa = maksimum(data, i + 1)
    if data[i] > max_sisa:
        return data[i]
    else:
        return max_sisa

def minimum(data, i=0):
    if i == len(data) - 1:
        return data[i]
    min_sisa = minimum(data, i + 1)

    if data[i] < min_sisa:
        return data[i]
    else:
        return min_sisa

angka = [4, 17, 2, 9, 25, 1, 8]

print('Data     :', angka)
print('Maksimum :', maksimum(angka))
print('Minimum  :', minimum(angka))
