# Personal Portofolio Website

Nama : **Fadhil Abdurrohman**

NPM : **2506656690**

Kelas : **PBP B**

Website Portofolio pribadi yang dibuat untuk memenuhi Tutorial dan Individual Assignment pada mata kuliah Pemrograman Berbasis Platform (CSGE602022) Ganjil 2026/2027.

Website ini menampilkan ringkasan tentang diri saya, kemampuan, proyek, serta pengalaman dan aktivitas yang pernah saya lakukan.

## Features

- Responsive design
- Responsive Navigation
- Light Mode dan Dark Mode
- Skill, Project, Experience section
- CRUD operations for Skill, Project, and Experience
- JSON API for Skill, Project, and Experience
- Search functionality for Skill, Project, and Experience
- Star and Unstar functionality
- User registration and login
- Session and cookie management
- Guest, Regular User, Editor, SUperuser roles

---

## Tugas Refleksi

- [Tugas refleksi 1](./tugas/tugas1.md)
- [Tugas refleksi 2](./tugas/tugas2.md)
- [Tugas refleksi 3](./tugas/tugas3.md)
- [Tugas refleksi 4](./tugas/tugas4.md)
- [Tugas refleksi 5](./tugas/tugas5.md)
- [Tugas refleksi 6](./tugas/tugas6.md)

### Pertanyaan Reflektif

> 1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!

REST (*Representational State Transfer*) adalah gaya arsitektur untuk merancang komunikasi antara klien dan server. Pada API portofolio saya, URL seperti `/api/v1/skills/<uuid>/` mengidentifikasi satu *resource*, sedangkan metode HTTP menentukan operasi yang dilakukan. Misalnya, `GET` membaca data dan `DELETE` menghapusnya. Mengembalikan JSON saja belum cukup karena JSON hanya menentukan format data. REST juga mengatur cara interaksi berlangsung, misalnya melalui antarmuka yang seragam dan permintaan yang membawa informasi yang diperlukan untuk memprosesnya. `PUT` digunakan ketika ingin mengganti representasi suatu *resource* dengan mengirim seluruh field wajib. Contohnya, untuk mengganti data Skill, saya mengirim nama, ikon, dan URL ke endpoint detailnya. `PATCH` digunakan ketika hanya ingin mengubah sebagian field. Jika saya hanya ingin mengganti nama Skill, saya cukup mengirim `{"name": "Python 3"}` melalui `PATCH`, sehingga ikon dan URL sebelumnya tetap tersimpan.

> 2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?

Serializer memiliki dua peran. Saat membaca data, serializer mengubah objek model menjadi struktur data yang dapat dirender sebagai JSON. Saat menerima input, serializer memvalidasi data sebelum menyimpannya. Sebagai contoh, `ExperienceSerializer` memeriksa apakah tanggal akhir mendahului tanggal mulai, sedangkan `SkillSerializer` menolak nama yang kosong setelah tag HTML dihapus. Dibanding merakit dictionary secara manual dengan `JsonResponse`, serializer memusatkan struktur respons dan aturan validasi di satu tempat. `ModelSerializer` juga dapat mengambil definisi field dari model, sehingga saya tidak perlu mendefinisikan ulang tipe setiap field. Informasi seperti `star_count` dan `is_starred` dapat ditampilkan sebagai field *read-only* karena nilainya dihitung dari data yang tersimpan.

> 3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?

Autentikasi menentukan identitas pengguna yang mengirim request. Dalam proyek ini, `SessionAuthentication` menggunakan sesi login Django untuk mengenali pengguna. Otorisasi menentukan tindakan yang boleh dilakukan oleh pengguna tersebut. Sebagai contoh, Editor dapat mengubah Skill dan Experience melalui `PUT` atau `PATCH`, sementara hanya superuser yang dapat menambah dan menghapus data. Menyembunyikan tombol hanya mengatur apa yang terlihat pada halaman. Pengguna masih dapat mencoba mengirim request langsung ke endpoint. Karena itu, *permission class* harus memeriksa izin pada server agar permintaan yang tidak diizinkan ditolak dengan status `403 Forbidden`.

