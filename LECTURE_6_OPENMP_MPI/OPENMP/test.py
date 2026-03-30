from multiprocessing import Pool, cpu_count
import time
import random

def extract_entity(doc_id):
    beban = random.uniform(1, 5) 
    print(f"  [Worker] Dokumen {doc_id} butuh waktu {beban:.2f}s")
    time.sleep(beban)
    return f"Hasil_{doc_id}"

if __name__ == "__main__":
    docs = [1, 2, 3, 4, 5]
    print(f"--- Memulai Ekstraksi (OpenMP Style - {cpu_count()} cores) ---")

    last = time.time()
  
    with Pool(8) as p:
        results = p.map(extract_entity, docs) 
    
    now = time.time() - last
      
    print("\n--- Semua selesai (Join) ---")
    print("Hasil Akhir:", results)
    print("Waktu:" , now)