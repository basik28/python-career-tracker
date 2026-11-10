import hashlib
from pathlib import Path

import chromadb
from ollama import chat, embed
from pypdf import PdfReader

# BARIS AI - Persistent PDF RAG
CHAT_MODEL = "qwen2.5:3b"
EMBED_MODEL = "embeddinggemma"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "baris_ai_documents"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((page_number, text))

    return pages


def split_into_chunks(pages):
    chunks = []

    for page_number, text in pages:
        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            content = text[start:end].strip()

            if content:
                chunks.append({
                    "page": page_number,
                    "text": content
                })

            if end >= len(text):
                break

            start = end - CHUNK_OVERLAP

    return chunks


def make_document_id(file_hash, page_number, chunk_index):
    return f"{file_hash}-p{page_number}-c{chunk_index}"


def index_pdf(pdf_path):
    path = Path(pdf_path)
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()

    pages = read_pdf(path)

    if not pages:
        raise ValueError(
            "PDF'den metin çıkarılamadı. Dosya taranmış görüntü olabilir."
        )

    chunks = split_into_chunks(pages)

    # Aynı dosya tekrar eklenirse aynı ID'ler kullanılır; kayıtlar çoğalmaz.
    ids = []
    documents = []
    metadatas = []

    page_chunk_counts = {}
    for chunk in chunks:
        page = chunk["page"]
        chunk_index = page_chunk_counts.get(page, 0)
        page_chunk_counts[page] = chunk_index + 1

        ids.append(make_document_id(file_hash, page, chunk_index))
        documents.append(chunk["text"])
        metadatas.append({
            "source": path.name,
            "page": page,
            "file_hash": file_hash
        })

    print(f"{len(chunks)} metin parçası için embedding hazırlanıyor...")
    embedding_result = embed(model=EMBED_MODEL, input=documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embedding_result.embeddings
    )

    return len(chunks), path.name


def search_documents(question):
    query_result = embed(model=EMBED_MODEL, input=question)
    query_vector = query_result.embeddings[0]

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(TOP_K, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    found = []

    if results["documents"] and results["documents"][0]:
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            found.append({
                "text": document,
                "source": metadata["source"],
                "page": metadata["page"],
                "distance": distance
            })

    return found


def answer_question(question, matches):
    if not matches:
        return "Bilgi havuzunda henüz belge bulunmuyor."

    context_parts = []

    for item in matches:
        context_parts.append(
            f"[Kaynak: {item['source']}, sayfa {item['page']}]\n"
            f"{item['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
Sen BARIS AI belge asistanısın.
Yalnızca aşağıdaki bulunan belge parçalarına dayanarak cevap ver.
Yeterli bilgi yoksa bunu açıkça söyle; bilgi uydurma.
Cevapta kullandığın kaynak dosya adını ve sayfa numarasını belirt.

BELGE PARÇALARI:
{context}

SORU:
{question}
"""

    response = chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.message.content.strip()


def main():
    print("=" * 46)
    print("       BARIS AI - PERSISTENT RAG")
    print("=" * 46)
    print(f"Bilgi havuzundaki parça sayısı: {collection.count()}")
    print("\nKomutlar:")
    print("  add   = PDF ekle")
    print("  ask   = Belgelere soru sor")
    print("  exit  = Çıkış")

    while True:
        command = input("\nKomut: ").strip().lower()

        if command == "exit":
            print("BARIS AI: Görüşürüz!")
            break

        elif command == "add":
            pdf_path = input("PDF dosyasının tam yolunu gir: ").strip().strip('"')

            try:
                count, filename = index_pdf(pdf_path)
                print(
                    f"Başarılı: {filename} bilgi havuzuna eklendi "
                    f"({count} parça)."
                )
                print(f"Toplam kayıtlı parça: {collection.count()}")

            except FileNotFoundError:
                print("Dosya bulunamadı. Dosya yolunu kontrol et.")
            except Exception as error:
                print(f"PDF ekleme hatası: {error}")

        elif command == "ask":
            if collection.count() == 0:
                print("Önce 'add' komutuyla bir PDF eklemelisin.")
                continue

            question = input("Sorun: ").strip()

            if not question:
                continue

            try:
                matches = search_documents(question)
                answer = answer_question(question, matches)
                print(f"\nBARIS AI: {answer}")

            except Exception as error:
                print(f"Arama/cevap hatası: {error}")

        else:
            print("Geçersiz komut. add, ask veya exit yaz.")


if __name__ == "__main__":
    main()
