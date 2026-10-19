# MLOps-GlobalLocalNews

## Project Goal
MLOps-GlobalLocalNews merupakan proyek MLOps untuk menganalisis perubahan perhatian terhadap suatu isu pada berita global dan berita Indonesia.

Proyek ini bertujuan membantu profesional media/content untuk mengidentifikasi isu yang sedang mengalami peningkatan perhatian secara global dan memperkirakan apakah isu tersebut berpotensi mengalami peningkatan perhatian di media Indonesia.

## Machine Learning Task
Task yang digunakan adalah binary classification:

* `0` = perhatian tidak meningkat
* `1` = perhatian meningkat

Primary evaluation metric:

* F1-score

Supporting metrics:

* Accuracy
* Precision
* Recall

## Data Source
Data proyek berasal dari GDELT, yaitu sumber data berita yang bersifat dinamis.

Data diambil secara berkala untuk menangkap perubahan perhatian terhadap isu dari waktu ke waktu.

Topik yang digunakan dalam pengambilan sample data:
* Artificial Intelligence
* Climate Change
* Energy

## Project Structure
```text
MLOps-GlobalLocalNews/
├── .devcontainer/
│   └── devcontainer.json
├── config/
│   └── .gitkeep
├── data/
│   ├── raw/
│   │   └── *.csv
│   └── processed/
│       └── gdelt_articles_processed.csv
├── models/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── src/
│   ├── ingest_data.py
│   └── preprocess.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Directory Description
* `.devcontainer/` untuk konfigurasi lingkungan pengembangan GitHub Codespaces
* `config/` untuk menyimpan file konfigurasi yang digunakan dalam proyek.
* `data/raw/` untuk menyimpan data mentah yang diperoleh dari sumber data.
* `data/processed/` untuk menyimpan data yang telah melalui proses pengolahan.
* `models/` untuk menyimpan model machine learning yang telah dilatih.
* `notebooks/` untuk menyimpan notebook untuk eksplorasi data dan eksperimen.
* `src/` menyimpan source code utama proyek.
* `requirements.txt` berisikan dependency Python yang dibutuhkan proyek.
* `.gitignore` untuk menentukan file atau folder yang tidak perlu dilacak oleh Git.
* `LICENSE` sebagai Lisensi penggunaan dan distribusi proyek.
* `README.md` Dokumentasi utama proyek.

## Development Environment
Proyek menggunakan GitHub Codespaces sebagai lingkungan pengembangan agar konfigurasi Python dan tools yang digunakan dapat dijalankan secara konsisten.

Environment menggunakan:

* Python 3.11
* pandas
* NumPy
* scikit-learn
* Matplotlib
* Seaborn
* Requests

Konfigurasi environment disimpan pada:
.devcontainer/devcontainer.json

Dependency proyek dapat dipasang menggunakan:
pip install -r requirements.txt

## Running the Project with GitHub Codespaces
1. Buka repository MLOps-GlobalLocalNews di GitHub.
2. Pilih tombol Code.
3. Buka tab Codespaces.
4. Pilih Create codespace on `main` atau branch yang ingin digunakan.
5. Tunggu hingga GitHub Codespaces selesai membuat dan menyiapkan environment.
6. Setelah Codespaces terbuka, pastikan Python dapat digunakan dengan perintah: python --version
7. Dependency proyek dapat diperiksa atau dipasang menggunakan: pip install -r requirements.txt
8. Setelah environment siap, proyek dapat dikembangkan melalui terminal, editor, dan notebook yang tersedia di GitHub Codespaces.

## GitHub Flow
Pengembangan proyek menggunakan GitHub Flow. Perubahan dikembangkan pada branch terpisah sebelum digabungkan ke branch `main`.

Branch foundation yang digunakan:
feat/initial-eda

Perubahan pada branch tersebut akan divalidasi terlebih dahulu melalui Pull Request sebelum di-merge ke `main`.

## Data Ingestion
Data ingestion diimplementasikan menggunakan script:
src/ingest_data.py

Script menggunakan GDELT DOC API untuk mengambil artikel berdasarkan query atau kata kunci tertentu. Query dapat diberikan melalui argument --query, sedangkan jumlah maksimum artikel dapat ditentukan melalui --maxrecords. Dengan contoh:
* `python src/ingest_data.py --query "climate change" --maxrecords 5`
* `python src/ingest_data.py --query "energy" --maxrecords 5`
* `python src/ingest_data.py --query "artificial intelligence" --maxrecords 5`

Hasil ingestion disimpan dalam format CSV pada folder:
data/raw/

Nama file menggunakan timestamp waktu ingestion sehingga pengambilan data berikutnya tidak langsung menimpa file sebelumnya. Dengan contoh:
* gdelt_articles_2026-09-28_08-14-14.csv
* gdelt_articles_2026-09-28_08-17-29.csv
* gdelt_articles_2026-09-28_08-18-39.csv

Script dapat dijalankan kembali dengan query dan waktu pengambilan yang berbeda sehingga data hasil ingestion sebelumnya tetap tersimpan.

## Preprocessing
Preprocessing diimplementasikan menggunakan script:
src/preprocess.py

Tahapan preprocessing yang dilakukan:
1. Membaca seluruh file CSV pada data/raw/.
2. Menggabungkan data dari beberapa file raw.
3. Menghapus duplikasi berdasarkan URL artikel.
4. Menghapus baris yang tidak memiliki URL atau judul.
5. Memastikan kolom seendate memiliki format timestamp yang valid.
6. Menyimpan hasil preprocessing ke data/processed/.

Script preprocessing dapat dijalankan menggunakan:
python src/preprocess.py

Hasil preprocessing disimpan pada:
data/processed/gdelt_articles_processed.csv

## Data Versioning with DVC
Dataset pada proyek ini menggunakan DVC (Data Version Control) untuk mengelola perubahan versi dataset dan menjaga reproducibility.

DVC digunakan karena dataset GDELT bersifat dinamis dan dapat berubah ketika proses ingestion dijalankan kembali. Git digunakan untuk menyimpan source code, konfigurasi, dokumentasi, serta file pointer `.dvc`, sedangkan dataset dikelola oleh DVC.

### Inisialisasi DVC
DVC diinisialisasi pada repository dengan:
```bash
dvc init
```

Hasil inisialisasi menghasilkan konfigurasi DVC pada:
```text
.dvc/config
.dvcignore
```

### Menambahkan Dataset ke DVC
Dataset ditambahkan ke DVC menggunakan:
```bash
dvc add data/raw/gdelt_articles_2026-09-28_08-14-14.csv
```

Perintah tersebut menghasilkan file pointer:
```text
data/raw/gdelt_articles_2026-09-28_08-14-14.csv.dvc
```

File `.dvc` disimpan dan di-versioning menggunakan Git, sedangkan isi dataset dikelola oleh DVC.

### Memperbarui Versi Dataset
Ketika isi dataset berubah, dataset dapat ditambahkan kembali menggunakan:
```bash
dvc add data/raw/gdelt_articles_2026-09-28_08-14-14.csv
```

DVC akan menghitung metadata dan hash baru untuk dataset.
Pada demonstrasi versioning, dataset berubah dari 5 artikel pada versi awal menjadi 10 artikel pada versi berikutnya. Hash DVC juga berubah sehingga perubahan dataset dapat dilacak.

Perubahan dapat diperiksa menggunakan:
```bash
dvc status
```

atau:
```bash
dvc diff HEAD
```

Contoh hasil pemeriksaan:
```text
Modified:
    data/raw/gdelt_articles_2026-09-28_08-14-14.csv

