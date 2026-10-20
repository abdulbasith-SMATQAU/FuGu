# FuGu — Future Guidance

Prototipe web untuk membantu pengguna mengenali minat, mengeksplorasi jurusan, melihat kampus contoh, membaca informasi beasiswa, dan memperoleh rekomendasi yang alasannya transparan.

> **Penting:** seluruh universitas, nama beasiswa, kategori biaya, dan isi data pada folder `data/` adalah **contoh/fiktif untuk demo**. Jangan menggunakannya sebagai informasi penerimaan, biaya kuliah, atau beasiswa resmi. Skor rekomendasi hanya mencocokkan preferensi yang dipilih dengan data contoh; aplikasi tidak mengukur bakat dan tidak memprediksi nilai, kelulusan, atau penerimaan.

## Isi proyek

```text
fugu_project/
├── app.py                   # Tampilan dan alur aplikasi Streamlit
├── fugu_logic.py            # Filter data dan aturan skor rekomendasi
├── test_fugu_logic.py       # Pengujian otomatis logika
├── requirements.txt         # Dependensi Python
├── README.md                # Panduan ini
├── .gitignore
├── .streamlit/
│   └── config.toml          # Tema warna Streamlit
└── data/
    ├── programs.json        # Contoh program studi
    ├── universities.json    # Contoh kampus dan atribut lokasi/biaya
    └── scholarships.json    # Contoh informasi beasiswa
```

## Dependensi

- Python 3.10 atau lebih baru disarankan.
- `streamlit` — dipasang dari `requirements.txt`.
- Pengujian logika memakai modul bawaan Python `unittest`; tidak membutuhkan dependensi tambahan.

## Menjalankan dari nol di komputer sendiri

### 1. Pasang Python

