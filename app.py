# ==========================================
# CHEFMATE - AI COOKING ASSISTANT
# ==========================================

import os
import json
from datetime import datetime

from groq import Groq
from dotenv import load_dotenv


# ==========================================
# 1. MEMUAT API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("⚠️ GROQ_API_KEY belum ditemukan.")
    print("Buat file .env dan isi:")
    print("GROQ_API_KEY=API_KEY_KAMU")
    raise SystemExit


# ==========================================
# 2. MEMBUAT GROQ CLIENT
# ==========================================

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"


# ==========================================
# 3. SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
Kamu adalah ChefMate, AI Cooking Assistant yang membantu
pengguna dalam mencari dan membuat makanan.

Tugas kamu:
- Memberikan ide masakan berdasarkan bahan yang tersedia.
- Memberikan resep dan langkah memasak.
- Menyesuaikan resep berdasarkan jumlah porsi.
- Memberikan alternatif bahan jika bahan tertentu tidak tersedia.
- Memberikan tips memasak sederhana.
- Membantu memilih makanan berdasarkan waktu, budget,
  atau tingkat kesulitan.

Aturan:
- Gunakan Bahasa Indonesia.
- Gunakan bahasa yang sederhana dan ramah.
- Buat jawaban terstruktur agar mudah diikuti.
- Jika memberikan resep, tampilkan bahan dan langkah memasak.
- Jika jumlah porsi diberikan, sesuaikan takaran bahan.
- Jangan memberikan klaim medis atau diagnosis kesehatan.
- Jika pengguna menyebut alergi makanan, ingatkan bahwa
  informasi alergi perlu diperhatikan dan sarankan memeriksa
  label bahan.
"""


# ==========================================
# 4. CONVERSATION HISTORY
# ==========================================

def reset_history():
    """Mengembalikan percakapan ke kondisi awal."""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


messages = reset_history()


# ==========================================
# 5. MENGIRIM PESAN KE LLM
# ==========================================

def kirim_pesan(messages):
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            stream=True
        )

        full_answer = ""

        print("\nChefMate : ", end="")

        for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            print(text, end="", flush=True)
            full_answer += text

        print("\n")
        return full_answer

    except Exception as e:
        print("\n⚠️ Terjadi error saat menghubungi API.")
        print("Detail:", e)
        return None


# ==========================================
# 6. MENYIMPAN RIWAYAT
# ==========================================

def simpan_riwayat(messages):
    os.makedirs("conversations", exist_ok=True)

    waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/chat_{waktu}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            messages,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"✅ Riwayat disimpan ke: {filename}")


# ==========================================
# 7. STATISTIK CHAT
# ==========================================

def tampilkan_statistik(messages):
    user_messages = 0
    assistant_messages = 0

    for message in messages:
        if message["role"] == "user":
            user_messages += 1
        elif message["role"] == "assistant":
            assistant_messages += 1

    print("\n========== STATISTIK ==========")
    print(f"Pesan pengguna : {user_messages}")
    print(f"Pesan ChefMate : {assistant_messages}")
    print(f"Total pesan    : {user_messages + assistant_messages}")
    print("===============================\n")


# ==========================================
# 8. CHATBOT LOOP
# ==========================================

print("=" * 55)
print("                 CHEFMATE")
print("            AI COOKING ASSISTANT")
print("=" * 55)
print("Halo! Aku ChefMate 👨‍🍳")
print("Sebutkan bahan yang kamu punya dan aku akan membantu")
print("mencari ide masakan.\n")

print("Perintah:")
print("  exit  -> keluar")
print("  clear -> reset percakapan")
print("  save  -> simpan riwayat")
print("  stats -> statistik percakapan\n")


while True:
    user_input = input("Kamu : ").strip()

    if not user_input:
        print("Silakan masukkan pertanyaan.\n")
        continue

    if user_input.lower() == "exit":
        if len(messages) > 1:
            simpan_riwayat(messages)

        print("ChefMate selesai. Selamat memasak! 👋")
        break

    if user_input.lower() == "clear":
        messages = reset_history()
        print("\n✅ Percakapan telah direset.\n")
        continue

    if user_input.lower() == "save":
        if len(messages) > 1:
            simpan_riwayat(messages)
        else:
            print("Belum ada percakapan.")
        continue

    if user_input.lower() == "stats":
        tampilkan_statistik(messages)
        continue

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    answer = kirim_pesan(messages)

    if answer:
        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
    else:
        messages.pop()
