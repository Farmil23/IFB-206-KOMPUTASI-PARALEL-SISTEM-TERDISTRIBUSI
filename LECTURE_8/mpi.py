from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()   # ID dari proses saat ini
size = comm.Get_size()   # Total proses yang berjalan

data_mentah = None
if rank == 0:
    data_mentah = [i * 12.3 for i in range(size)]
    print(f"\n[Master - Proses {rank}] Data awal yang akan disebar: {data_mentah}\n")
    print("-" * 40)

data_lokal = comm.scatter(data_mentah, root=0)

hasil_lokal = data_lokal + 5
print(f"[Proses {rank}] Menerima data '{data_lokal}', setelah ditambah 5 hasilnya: {hasil_lokal}")

hasil_akhir = comm.gather(hasil_lokal, root=0)

if rank == 0:
    print("-" * 40)
    print(f"\n[Master - Proses {rank}] Hasil akhir setelah dikumpulkan dari semua proses: {hasil_akhir}\n")