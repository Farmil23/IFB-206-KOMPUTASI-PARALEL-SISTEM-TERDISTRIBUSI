import os
import time
from multiprocessing import Pool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
# ==========================================
# 1. SETUP: Membuat "Different Data"
# ==========================================
def create_rag_documents():
    """Membuat 4 dokumen konteks yang berbeda (Different Data)"""
    docs = {
        "export_ai_compliance.txt": "Regulasi ekspor UMKM memerlukan validasi dokumen kepatuhan secara ketat menggunakan vision extraction dan penalaran terstruktur. ",
        "scholarsync_journals.txt": "Pengindeksan dokumen saintifik dalam format PDF dapat dianalisis secara semantik untuk membantu asisten peneliti melakukan tinjauan pustaka otonom. ",
        "graphweaver_docs.txt": "Investigasi forensik digital memanfaatkan autonomous knowledge graph builder yang didukung oleh database graf dan multi-agent workflow. ",
        "farmile_portfolio.txt": "Portofolio pengembangan sistem automasi pertanian mencakup berbagai integrasi sensor dan pemetaan area operasional untuk efisiensi lahan. "
    }
    
    file_paths = []
    for filename, content in docs.items():
        # Memperbanyak teks agar chunking process lebih realistis
        with open(filename, "w", encoding="utf-8") as f:
            f.write((content + "\n") * 100)
        file_paths.append(filename)
    return file_paths

# ==========================================
# 2. THE SAME TASK (Tugas Paralel)
# ==========================================
def process_single_document(file_path):
    """
    TUGAS YANG SAMA: Setiap proseser memuat satu dokumen dan memecahnya menjadi chunks.
    Ini adalah CPU-bound task yang sangat cocok untuk Data Parallelism.
    """
    process_id = os.getpid()
    print(f"[Worker PID: {process_id}] Memulai ingestion data pada: {file_path}")
    
    # Load dan Split
    loader = TextLoader(file_path, encoding="utf-8")
    document = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=80)
    chunks = text_splitter.split_documents(document)
    
    time.sleep(3) # Simulasi komputasi berat agar paralelisasi terlihat di log
    print(f"[Worker PID: {process_id}] Selesai memproses {file_path} -> {len(chunks)} chunks.")
    
    return chunks

# ==========================================
# 3. MAIN EXECUTION (Data Parallelism)
# ==========================================
def parallel_retrieve_docs():
    file_paths = create_rag_documents()
    print("=== MEMULAI PARALLEL DOCUMENT INGESTION ===")
    start_time = time.time()
    
    # Menjalankan Data Parallelism dengan 4 CPU cores
    with Pool(processes=8) as pool:
        # pool.map mendistribusikan Task yang SAMA ke Data yang BERBEDA
        parallel_results = pool.map(process_single_document, file_paths)
    
    # Menggabungkan hasil dari semua worker menjadi satu list (flatten list)
    all_chunks = [chunk for sublist in parallel_results for chunk in sublist]
    end_time = time.time()
    
    print(f"\nTotal waktu eksekusi Sekuensial: {end_time - start_time:.4f} detik")
    print(f"Total chunks dari semua dokumen: {len(all_chunks)}")
    print("Membangun FAISS Vectorstore...\n")
    
    # Embeddings (Memasukkan semua chunk ke dalam FAISS)
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents=all_chunks, embedding=embedding)
    
    # Bersihkan file sementara
    for file in file_paths:
        if os.path.exists(file):
            os.remove(file)
            
    return vectorstore.as_retriever()

def sequential_retrieve_docs():
    file_paths = create_rag_documents()
    print("=== MEMULAI PARALLEL DOCUMENT INGESTION ===")
    start_time = time.time()
    
    # Menjalankan Data Parallelism dengan 4 CPU cores
    with Pool(processes=1) as pool:
        # pool.map mendistribusikan Task yang SAMA ke Data yang BERBEDA
        parallel_results = pool.map(process_single_document, file_paths)
    
    # Menggabungkan hasil dari semua worker menjadi satu list (flatten list)
    all_chunks = [chunk for sublist in parallel_results for chunk in sublist]
    end_time = time.time()
    
    print(f"\nTotal waktu eksekusi paralel: {end_time - start_time:.4f} detik")
    print(f"Total chunks dari semua dokumen: {len(all_chunks)}")
    print("Membangun FAISS Vectorstore...\n")
    
    # Embeddings (Memasukkan semua chunk ke dalam FAISS)
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents=all_chunks, embedding=embedding)
    
    # Bersihkan file sementara
    for file in file_paths:
        if os.path.exists(file):
            os.remove(file)
            
    return vectorstore.as_retriever()
# Eksekusi untuk dites di Notebook
if __name__ == '__main__':
    # Kamu bisa mengganti 'retriever = retrieve_docs()' di cell 30 dengan ini:
    retriever = parallel_retrieve_docs()