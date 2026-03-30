from multiprocessing import Pool, cpu_count
import time

# Fungsi 'worker' yang mensimulasikan ekstraksi AI pada satu dokumen
def extract_entity(doc_id):
    print(f"  [Thread/Process] Menganalisis dokumen ke-{doc_id}...")
    time.sleep(1.5)  # Simulasi beban kerja CPU (embedding/LLM)
    return f"Data_Entitas_{doc_id}"

if __name__ == "__main__":
    docs = [1, 2, 3, 4, 5]
    print(f"--- Memulai Ekstraksi (OpenMP Style - {cpu_count()} cores) ---")
    
    # Fork: Membagi tugas ke semua core yang tersedia
    # with Pool(cpu_count()) as p:
        # Parallel Work: Semua thread jalan barengan
    last = time.time()
    results = []
    for id in docs:
        final = extract_entity(id)
        results.append(final)
    
    now = time.time() - last
      
    # Join: Menggabungkan hasil kembali ke program utama
    print("\n--- Semua selesai (Join) ---")
    print("Hasil Akhir:", results)
    print("Waktu:" , now)