import multiprocessing

# Agent 1: Bertugas mencari data (Crawler) di Server A
def agent_crawler(queue):
    data_mentah = "Laporan Keuangan PT. Maju Jaya"
    print(f"Agent Crawler: Menemukan data. Mengirim pesan ke Agent Analyst...")
    # MPI Concept: Mengirim pesan (Message Passing)
    queue.put(data_mentah) 

# Agent 2: Bertugas menganalisis (Analyst) di Server B
def agent_analyst(queue):
    # Menunggu pesan datang dari node lain
    pesan = queue.get()
    print(f"Agent Analyst: Pesan diterima! Menganalisis: '{pesan}'")
    print("Agent Analyst: Analisis selesai.")

if __name__ == "__main__":
    # Channel komunikasi antar proses (seperti kabel jaringan di MPI)
    komunikasi_channel = multiprocessing.Queue()

    # Membuat dua proses yang memiliki memori terpisah
    p1 = multiprocessing.Process(target=agent_crawler, args=(komunikasi_channel,))
    p2 = multiprocessing.Process(target=agent_analyst, args=(komunikasi_channel,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()