files summary: 1 modified
```

### Reproducibility
Versioning dataset memungkinkan perubahan dataset dikaitkan dengan commit Git yang sesuai. Dengan demikian, versi dataset dapat dilacak berdasarkan riwayat perubahan pada file `.dvc`.

Versi awal dataset disimpan pada commit:
```text
65b993c Track initial dataset with DVC
```

Versi berikutnya disimpan pada commit:
```text
4df6cb8 Update dataset version with DVC
```

Hal ini membantu menjaga reproducibility karena perubahan data memiliki metadata dan riwayat versi yang dapat dilacak.

### Catatan Ingestion
Pada pengujian ulang ingestion untuk memperoleh data terbaru, GDELT beberapa kali mengembalikan HTTP 429 (rate limit) dan tidak menghasilkan artikel. Oleh karena itu, demonstrasi perubahan versi menggunakan hasil ingestion GDELT yang telah berhasil dikumpulkan sebelumnya sebagai data tambahan. Pendekatan ini digunakan untuk menunjukkan mekanisme versioning dan lineage DVC tanpa membuat data sintetis.

## Machine Learning dan MLflow

Tahap LK-06 mengembangkan model Machine Learning sesuai dengan rancangan pada LK-01, yaitu binary classification untuk memprediksi apakah perhatian media Indonesia terhadap suatu isu global akan meningkat.

Dataset training menggunakan data timeline volume berita dari GDELT untuk tiga topik: Artificial Intelligence, Climate Change, dan Energy.

Dataset hasil feature engineering disimpan pada `data/processed/lk06_training_dataset.csv`.

### Fitur dan Target

Fitur yang digunakan adalah `global_growth`, `indonesia_growth`, `global_indonesia_ratio`, dan `topic`. Target klasifikasi adalah `label`. Nilai `1` menunjukkan bahwa volume berita Indonesia pada 24 jam berikutnya meningkat minimal 10% dibandingkan periode 24 jam sebelumnya, sedangkan nilai `0` menunjukkan kondisi lainnya.

### Training Model

Model yang digunakan adalah Logistic Regression dengan preprocessing untuk fitur numerik dan kategorikal. Eksperimen dilakukan dengan beberapa variasi nilai hyperparameter `C`:

```bash
python src/train.py --C 0.1
python src/train.py --C 1
python src/train.py --C 10
```

### Integrasi MLflow

MLflow digunakan sebagai sistem manajemen eksperimen untuk mencatat parameter, metric evaluasi, dan model dari setiap eksperimen.

MLflow server dapat dijalankan menggunakan:

```bash
mlflow server --host 0.0.0.0 --port 5000
```

Nama experiment: `LK-06-Global-vs-Local-News`.

Metric yang dicatat adalah Accuracy, Precision, Recall, dan F1-score. F1-score digunakan sebagai metric utama sesuai rancangan LK-01.

### Hasil Eksperimen

| C | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| 0.1 | 0.6667 | 0.3333 | 0.3333 | 0.3333 |
| 1.0 | 0.7500 | 0.5000 | 0.3333 | 0.4000 |
| 10.0 | 0.6667 | 0.4000 | 0.6667 | 0.5000 |

Eksperimen dengan `C=10.0` memberikan hasil terbaik berdasarkan F1-score, yaitu `0.5000`.

### Model Registry

Model terbaik diregistrasikan pada MLflow Model Registry dengan nama `GlobalLocalNewsClassifier` dan tersedia sebagai **Version 1**. Model tersebut berasal dari eksperimen dengan hyperparameter `C=10.0`.

### Reproduktibilitas

Dependency proyek dicatat pada `requirements.txt`, termasuk `mlflow==3.17.1`. File `mlflow.db` dan folder `mlruns/` digunakan sebagai penyimpanan tracking MLflow lokal dan tidak dimasukkan ke Git repository.

### Catatan LK-06

Dataset training merupakan dataset hasil pengolahan timeline GDELT dan digunakan untuk proof of concept. Ukuran dataset relatif terbatas sehingga hasil evaluasi digunakan sebagai hasil eksperimen awal, bukan sebagai klaim performa produksi.