> 4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?

Ketika API memakai `SessionAuthentication`, browser dapat menyertakan cookie sesi secara otomatis dalam request. Jika situs lain berhasil memicu request yang mengubah data, cookie tersebut dapat membuat request dikenali sebagai milik pengguna yang sedang login. Oleh karena itu, server memeriksa token CSRF. Pada proyek ini, JavaScript mengirim token tersebut melalui header `X-CSRFToken` saat melakukan operasi tulis.  `force_authenticate()` langsung menetapkan identitas pengguna dalam pengujian sehingga proses autentikasi sesi dan pemeriksaan CSRF tidak dijalankan. Untuk menguji perlindungan CSRF, saya menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()` agar request memakai sesi Django. Test memeriksa bahwa request tanpa token ditolak dengan status `403`, sedangkan request dengan token yang diperoleh dari halaman dapat berhasil.

### AI Disclosure

Dalam pengerjaan tugas ini, saya menggunakan bantuan AI (ChatGPT) untuk memahami REST, serializer, autentikasi, otorisasi, dan CSRF, serta memperoleh contoh implementasi dan pengujian API. AI juga membantu untuk membuat beberapa bagian kode, dan kemudian diperiksa secara manual.

[ChatGPT](https://chatgpt.com/share/6af1f0fa-6740-83ec-ae05-52908ea7273b)

### Penggunaan AI

AI digunakan untuk membantu hal-hal berikut.

- Memahami perbedaan `PUT` dan `PATCH`, serta peran serializer, autentikasi, dan *permission class*.
- Menyusun serializer, endpoint CRUD, pencarian, dan star untuk Skill dan Experience.
- Menyesuaikan kode `fetch()` agar dapat membaca respons DRF dan menampilkan pesan validasi melalui toast.
- Menyusun test hak akses, validasi input, star, dan perlindungan CSRF.
- Menemukan penyebab test Project gagal ketika batas validasi tahun 1900–2100 tidak tercantum pada serializer.
- Membantu menjawab pertanyaan reflektif.

Perbaikan manual yang dilakukan meliputi hal-hal berikut.

- Menggabungkan pembuatan API CRUD Skill dan Experience dalam satu commit.
- Memisahkan pengujian Skill dan Experience ke dalam `SkillAPITest` dan `ExperienceAPITest`, mengikuti struktur `ProjectAPITest`.

### Referensi

- [Tutorial 07 — Django REST Framework Implementation](https://pbp.cs.ui.ac.id/tutorial/tutorial-7.html)


---

## Setup Instruction

### Instalasi

1. Clone repository

```bash
git clone https://github.com/fadhilabdurrohman/myportofolio.git
cd myportofolio
```

2. Buat virtual environment

```bash
python -m venv env
```

3. Aktifkan virtual environment

Windows:

```bash
env\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Jalankan migrasi database

```bash
python manage.py migrate
```

6. Buat superuser

```bash
python manage.py create superuser
```

Ikuti instruksi yang diberikan untuk membuat username, email, dan password.

7. Jalankan server

```bash
python manage.py runserver
```

8. Buka melalui browser

```
http://127.0.0.1:8000/
```

9. Akses Django Admin

Untuk mengelola user dan role Editor, buka:

```
http://127.0.0.1:8000/admin/
```

Pada Django Admin, buat Group `Editor` dan masukkan user yang diinginkan ke dalam group tersebut.

11. Pengujian

Gunakan akun dengan _role_ yang sesuai untuk menguji _authentication_, _authorization_, dan fitur Star

- Guest
- Regular User
- Editor
- Superuser

Endpoint JSON dapat diuji melalui:

- `http://127.0.0.1:8000/api/skills/`
- `http://127.0.0.1:8000/api/projects/`
- `http://127.0.0.1:8000/api/experiences/`
