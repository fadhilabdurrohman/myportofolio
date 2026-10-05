## Tugas 5

### Pertanyaan Reflektif

> 1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

1. Debouncing adalah teknik untuk menunda eksekusi fungsi sampai pengguna berhenti melakukan input selama waktu tertentu, misalnya 300 ms. Pada pencarian AJAX, debouncing penting agar `fetch()` tidak dikirim setiap kali satu karakter diketik, sehingga mengurangi jumlah request ke server dan membuat aplikasi lebih efisien.

> 2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

2. `await` digunakan untuk menunggu Promise selesai sebelum melanjutkan ke baris berikutnya. Contoh:

```
const response = await fetch(url);
const data = await response.json();
```

Tanpa `await`, variabel `response` masih berupa `Promise`, bukan hasil respons server, sehingga data belum bisa langsung digunakan.

> 3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

3. *XSS (Cross-Site Scripting)* adalah serangan dengan menyisipkan kode JavaScript/HTML berbahaya ke dalam halaman web. Data dari AJAX lebih rentan jika langsung dimasukkan menggunakan `innerHTML`, karena browser dapat menganggap input tersebut sebagai HTML yang harus dieksekusi. Django template secara default melakukan auto-escaping, sedangkan saat membuat HTML lewat JavaScript kita harus melakukan escaping sendiri, misalnya dengan `escapeHtml()`.

### AI Disclosure

Dalam pengerjaan tugas ini, saya menggunakan bantuan AI (ChatGPT) untuk membantu memahami konsep AJAX, debouncing, XSS, serta memberikan saran implementasi, debugging, dan perbaikan kode.

[ChatGPT]()

### Penggunaan AI

AI digunakan untuk membantu:
- Memahami konsep AJAX, `fetch()`, debouncing, CSRF, toast, dan XSS.
- Menyusun implementasi AJAX `fetch()` untuk menampilkan data.
- Membantu pembuatan AJAX create, star/unstar, delete, dan update.
- Membantu penerapan debouncing, toast, CSRF, dan proteksi XSS.
- Membantu debugging error JavaScript dan alur request AJAX.
- Membantu menjawab pertanyaan reflektif.

Perbaikan manual yang dilakukan:
- Mengembalikan struktur HTML/CSS ketika saran AI sempat mengubah tampilan.
- Memperbaiki referensi URL/variabel AJAX yang tidak sesuai.
- Mengubah star/delete agar tidak me-render ulang seluruh daftar sehingga scroll tidak berpindah.
- Mengganti native `confirm()` dengan custom modal agar konsisten dengan UI.
- Menyesuaikan kode dengan permission, struktur project, dan checklist resmi Tugas 5.
- Menguji ulang fitur pada browser dan memastikan tidak ada error.

### Referensi

- [MDN Web Docs - How to use promises](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS/Promises)
- [OWASP - Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)