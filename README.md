# Personal Portofolio Website

Nama : **Fadhil Abdurrohman**

NPM : **2506656690**

Kelas : **PBP B**

Website Portofolio pribadi yang dibuat untuk memenuhi Tutorial dan Individual Assignment pada mata kuliah Pemrograman Berbasis Platform (CSGE602022) Ganjil 2026/2027.

Website ini menampilkan ringkasan tentang diri saya, kemampuan, proyek, serta pengalaman dan aktivitas yang pernah saya lakukan.

## Features

- Responsive design
- Resonsive Navigation
- Light Mode dan Dark Mode
- Skill, Project, Experience section

## Tugas Refleksi

- [Tugas refleksi 1](./tugas/tugas1.md)
- [Tugas refleksi 2](./tugas/tugas2.md)
- [Tugas refleksi 3](./tugas/tugas3.md)

### Pertanyaan Reflektif

> 1. Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

`ModelForm` digunakan karena dapat membuat form berdasarkan model Django secara otomatis, sehingga validasi dan pengelolaan data menjadi lebih mudah dan konsisten dibandingkan membuat form HTML secara manual. `{% csrf_token %}` wajib digunakan untuk melindungi form dari serangan Cross-Site Request Forgery (CSRF) dengan memastikan permintaan POST berasal dari sumber yang benar.

> 2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

JSON lebih banyak digunakan dalam aplikasi web modern karena sintaksnya lebih sederhana, ukuran datanya relatif kecil, dan mudah diproses oleh berbagai bahasa pemrograman. JSON juga lebih sesuai untuk komunikasi antara _frontend_ dan _backend_ melalui API dibandingkan XML yang memiliki struktur lebih kompleks.

> 3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

Saat _view_ mengembalikan data portofolio dalam bentuk JSON, Django mengambil data dari model, melakukan *serialization* untuk mengubah objek atau _queryset_ Django menjadi struktur data yang dapat direpresentasikan sebagai JSON, lalu mengembalikannya kepada _client_ melalui HTTP response. Serialization diperlukan karena objek model Django tidak dapat langsung dikirim sebagai JSON tanpa terlebih dahulu diubah menjadi format data yang dapat dipahami oleh _client_.

### AI Disclosure

Pengerjaan tugas ini dibantu dengan Gen AI, yaitu ChatGPT dan Claude, sebagai alat bantu dalam memahami konsep dan membantu dalam progres pengerjaan.

- [ChatGPT](https://chatgpt.com/share/6ab13b40-e428-83ec-ac0b-7bfd2eb2c0f8)
- [Claude](https://chatgpt.com/share/6ab13b40-e428-83ec-ac0b-7bfd2eb2c0f8)

### Penggunaan AI

1. Membantu memahami konsep dan penggunaan `ModelForm`
2. Membantu implementasi CRUD Experience dan CRUD Project
3. Membantu perbaikan dan penyusunan HTML/CSS, termasuk desain form, tombol, modal delete, status, dan elemen Experience.

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

6. Jalankan server

```bash
python manage.py runserver
```

7. Buka melalui browser

```
http://127.0.0.1:8000/
```