Unduh Python dari [python.org](https://www.python.org/downloads/). Saat instalasi Windows, centang opsi **Add Python to PATH** jika tersedia. Buka terminal/Command Prompt baru setelah instalasi.

Periksa instalasi:

```bash
python --version
```

Pada sebagian komputer, perintahnya adalah `python3 --version`.

### 2. Ekstrak proyek

Ekstrak ZIP FuGu, lalu buka folder `fugu_project` di terminal. Pastikan `app.py`, `fugu_logic.py`, `requirements.txt`, dan folder `data/` berada di folder yang sama seperti struktur di atas.

### 3. Buat lingkungan Python terpisah

**Windows — Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Jika aktivasi lingkungan diblokir di komputer tertentu, Anda bisa berkonsultasi dengan panduan resmi Python/Streamlit untuk sistem operasi tersebut; jangan menghapus kebijakan keamanan perangkat kantor/sekolah tanpa izin.

### 4. Instal dependensi

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Jalankan FuGu

Dari folder proyek dan dengan lingkungan `.venv` aktif:

```bash
python -m streamlit run app.py
```

Terminal akan menampilkan alamat lokal. Buka alamat yang ditampilkan (umumnya `http://localhost:8501`) di browser. Terminal perlu tetap berjalan selama aplikasi digunakan. Untuk menghentikan server, tekan `Ctrl+C` di terminal.

## Pengujian

### Status pemeriksaan paket ini

File Python telah diperiksa dengan `compileall`, dan 6 tes otomatis untuk logika data/rekomendasi berhasil dijalankan di lingkungan pembuatan. Antarmuka Streamlit belum dapat dijalankan di lingkungan tersebut karena paket Streamlit tidak terpasang dan unduhan paket terhalang koneksi jaringan. Karena itu, lakukan juga langkah pengujian manual di bawah setelah memasang dependensi di komputer atau setelah deploy.

### Pengujian otomatis logika

Dari folder proyek, jalankan:

```bash
python -m unittest -v test_fugu_logic.py
```

Tes tersebut memeriksa konsistensi hubungan ID data, pencarian/filter program, filter kampus, filter beasiswa, pengurutan skor rekomendasi, rentang skor, dan hasil ketika belum ada minat dipilih.

### Checklist pengujian antarmuka secara manual

1. **Home:** tekan `Mulai Eksplorasi`; halaman berpindah ke bagian `Kenali Dirimu`.
2. **Kenali Dirimu:** coba kirim tanpa memilih minat; pesan validasi harus muncul. Pilih dua minat, lokasi, gaya belajar, lalu tekan `Buat Rekomendasi`; bagian rekomendasi harus terbuka.
3. **Eksplorasi Jurusan:** cari `data`, ubah bidang/jenjang/minat, lalu pastikan jumlah dan hasil berubah. Kosongkan kata pencarian untuk mengembalikan hasil.
4. **Detail Program:** dari kartu jurusan, tekan `Lihat Detail Program`. Coba pilih program lain dari dropdown. Periksa ringkasan, contoh mata kuliah, karier, dan kampus demo.
5. **Universitas Pilihan:** cari kota seperti `Surakarta`; uji filter wilayah, kisaran biaya, dan program. Coba kombinasi yang menghasilkan nol hasil; pesan kosong harus muncul.
6. **Rekomendasi:** periksa skor 0–100 dan buka `Mengapa jurusan ini direkomendasikan?`. Pastikan setiap komponen menunjukkan poin dan alasan. Ubah minat/gaya/lokasi/biaya dan hitung ulang untuk melihat perubahan.
7. **Beasiswa:** cari `kreatif`, ubah sasaran/kategori, buka `Lihat contoh kriteria dan dokumen`, lalu tekan `Tandai untuk dibaca` dan pastikan bagian terkait terbuka setelah aplikasi dirender ulang.
8. **Navigasi:** pindah di antara `Home`, `Eksplorasi`, dan `Beasiswa` berkali-kali. Pastikan tidak ada error terminal dan fungsi pencarian/filter tetap dapat digunakan.

## Mengubah data contoh

Edit JSON di dalam folder `data/`. Pertahankan format JSON dan ID yang konsisten: nilai `program_ids` pada `universities.json` harus cocok dengan `id` pada `programs.json`; `university_ids` pada program juga harus merujuk ID kampus yang ada. Jalankan pengujian otomatis setelah mengubah data.

Untuk penggunaan sungguhan, gantilah data contoh dengan data yang sumber, tanggal pembaruan, lisensi, syarat penggunaan, dan akurasinya jelas. Tambahkan tautan sumber resmi untuk jurusan, institusi, dan beasiswa, serta peninjauan berkala. Jangan memasukkan data pribadi siswa ke repositori publik.

## Publikasi gratis menggunakan GitHub dan Streamlit Community Cloud

### A. Unggah proyek ke GitHub

1. Buat akun atau masuk di [GitHub](https://github.com/).
2. Buat repository baru, misalnya `fugu-future-guidance`. Jika ingin aplikasi terbuka, pilih repository **Public**. Jangan unggah data pribadi, kata sandi, token, atau file rahasia.
3. Dari halaman repository, pilih **Add file → Upload files**. Unggah isi folder proyek (file `app.py` harus berada di root repository, bukan di folder bersarang tambahan). Pastikan folder `.streamlit/` dan `data/` juga ikut terunggah.
4. Isi pesan commit, misalnya `Tambahkan prototipe FuGu`, lalu pilih **Commit changes**.

Alternatif bila Git sudah terpasang: dari folder proyek, jalankan `git init`, `git add .`, `git commit -m "Tambahkan prototipe FuGu"`, lalu hubungkan remote repository GitHub sesuai petunjuk GitHub dan jalankan `git push -u origin main`. Untuk pemula, unggah melalui antarmuka web GitHub biasanya lebih mudah.

### B. Deploy di Streamlit Community Cloud

1. Buka [Streamlit Community Cloud](https://share.streamlit.io/) dan masuk/daftar menggunakan akun GitHub.
2. Pilih **Create app** lalu **Yup, I have an app** jika opsi itu ditampilkan.
3. Pilih repository `fugu-future-guidance`, branch `main`, dan entrypoint file `app.py`.
4. Pada **Advanced settings**, pilih versi Python yang didukung jika diperlukan. Dependensi dibaca dari `requirements.txt`.
5. Tekan **Deploy**. Tunggu proses deploy di halaman layanan hingga log menunjukkan aplikasi tersedia; jika gagal, buka log untuk pesan kesalahan.
6. Setelah berhasil, salin URL `*.streamlit.app` yang diberikan. Uji lagi Home, formulir, filter, detail, dan rekomendasi dari URL publik.

Perubahan yang di-commit dan di-push ke repository biasanya akan diproses ulang oleh Community Cloud. Layanan, batas penggunaan gratis, dan tampilan dashboard dapat berubah; periksa dokumentasi resmi saat deploy.

## Dokumentasi resmi

- [Instalasi Streamlit](https://docs.streamlit.io/get-started/installation)
- [Deploy aplikasi di Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Struktur file aplikasi Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)
