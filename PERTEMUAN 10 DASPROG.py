# Soal 1
def print_triangle_1(n):
    for i in range(n, 0, -1):
        for j in range(i):
            print('*', end='')
        print()
 
 
def print_triangle_2(n):
    for i in range(1, n + 1):
        for j in range(n - i):
            print(' ', end='')
        for j in range(i):
            print('*', end='')
        print()
 
 
def print_triangle_3(n):
    for i in range(n, 0, -1):
        for j in range(n - i):
            print(' ', end='')
        for j in range(i):
            print('*', end='')
        print()
 
 
def print_box_1(tinggi, lebar):
    for i in range(tinggi):
        for j in range(lebar):
            print('*', end='')
        print()
 
 
def print_box_2(tinggi, lebar):
    for i in range(tinggi):
        for j in range(lebar):
            if i == 0 or i == tinggi - 1 or j == 0 or j == lebar - 1:
                print('*', end='')
            else:
                print(' ', end='')
        print()
 

tinggi = int(input('Masukkan tinggi: '))
lebar = int(input('Masukkan lebar (untuk kotak): '))
 
print('\nprint_triangle_1')
print_triangle_1(tinggi)
 
print('\nprint_triangle_2')
print_triangle_2(tinggi)
 
print('\nprint_triangle_3')
print_triangle_3(tinggi)
 
print('\nprint_box_1')
print_box_1(tinggi, lebar)
 
print('\nprint_box_2')
print_box_2(tinggi, lebar)

#Soal 2

def sum_x(x):
    if x < 0:
        return None

    total = 0
    for i in range(x + 1):
        total = total + i
    return total


def sum_x_y(x, y):
    if x > y:
        x, y = y, x

    total = 0
    for i in range(x, y + 1):
        total = total + i
    return total

x = int(input('Masukkan x: '))
y = int(input('Masukkan y: '))

print('sum_x(x)      =', sum_x(x))
print('sum_x_y(x, y) =', sum_x_y(x, y))

#Soal 3

def print_number_triangle(n, start=0):
    angka = start
    for baris in range(1, n + 1):
        for j in range(baris):
            print(angka % 10, end='')
            angka = angka + 1
        print()


print('print_number_triangle(3)')
print_number_triangle(3)

print('\nprint_number_triangle(3, 7)')
print_number_triangle(3, 7)