import numpy as np

# Ubah data menjadi struktur array milik NumPy
A = np.array([10, 20, 30, 40])
B = np.array([1, 2, 3, 4])

# VEKTORISASI: Satu instruksi (+) langsung menyapu seluruh elemen array sekaligus!
hasil = A + B

print("Hasil Vektorisasi:", hasil) 
# Output: [11 22 33 44]