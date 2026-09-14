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

## Setup

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
