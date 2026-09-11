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
Data proyek direncanakan berasal dari GDELT, yaitu sumber data berita yang bersifat dinamis.

Data akan diambil secara berkala untuk menangkap perubahan perhatian terhadap isu dari waktu ke waktu.

## Project Structure
MLOps-GlobalLocalNews/
├── .devcontainer/
│   └── devcontainer.json
├── config/
│   └── .gitkeep
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── models/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── src/
│   └── .gitkeep
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt


### Directory Description
`.devcontainer/` untuk konfigurasi lingkungan pengembangan GitHub Codespaces
`config/` untuk menyimpan file konfigurasi yang digunakan dalam proyek.
`data/raw/` untuk menyimpan data mentah yang diperoleh dari sumber data.
`data/processed/` untuk menyimpan data yang telah melalui proses pengolahan.
`models/` untuk menyimpan model machine learning yang telah dilatih.
`notebooks/` untuk menyimpan notebook untuk eksplorasi data dan eksperimen. 
`src/` menyimpan source code utama proyek.
`requirements.txt` berisikan dependency Python yang dibutuhkan proyek.
`.gitignore` untuk menentukan file atau folder yang tidak perlu dilacak oleh Git. 
`LICENSE` sebagai Lisensi penggunaan dan distribusi proyek.
`README.md` Dokumentasi utama proyek. 

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
