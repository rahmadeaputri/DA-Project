# Dicoding-DA-Project

## Analisis Data Penyewaan Sepeda

### Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda untuk mengidentifikasi pola penggunaan, faktor-faktor yang memengaruhi jumlah penyewaan, serta perbedaan perilaku pengguna berdasarkan waktu, cuaca, dan tipe pengguna. Melalui analisis ini, diharapkan dapat memberikan insight yang berguna untuk pengambilan keputusan strategis seperti pengelolaan armada sepeda, promosi yang tepat sasaran, dan peningkatan layanan pelanggan.

### Tujuan Proyek
1. Memahami pola waktu penggunaan sepeda: Mengidentifikasi jam-jam penggunaan tertinggi berdasarkan musim dan kondisi cuaca.
2. Mengukur pengaruh cuaca dan suhu: Melihat bagaimana kondisi cuaca dan suhu memengaruhi tingkat penyewaan.
3. Membandingkan perilaku pengguna terdaftar dan kasual: Analisis pola penggunaan pada hari kerja, akhir pekan, dan hari libur.
4. Mengidentifikasi faktor yang paling memengaruhi penyewaan: Menggunakan korelasi untuk menemukan faktor dominan.
5. Segmentasi pengguna berbasis RFM (Recency, Frequency, Monetary): Memahami kontribusi pengguna berdasarkan intensitas dan waktu penyewaan.

### Data yang Digunakan
Dataset yang digunakan mencakup informasi sebagai berikut. 
- Dataset day berisi penggunaan sepeda per-hari
- Dataset hour berisi penggunaan sepeda per-jam
- Dataset ini terdiri dari beberapa fields dengan penjelasan sebagai berikut : 
    1. instant -> indeks atau nomor urut untuk setiap catatan dalam dataset 
    2. dteday -> tanggal penyewaan sepeda dg format (yyyy-mm-dd)
    3. season -> musim penyewaan (1: semi, 2: panas, 3: gugur, 4: dingin)
    4. yr -> tahun penyewaan (0: 2011, 1:2012)
    5. mnth -> bulan penyewaan (1-12)
    6. holiday -> menunjukkan hari libur/tidak (1: libur, 0: Bukan hari libur)
    7. weekday -> hari dalam seminggu (0: minggu, 1: senin, dst )
    8. workingday -> hari kerja/tidak (0: bukan hari kerja, 1: hari kerja)
    9. weathershit -> kode kondisi cuaca (1: cerah, 2: berawan + kabut, 3: hujan/rintik, 4:hujan berat + salju)
    10. temp -> suhu dalam celcius (skala 0-1)
    11. atempt -> suhu terasa dalam celcius (0-1)
    12. hum -> kelembapan (skala 0-1)
    13. windspeed -> kecepatan angin (skala 0-1)
    14. casual -> jumlah pengguna kasual yang menyewa sepeda 
    15. registered -> jumlah pengguna terdaftar yang menyewa sepeda
    16. cnt -> total jumlah penyewa sepeda(casual + registered)
    17. hr -> jam penyewaan (0-23) **hanya tersedia di hour.csv

### Analisis dan Visualisasi
1. Pola Penggunaan Berdasarkan Waktu
    Menggunakan heatmap untuk memvisualisasikan rata-rata penyewaan sepeda berdasarkan jam, musim, dan kondisi cuaca. Insight utama:
    - Musim gugur memiliki jumlah penyewaan tertinggi.
    - Penggunaan sepeda memuncak pada sore hari (jam 17:00) di hampir semua musim.

2. Pengaruh Cuaca dan Suhu
    Menggunakan scatter plot dengan kategori cuaca untuk memahami hubungan suhu dan kondisi cuaca dengan penyewaan. Insight utama:
    - Penyewaan meningkat seiring kenaikan suhu hingga batas tertentu.
    - Cuaca cerah memiliki tingkat penyewaan tertinggi, sementara hujan lebat menurunkan penyewaan secara signifikan.

3. Perilaku Pengguna Terdaftar vs Kasual
    Menggunakan bar chart untuk menganalisis perilaku berdasarkan tipe hari:
    - Pengguna terdaftar lebih dominan pada hari kerja.
    - Pengguna kasual mendominasi saat hari libur.

4. Faktor yang Mempengaruhi Penyewaan
    Menggunakan heatmap korelasi untuk menemukan hubungan antara fitur seperti suhu, kelembapan, dan kondisi cuaca dengan jumlah penyewaan. Faktor dominan:
    - Suhu memiliki korelasi positif yang kuat terhadap penyewaan.
    - Kelembapan memiliki korelasi negatif yang lemah.

5. Segmentasi Pengguna dengan RFM
    Mengelompokkan pengguna ke dalam High-Value, Medium-Value, dan Low-Value Users berdasarkan analisis RFM. Insight:
    - High-value users sebagian besar adalah pengguna terdaftar.
    - Pengguna kasual cenderung berada pada segmen medium atau low value.

### Teknologi yang Digunakan
- Python : Analisis daya dan visualisasi
- Streamlit : Dashboard
- Library : 
    - Pandas dan Numpy untuk manipulasi data.
    - Matplotlib dan seaborn untuk visualisasi.

### Cara Menggunakan 

#### Setup Environment - Shell/Terminal

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install 

#### Run streamlit app
streamlit run dashboard.py
