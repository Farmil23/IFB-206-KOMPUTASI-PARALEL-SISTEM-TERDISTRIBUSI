
A = [10, 20, 30, 40]
B = [1, 2, 3, 4]

hasil = []

# Komputer harus mengulang instruksi ini 4 kali (satu per satu)
for i in range(len(A)):
    penjumlahan = A[i] + B[i]
    hasil.append(penjumlahan)

print("Hasil For-Loop:", hasil) 
# Output: [11, 22, 33, 44]