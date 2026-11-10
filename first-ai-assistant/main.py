import json
import os
from ollama import chat

MODEL = "qwen2.5:3b"
MEMORY_FILE = "memory.json"

USER_PROFILE = {
    "career_goals": [
        "İlk hedef: AI Automation Engineer",
        "İkinci hedef: AI Application Developer",
        "Uzun vadeli hedef: LLM Engineer / AI Solutions Architect",
    ],
    "work_goal": "Uluslararası şirketlerde uzaktan çalışmak ve dolar üzerinden gelir elde etmek.",
    "learning_preferences": [
        "Türkçe ve anlaşılır açıklamalar",
        "Adım adım öğrenme",
        "Uygulamalı Python ve AI projeleri",
    ],
}

SYSTEM_PROMPT = (
    "Sen BARIS AI isimli kişisel yapay zeka asistanısın. "
    "Doğal ve düzgün Türkçe konuş. Kullanıcıya kanka diye hitap edebilirsin. "
    "Bilmediğin bilgileri uydurma. Teknik konuları örneklerle açıkla. "
    "Kod yazarken çalışabilir, temiz ve eksiksiz kod üret. "
    "Kullanıcının kariyer profili: "
    + json.dumps(USER_PROFILE, ensure_ascii=False)
    + " Kullanıcı kariyer hedeflerini sorarsa profildeki hedefleri doğrudan söyle."
)


def load_memory():
    """Sohbet geçmişini JSON dosyasından yükler."""
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Uyarı: Hafıza dosyası geçersiz. Yeni sohbet başlatılıyor.")
            return []

        # Sadece geçerli kullanıcı ve asistan mesajlarını tut.
        return [
            item for item in data
            if isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

    except (json.JSONDecodeError, OSError) as error:
        print(f"Hafıza okunamadı: {error}")
        return []


def save_memory(history):
    """Sohbet geçmişini JSON dosyasına kaydeder."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Hafıza kaydedilemedi: {error}")


def main():
    history = load_memory()

    print("=" * 36)
    print("          BARIS AI ASISTAN")
    print("=" * 36)
    print(f"Model: {MODEL}")
    print("Komutlar: 'exit' = çıkış, 'clear' = sohbet geçmişini sil")
    print("Not: clear kullanıcı profilini silmez.\n")

    while True:
        try:
            user_message = input("Sen: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBARIS AI: Görüşürüz!")
            save_memory(history)
            break

        if not user_message:
            continue

        command = user_message.lower()

        if command == "exit":
            save_memory(history)
            print("BARIS AI: Hafıza kaydedildi. Görüşürüz!")
            break

        if command == "clear":
            history = []
            save_memory(history)
            print("BARIS AI: Sohbet geçmişi temizlendi. Profil bilgilerin korunuyor.\n")
            continue

        history.append({"role": "user", "content": user_message})

        # Bütün geçmiş JSON'da kalır; modele sistem talimatı ve son 6 mesaj gönderilir.
        recent_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + history[-6:]

        try:
            response = chat(model=MODEL, messages=recent_messages)
            answer = response.message.content.strip()

            print(f"\nBARIS AI: {answer}\n")

            history.append({"role": "assistant", "content": answer})
            save_memory(history)

        except Exception as error:
            # Başarısız istek geçmişte cevapsız bir kullanıcı mesajı bırakmasın.
            if history and history[-1]["role"] == "user":
                history.pop()

            print(f"BARIS AI hata: {error}")
            print("Ollama'nın çalıştığını ve qwen2.5:3b modelinin yüklü olduğunu kontrol et.\n")


if __name__ == "__main__":
    main()
