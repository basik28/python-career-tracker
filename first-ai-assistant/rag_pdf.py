import math
from pypdf import PdfReader
from ollama import chat, embed

CHAT_MODEL = "qwen2.5:3b"
EMBED_MODEL = "embeddinggemma"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4


def read_pdf(path):
    reader = PdfReader(path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((page_number, text))

    return pages


def make_chunks(pages):
    chunks = []

    for page_number, page_text in pages:
        start = 0

        while start < len(page_text):
            end = start + CHUNK_SIZE
            piece = page_text[start:end].strip()

            if piece:
                chunks.append({
                    "page": page_number,
                    "text": piece
                })

            if end >= len(page_text):
                break

            start = end - CHUNK_OVERLAP

    return chunks


def add_embeddings(chunks):
    # Ollama creates a vector for each text chunk.
    texts = [chunk["text"] for chunk in chunks]
    result = embed(model=EMBED_MODEL, input=texts)

    for chunk, vector in zip(chunks, result.embeddings):
        chunk["embedding"] = vector

    return chunks


def cosine_similarity(vector_a, vector_b):
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def find_relevant_chunks(question, chunks):
    question_result = embed(model=EMBED_MODEL, input=question)
    question_vector = question_result.embeddings[0]

    ranked = []

    for chunk in chunks:
        score = cosine_similarity(question_vector, chunk["embedding"])
        ranked.append((score, chunk))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in ranked[:TOP_K]]


def answer_question(question, relevant_chunks):
    context = "\n\n".join(
        f"[PDF sayfa {chunk['page']}]\n{chunk['text']}"
        for chunk in relevant_chunks
    )

    prompt = f"""
Sen BARIS AI belge asistanısın.
Soruyu yalnızca aşağıdaki PDF parçalarına dayanarak cevapla.
Cevap için yeterli bilgi yoksa bunu açıkça söyle.
Belgede olmayan bilgi uydurma. Mümkünse sayfa numarasını belirt.

PDF'DEN BULUNAN İLGİLİ BÖLÜMLER:
{context}

KULLANICININ SORUSU:
{question}
"""

    response = chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.message.content


def main():
    print("=" * 40)
    print("       BARIS AI - PDF RAG")
    print("=" * 40)

    path = input("PDF dosyasının tam yolunu gir: ").strip().strip('"')

    try:
        pages = read_pdf(path)

        if not pages:
            print("PDF'den metin çıkarılamadı. Dosya taranmış görüntü olabilir.")
            return

        chunks = make_chunks(pages)

        if not chunks:
            print("PDF'de analiz edilecek metin bulunamadı.")
            return

        print(f"PDF okundu: {len(pages)} sayfa, {len(chunks)} metin parçası.")
        print("Belge için arama vektörleri hazırlanıyor...")

        chunks = add_embeddings(chunks)
        print("Hazır. Sorularını sorabilirsin. Çıkmak için 'exit' yaz.")

        while True:
            question = input("\nSen: ").strip()

            if question.lower() == "exit":
                print("BARIS AI: Görüşürüz!")
                break

            if not question:
                continue

            relevant = find_relevant_chunks(question, chunks)
            answer = answer_question(question, relevant)
            print(f"\nBARIS AI: {answer}")

    except FileNotFoundError:
        print("Dosya bulunamadı. PDF yolunu kontrol et.")
    except Exception as error:
        print(f"Bir hata oluştu: {error}")


if __name__ == "__main__":
    main()
