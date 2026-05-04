import time

def simulasi_static_distribution_150():
    # Studi Kasus: Distribusi Request ke Cluster Server Heterogen
    # Server A (High-Spec), Server B (Mid-Spec), Server C (Low-Spec)
    print("=== MONITORING DISTRIBUSI RESOURCE - NRP 150 ===")
    
    tasks = 150  # Total beban kerja berdasarkan NRP
    nodes = {
        "Server_A_High": {"weight": 0.6, "allocated": 0},
        "Server_B_Mid":  {"weight": 0.3, "allocated": 0},
        "Server_C_Low":  {"weight": 0.1, "allocated": 0}
    }
    
    # Menghitung target ideal berdasarkan bobot statis
    targets = {node: int(tasks * data["weight"]) for node, data in nodes.items()}
    
    print(f"Target Distribusi Ideal: {targets}\n")
    print("Memulai proses alokasi task...")
    print("-" * 45)

    # Proses alokasi deterministik
    for i in range(1, tasks + 1):
        if nodes["Server_A_High"]["allocated"] < targets["Server_A_High"]:
            nodes["Server_A_High"]["allocated"] += 1
        elif nodes["Server_B_Mid"]["allocated"] < targets["Server_B_Mid"]:
            nodes["Server_B_Mid"]["allocated"] += 1
        else:
            nodes["Server_C_Low"]["allocated"] += 1
        
        # Cek apakah distribusi ideal telah tercapai (Convergence Point)
        current_alloc = {k: v["allocated"] for k, v in nodes.items()}
        if current_alloc == targets:
            print(f"STEP {i}: [!] IDEAL DISTRIBUTION REACHED")
            break
        
        # Tampilkan log per 30 task untuk efisiensi layar
        if i % 30 == 0:
            print(f"Step {i}: Current State -> {current_alloc}")

    print("-" * 45)
    print("FINAL REPORT (COMPLIANCE CHECK):")
    for node, target in targets.items():
        actual = nodes[node]["allocated"]
        status = "MATCH" if actual == target else "MISMATCH"
        print(f"{node}: Target {target} | Actual {actual} -> {status}")

if __name__ == "__main__":
    simulasi_static_distribution_150()