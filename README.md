# ✈️ Airlines Price Prediction - Flight Fare Analytics

## 📌 Project Overview

Proyek ini dikembangkan oleh **Kelompok 2 - DATALENS** untuk menganalisis dan memprediksi harga tiket pesawat berdasarkan berbagai faktor perjalanan, seperti maskapai penerbangan, rute, waktu keberangkatan, durasi, kelas penerbangan, dan jumlah hari sebelum keberangkatan.

Dengan model prediksi harga tiket pesawat ini, pengguna dan calon penumpang dapat membuat keputusan pemesanan tiket yang lebih efisien dan hemat biaya.

## 👥 Team 

* **Team Name:** DATALENS

* **Project:** Final Project Data Science - Airlines Price Prediction

## 📊 Dataset Information

Dataset yang digunakan diambil dari Kaggle: [Airlines Flights Data](https://www.kaggle.com/datasets/rohitgrewal/airlines-flights-data?utm_source=gemini).

* **Total Records:** 300,153 baris

* **Total Features:** 12 Kolom Utama (+ 1 Feature Engineering)

* **Data Quality:** Tidak ditemukan missing values (0 nulls) maupun duplikasi data.

### Feature Description:

| Nama Kolom | Tipe Data | Deskripsi | 
 | ----- | ----- | ----- | 
| `airline` | Categorical | Nama maskapai penerbangan (misal: Vistara, AirAsia, Indigo, dll.) | 
| `flight` | Categorical | Kode unik penerbangan | 
| `source_city` | Categorical | Kota asal keberangkatan | 
| `departure_time` | Categorical | Waktu keberangkatan (*Morning, Afternoon, Evening*, dll.) | 
| `stops` | Categorical | Jumlah transit (*zero, one, two_or_more*) | 
| `arrival_time` | Categorical | Waktu kedatangan di kota tujuan | 
| `destination_city` | Categorical | Kota tujuan akhir | 
| `class` | Categorical | Kelas penerbangan (*Economy* vs *Business*) | 
| `duration` | Numerical | Total durasi penerbangan (dalam jam) | 
| `days_left` | Numerical | Jumlah hari tersisa dari tanggal pemesanan ke keberangkatan | 
| `price` | Numerical | **Target Variable**: Harga tiket pesawat | 
| `route` | Categorical | *Engineered Feature*: Rute perjalanan (`source_city` $\rightarrow$ `destination_city`) | 

## 📈 Exploratory Data Analysis (EDA) Highlights

Beberapa temuan penting dari tahapan EDA awal:

1. **Dampak Kelas Penerbangan:** Terdapat perbedaan harga yang sangat signifikan antara kelas *Business* dan *Economy*, di mana tiket kelas *Business* mendominasi kisaran harga tertinggi.

2. **Efek Waktu Pemesanan (`days_left`):** Harga tiket cenderung melambung tinggi ketika pemesanan dilakukan dalam waktu dekat (kurang dari 10-14 hari sebelum keberangkatan).

3. **Pengaruh Rute dan Durasi:** Rute penerbangan antar kota besar serta penerbangan dengan transit (*one-stop*) memiliki variasi durasi dan rentang harga yang beragam.

## 🛠️ Workflow & Methodology

1. **Data Cleaning & Preprocessing:**

   * Pengecekan data hilang (*missing values*) dan duplikasi.

   * Pembersihan kolom indeks/variabel redundant.

   * *Feature Engineering* (pembuatan kolom `route`).

2. **Feature Encoding & Scaling:**

   * Encoding untuk variabel kategorikal (`One-Hot Encoding` / `Ordinal Encoding`).

   * Normalisasi/Standarisasi untuk variabel numerik (`duration`, `days_left`).

3. **Machine Learning Modeling:**

   * Pengujian beberapa algoritma regresi (misal: *Linear Regression, Random Forest Regressor, XGBoost, LightGBM*).

   * Evaluasi performa model menggunakan metrik **MAE, RMSE,** dan $R^2$ **Score**.

## 🚀 How to Run

1. Clone repositori ini:

   ```
   git clone https://github.com/yahyaabdulloh28/project_airflight.git
   
   ```

2. Masuk ke direktori proyek:

   ```
   cd airlines-price-prediction
   
   ```

3. Install dependensi yang dibutuhkan:

   ```
   pip install -r requirements.txt
   
   ```

4. Buka file notebook menggunakan Jupyter Notebook atau Google Colab:

   ```
   jupyter notebook "final_project_ds_datalens.ipynb"
   
   ```

## 🛠️ Tech Stack & Libraries

* **Language:** Python

* **Data Manipulation:** Pandas, NumPy

* **Data Visualization:** Matplotlib, Seaborn

* **Machine Learning:** Scikit-Learn, XGBoost, LightGBM
