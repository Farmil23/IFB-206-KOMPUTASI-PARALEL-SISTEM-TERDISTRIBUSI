import multiprocessing
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


llm = ChatGroq(model_name = "llama3-70b-8192", api_key = API_KEY) 

def proses_satu_cv(teks_cv):
    pid = os.getpid()
    print(f"[Core PID: {pid}] Mulai embedding untuk: '{teks_cv}'...")
    
    embedder = OpenAIEmbeddings() 
    hasil = embedder.embed_query(teks_cv)
    
    print(f"[Core PID: {pid}] SELESAI embedding untuk: '{teks_cv}'")
    return hasil

def agen_simd_hr_assistant_multiprocessing(daftar_cv):
    print(f"Memproses (SIMD) {len(daftar_cv)} CV menggunakan multiprocessing...")
    
    jumlah_core = multiprocessing.cpu_count()
    print(f"Menggunakan {jumlah_core} core CPU.\n" + "-"*40)

    with multiprocessing.Pool(processes=jumlah_core) as pool:
        hasil_embedding = pool.map(proses_satu_cv, daftar_cv)
        
    return hasil_embedding

if __name__ == '__main__':
    waktu_mulai = time.time()

    ratusan_cv = [
        "Teks CV Kandidat 1 - Software Engineer...", 
        "Teks CV Kandidat 2 - Data Scientist...", 
        "Teks CV Kandidat 3 - Product Manager...",
        "Teks CV Kandidat 4 - UI/UX Designer...",
        "Teks CV Kandidat 5 - DevOps Engineer..."
    ] 
    
    hasil = agen_simd_hr_assistant_multiprocessing(ratusan_cv)

    waktu_eksekusi = time.time() - waktu_mulai
    
    print("-" * 40)
    print(f"--- WAKTU EKSEKUSI : {waktu_eksekusi:.2f} detik ---")
    print(f"Selesai! Berhasil membuat {len(hasil)} vektor embedding.")