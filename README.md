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

## Tugas Refleksi

- [Tugas refleksi 1](./tugas/tugas1.md)
- [Tugas refleksi 2](./tugas/tugas2.md)
- [Tugas refleksi 3](./tugas/tugas3.md)
- [Tugas refleksi 4](./tugas/tugas4.md)

### AI Disclosure

Untuk tugas ini, saya dibantu Ai dalam menyelesaikan beberapa masalah, terkait autentikasi akun.

- [ChatGPT](https://chatgpt.com/share/6aba8c88-b1ec-83ec-bdc9-6076a8c57c29)

### Penggunaan AI

1. Membantu memahami konsep dan implementasi Django, khususnya authentication, session, cookie, authorization, Django Group, dan permission.
2. Membantu menganalisis error dan traceback selama pengembangan, seperti NoReverseMatch, 404 Not Found, OperationalError, dan TimeoutException pada pengujian Selenium.
3. Membantu meninjau dan memperbaiki bagian kode tertentu.

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
