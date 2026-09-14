## Tugas 2

### Pertanyaan Reflektif

> 1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

1. Browser mengirimkan permintaan (_request_) melalui URL tertentu. Kemudian, _request_ ini diterima oleh `urls.py`, yang bertugas mencocokkan pola alamat tersebut untuk menentukan view yang tepat. Kemudain, `views.py` bertindak memproses logika bisnis, jika halaman memerlukan informasi dari database, `views.py` akan memanggil `models.py` untuk memanipulasi data tersebut. `models.py` kemudian mengembalikan data yang dibutuhkan kepada view dalam bentuk objek. Terakhir, view menggabungkan data tersebut ke dalam file Template (`.html`) melalui proses _rendering_, lalu membungkus hasilnya menjadi sebuah *Response HTML* untuk dikirimkan ke browser pengguna

> 2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

2. Data yang disimpan pada moodel lebih mudah untuk diperbarui tanpa mengubah kode template. Hal ini membuat aplikasi mudah dipelihara, dikembangkan, dan dikelola, terutama jika jumlah data bertambah.

> 3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

3. - `makemigrations` adalah tahap persiapan untuk mencatat perubahan pada file `models.py` menjadi file cetak biru baru di folder aplikasi. Perintah ini hanya bekerja di tingkat kode dan tidak mengubah database sama sekali.
- `migrate` adalah tahap eksekusi yang membaca file cetak biru tersebut untuk diterapkan langsung ke database. Perintah inilah yang secara nyata mengubah struktur tabel (seperti membuat atau memodifikasi tabel) di database Anda.

### AI Disclosure

Saya menggunakan ChatGPT dalam membantu saya menyelesaian Individual Assignment ini. Namun, saya tidak menjadikan AI sebagai tools yang menulis kode saya mentah-mentah seluruhnya. Saya jadikan AI sebagai sarana dan media saya **belajar dan bertanya, memberikan contoh kode, referensi, membantu dalam pengerjaan tugas, serta memberikan feedback bagi kode saya**. Dalam Individual Assignment 2 ini, beberapa dibantu oleh Gen AI, seperti desain web dan pembuatan model.

- [Log percakapan ChatGPT](https://chatgpt.com/share/6aa80c04-1d2c-83ec-9ff1-a085276d69e6)
- [Log percakapan ChatGPT 2](https://chatgpt.com/share/6aa80c04-1d2c-83ec-9ff1-a085276d69e6)

### Penggunaan AI

- Membantu memahami struktur MVT Architecture
- Membantu membangun dan mengembangkan model
- Membantu memperbaiki kode JavaScript pada fitur _Dark Theme_
- Membantu memperbaiki dan mengembangkan unit test

## Referensi

[How Django's MVT Architecture Works: A Deep Dive into Models, Views, and Templates - Timothy Olanrewaju](https://www.freecodecamp.org/news/how-django-mvt-architecture-works/)
[Migrations - Django Documentation](https://docs.djangoproject.com/id/6.1/topics/migrations/)
[MTV Django Architecture - Tim Dosen PBP](https://scele.cs.ui.ac.id/pluginfile.php/291223/mod_resource/content/3/03%20-%20MTV%20Django%20Architecture.pdf)