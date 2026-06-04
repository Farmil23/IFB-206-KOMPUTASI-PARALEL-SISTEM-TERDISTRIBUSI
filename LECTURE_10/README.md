# CuffnCode — Mini Project (Komputasi Paralel & Sistem Terdistribusi)

Mini project untuk mata kuliah **Komputasi Paralel dan Sistem Terdistribusi** (IFB 206), berbasis proyek open-source [CuffnCode](https://github.com/Student-Embedded-Control-and-AI-Fest/CuffnCode): sistem pengukuran tekanan darah retrofit untuk pengajaran dan riset.

| Dokumentasi lengkap (GitHub Pages) | [Buka docs/index.md](./docs/index.md) setelah Pages diaktifkan |
| Referensi desain | [Obsidian — CuffnCode](https://publish.obsidian.md/auralius/Published/CuffnCode) |
| Laporan akhir | [LAPORAN_AKHIR.md](./LAPORAN_AKHIR.md) |
| Video demo | [VIDEO_DEMO_SCRIPT.md](./VIDEO_DEMO_SCRIPT.md) |

---

## Pelaksana

| Nama | NRP | Kelas | Institusi |
|------|-----|-------|-----------|
| **Farhan Kamil Hermansyah** | 152024150 | CC | Institut Teknologi Nasional (ITENAS) |

Seluruh pengembangan mini project ini — simulasi software, GUI, pipeline paralel & terdistribusi, dokumentasi, dan integrasi repositori — **dikerjakan oleh Farhan Kamil Hermansyah**.

---

## Masalah yang diselesaikan

| Masalah | Konteks CuffnCode | Solusi dalam mini project |
|---------|-------------------|---------------------------|
| **Sinyal cuff lemah & berisik** | Output bridge MPS20N0040D berorde mV; hum **50 Hz** mengganggu estimasi oscillometric | Generator sinyal sintetis + filter **notch 50 Hz** dan **moving average**; perbandingan **SEBELUM vs SESUDAH** di GUI |
| **Beban komputasi filter besar** | Batch ADC menghasilkan ribuan sample yang harus difilter cepat di Host PC | **Komputasi paralel** — data parallelism dengan `multiprocessing.Pool` pada chunk waveform |
| **Subsistem terpisah secara fisik/logis** | Acquisition (STM32/ADC), pemrosesan (Host), dan penyimpanan/UI tidak satu proses monolitik | **Sistem terdistribusi** — 3 node logis (A → B → C) dengan **message passing** (`Queue`) |
| **Demo tanpa hardware di meja** | Tugas menekankan komputasi, bukan fabrikasi PCB | **Simulator desktop (GUI)** + pipeline terminal; spesifikasi hardware mengacu dokumentasi resmi CuffnCode |
| **Dokumentasi & penilaian EVALUASI 3** | Repo GitHub + GitHub Pages + video 20–30 detik | Folder `docs/`, `Host-Simulation/`, skrip video, dan panduan deploy Pages |

---

## Tujuan

| No | Tujuan |
|----|--------|
| 1 | Mensimulasikan alur pengukuran oscillometric (pump → valve → sensor → AFE → STM32 → Host) **sepenuhnya di software** |
| 2 | Menerapkan **komputasi paralel** (data parallelism) pada pemfilteran sinyal dan menunjukkan **speedup** sequential vs parallel |
| 3 | Mensimulasikan **sistem terdistribusi** tiga node: Acquisition → Processing → Storage dengan pola message passing |
| 4 | Menyediakan **GUI** untuk demonstrasi dan analisis pengaruh filter (metrik hum, noise, peak) |
| 5 | Mendokumentasikan kontribusi di **GitHub** dan **GitHub Pages** sesuai EVALUASI 3 IFB 206 |
| 6 | Menyediakan materi **video demo** 20–30 detik (Instagram Lab) |

---

## Apa yang dikerjakan

1. **Simulasi komputasi paralel** — pipeline filter sinyal cuff (data parallelism, benchmark speedup)  
2. **Simulasi sistem terdistribusi** — 3 node: Acquisition → Processing → Storage  
3. **GUI Host-Simulation** — diagram alur hardware + grafik sinyal sebelum/sesudah filter  
4. **GitHub documentation** — README, `docs/` untuk GitHub Pages, folder `Host-Simulation/`  
5. **Video Instagram 20–30 detik** — skrip di `VIDEO_DEMO_SCRIPT.md`

---

## Struktur folder

```
LECTURE_10/
├── gui.py                  # Simulator desktop (utama)
├── main.py                 # Entry point: demo terminal
├── requirements.txt
├── README.md
├── LAPORAN_AKHIR.md
├── VIDEO_DEMO_SCRIPT.md
├── Host-Simulation/        # Salinan untuk push ke fork CuffnCode
├── docs/                   # Sumber GitHub Pages
│   ├── index.md
│   └── _config.yml
└── src/
    ├── signal_generator.py # Waveform sintetis (tanpa hardware)
    ├── signal_analysis.py  # Metrik sebelum/sesudah filter
    ├── filters.py          # Moving avg + notch 50 Hz
    ├── parallel_pipeline.py
    └── distributed_nodes.py
```

---

## Cara menjalankan

### GUI (simulasi hardware + grafik sinyal) — disarankan

```powershell
cd "LECTURE_10"
pip install -r requirements.txt
python gui.py
```

Klik **Mulai Simulasi** untuk melihat alur: pump → valve → sensor → AFE → STM32 → paralel → distributed.

Panel tengah menampilkan **detail teknis** sesuai [repo CuffnCode](https://github.com/Student-Embedded-Control-and-AI-Fest/CuffnCode): spesifikasi MPS20N0040D, rumus gain AD620 (`G = 1 + 49.4k/Rg`), offset TLC2272, STM32F411CE, notch 50 Hz, safety notes, dan roadmap proyek.

### Terminal (benchmark angka)

```powershell
python main.py
```

Output yang diharapkan:

- Perbandingan waktu **sequential vs parallel** (speedup)
- Log **3 node terdistribusi** (A → B → C)
- Estimasi BP demo (bukan medis)

---

## Kaitan dengan CuffnCode (hardware)

| Komponen CuffnCode | Peran | Implementasi di mini project |
|--------------------|-------|------------------------------|
| MPS20N0040D | Sensor tekanan cuff | `signal_generator.py` (waveform sintetis) |
| AD620 + TLC2272 | AFE, gain & offset | Dijelaskan di `docs/index.md` + telemetri GUI |
| STM32F411CE | Kontrol & ADC | Diwakili Node A (acquisition) |
| Notch 50/60 Hz | Roadmap filter | `filters.notch_50hz()` |
| Pump + 2 valve | Inflate/deflate | Diagram arsitektur di GUI |

---

## Komputasi paralel (Komputasi Paralel & Sistem Terdistribusi)

**Konsep:** *Data parallelism* — satu fungsi task (`process_chunk`) diterapkan ke banyak potongan data (chunk waveform) secara bersamaan, mirip pola SIMD dan studi kasus di kuliah (`LECTURE_6` load balancing, `LECTURE_7`).

**Mengapa paralel di sini?** Filter notch + moving average pada ribuan sample bersifat **embarrassingly parallel**; pembagian chunk memungkinkan pemanfaatan semua core CPU Host.

**Implementasi:**

```python
with Pool(cpu_count()) as pool:
    pool.map(process_chunk, tasks, chunksize=1)  # dynamic scheduling
```

**Output penilaian:** perbandingan waktu sequential vs parallel + faktor **speedup** di `main.py` dan log GUI.

---

## Sistem terdistribusi (Komputasi Paralel & Sistem Terdistribusi)

**Konsep:** Subsistem CuffnCode dipetakan ke **tiga node logis** yang berkomunikasi lewat **message passing** (bukan shared memory global), selaras dengan cluster/MPI di `LECTURE_9`.

| Node | Peran dalam CuffnCode | Mekanisme simulasi |
|------|------------------------|-------------------|
| **A — Acquisition** | STM32 + ADC mengirim batch sample | `Queue.put(samples)` |
| **B — Processing** | Host memfilter & ekstrak fitur | Filter + peak per batch |
| **C — Storage / UI** | Agregasi hasil & estimasi BP demo | Konsumsi antrian hasil |

Alur: **A → B → C** dengan thread terpisah per node, mendemonstrasikan latency antar-tahap dan pemisahan tanggung jawab subsistem.

---

## Aktifkan GitHub Pages

1. Push folder `LECTURE_10` (atau repo terpisah) ke GitHub  
2. **Settings → Pages → Build from branch**  
3. Branch: `main`, folder: `/docs`  
4. URL: `https://<username>.github.io/<repo>/`

Detail: [GITHUB_PAGES_SETUP.md](./GITHUB_PAGES_SETUP.md)

---

## Kredit

- [CuffnCode — Student Embedded Control and AI Fest](https://github.com/Student-Embedded-Control-and-AI-Fest/CuffnCode) (IFAC Activity Fund)
- [System design notes](https://publish.obsidian.md/auralius/Published/CuffnCode)
- Mata kuliah IFB 206 — Komputasi Paralel, Institut Teknologi Nasional
