# ChefMate – AI Cooking Assistant 🍳

ChefMate adalah chatbot berbasis Large Language Model (LLM) yang
membantu pengguna mencari ide masakan berdasarkan bahan yang tersedia.

ChefMate dapat memberikan resep, langkah memasak, alternatif bahan,
menyesuaikan jumlah porsi, dan memberikan tips memasak sederhana.

Project ini menggunakan Groq API sehingga **tidak membutuhkan training
model maupun dataset**.

## 1. Fitur

- 🍳 Rekomendasi masakan berdasarkan bahan
- 📝 Resep dan langkah memasak
- 🔄 Alternatif bahan
- 👨‍👩‍👧 Penyesuaian jumlah porsi
- 💬 Conversation history
- ⚡ Streaming response
- 🧹 Reset percakapan dengan `clear`
- 💾 Menyimpan riwayat dengan `save`
- 📊 Statistik dengan `stats`
- 🚪 Keluar dengan `exit`
- ⚠️ Error handling

## 2. Teknologi

- Python
- Groq API
- Groq Python SDK
- python-dotenv
- Model `openai/gpt-oss-120b`

Tidak menggunakan dataset, training model, model lokal, atau database.

## 3. Struktur Project

```text
chefmate-chatbot/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── conversations/
    └── .gitkeep
```

## 4. Cara Menjalankan

### Step 1 – Masuk ke folder project

```bash
cd chefmate-chatbot
```

### Step 2 – Buat virtual environment

Windows:

```bash
python -m venv venv
```

Aktifkan:

```bash
venv\Scripts\activate
```

### Step 3 – Install library

```bash
pip install -r requirements.txt
```

### Step 4 – Buat API key

Buat API key dari Groq.

Kemudian salin `.env.example` menjadi file `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Buka `.env`, lalu isi:

```text
GROQ_API_KEY=API_KEY_KAMU
```

**Jangan upload `.env` ke GitHub.** File tersebut sudah dimasukkan
ke `.gitignore`.

### Step 5 – Jalankan chatbot

```bash
python app.py
```

## 5. Contoh Percakapan

```text
Kamu : Saya punya telur, mie dan sawi.

ChefMate : Kamu bisa membuat mie goreng telur sawi.

Kamu : Kalau untuk 3 orang?

ChefMate : Untuk 3 orang, takaran bahan dapat disesuaikan...
```

Pertanyaan kedua tetap dapat menggunakan konteks pertanyaan pertama
karena conversation history dikirim kembali pada request berikutnya.

## 6. Perintah Chatbot

| Perintah | Fungsi |
|---|---|
| `exit` | Keluar dari chatbot |
| `clear` | Menghapus conversation history |
| `save` | Menyimpan percakapan ke JSON |
| `stats` | Menampilkan statistik percakapan |

## 7. Cara Kerja

```text
User
  ↓
Input pertanyaan
  ↓
Conversation History
  ↓
System Prompt + History
  ↓
Groq API / LLM
  ↓
Streaming Response
  ↓
Jawaban ChefMate
  ↓
Jawaban disimpan ke History
  ↓
Pertanyaan berikutnya
```

### Role dalam conversation history

- `system` → menentukan peran dan aturan ChefMate
- `user` → pesan dari pengguna
- `assistant` → jawaban dari LLM

## 8. Streaming Response

Program menggunakan:

```python
stream=True
```

Dengan streaming, jawaban ditampilkan secara bertahap ketika
LLM menghasilkan output.

## 9. Error Handling

Request ke Groq API menggunakan `try-except`. Jika terjadi error,
program menampilkan pesan error dan tidak langsung menghentikan
chatbot.

Jika request gagal, pesan user terakhir juga dihapus dari history
agar history tetap konsisten.

## 10. Penyimpanan Riwayat

Gunakan:

```text
save
```

Riwayat akan disimpan ke:

```text
conversations/chat_YYYYMMDD_HHMMSS.json
```

Riwayat juga otomatis disimpan ketika pengguna menjalankan `exit`
setelah melakukan percakapan.

## 11. Keamanan API Key

API key disimpan dalam file `.env` dan tidak ditulis langsung
di dalam kode.

File `.env` sudah dimasukkan ke `.gitignore`, sehingga tidak
seharusnya ikut ter-upload ke GitHub.

Repository hanya menyediakan `.env.example`.

## 12. Penggunaan AI Assistant

AI assistant digunakan sebagai bantuan dalam:

- Menyusun struktur program.
- Membantu implementasi Groq API.
- Membantu membuat system prompt.
- Membantu membuat conversation history.
- Membantu implementasi streaming.
- Membantu membuat error handling.
- Membantu membuat fitur penyimpanan history.
- Membantu menyusun dokumentasi.

Mahasiswa melakukan konfigurasi API key, menjalankan dan menguji
program, serta memahami konsep dan fungsi utama kode yang digunakan.

## 13. Checklist Tugas

- [x] Menggunakan API LLM
- [x] Memiliki system prompt
- [x] Memiliki conversation history
- [x] Memiliki error handling
- [x] Memiliki minimal 2 perintah khusus
- [x] Streaming response
- [x] Menyimpan riwayat percakapan
- [x] Statistik percakapan
- [x] API key tidak disimpan di source code
- [x] Tidak membutuhkan training model
