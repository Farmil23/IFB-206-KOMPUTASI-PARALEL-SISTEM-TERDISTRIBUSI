from multiprocessing import Pool, cpu_count
import time

def ai_agent_task(doc_info):
    doc_id, duration = doc_info
    print(f"  [Worker] Menganalisis Dokumen {doc_id} (Beban: {duration}s)...")
    time.sleep(duration)
    return f"Hasil_{doc_id}"

if __name__ == "__main__":
    # Skenario: 6 Dokumen dengan beban kerja tidak merata (Heterogen)
    # Dokumen 2 sangat berat (4 detik), sisanya ringan (0.5 detik)
    docs = [(1, 0.5), (2, 4.0), (3, 0.5), (4, 0.5), (5, 0.5), (6, 0.5)]
    
    print(f"--- Simulasi Load Balancing pada {cpu_count()} Cores ---\n")

    # --- TEKNIK 1: STATIC SCHEDULING (Chunksize > 1) ---

    print("1. Menjalankan STATIC SCHEDULING (Chunksize=3)...")
    start_static = time.time()
    with Pool(2) as p_static: # Worker 1 dapat (Dok 1,2,3), Worker 2 dapat (Dok 4,5,6)
        p_static.map(ai_agent_task, docs, chunksize=3)
    time_static = time.time() - start_static
    print(f"Total Waktu Static: {time_static:.2f}s\n")

    # --- TEKNIK 2: DYNAMIC SCHEDULING (Chunksize = 1) ---
    print("2. Menjalankan DYNAMIC SCHEDULING (Chunksize=1)...")
    start_dynamic = time.time()
    with Pool(2) as p_dynamic:
        p_dynamic.map(ai_agent_task, docs, chunksize=1)
    time_dynamic = time.time() - start_dynamic
    print(f"Total Waktu Dynamic: {time_dynamic:.2f}s")