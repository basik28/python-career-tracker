
from pypdf import PdfReader
from ollama import chat

MODEL = "qwen2.5:3b"


def read_pdf(file_path):

    try:
        reader = PdfReader(file_path)

        text = ""

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            text += f"\n--- Sayfa {page_number} ---\n"
            text += page_text

        return text

    except Exception as error:
        print("PDF okuma hatası:", error)
        return None


def analyze_document(document_text, question):

    prompt = f"""
    Sen BARIS AI belge analiz asistanısın.

    Aşağıdaki PDF içeriğini incele.
    Yalnızca belgedeki bilgilere dayanarak cevap ver.
    Belgede olmayan bilgileri uydurma.

    PDF İÇERİĞİ:
    {document_text[:12000]}

    KULLANICININ SORUSU:
    {question}
    """

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content


def main():

    print("==============================")
    print("     BARIS AI PDF ANALYZER")
    print("==============================")

    file_path = input("PDF dosyasının yolunu gir: ")

    document_text = read_pdf(file_path)

    if not document_text or not document_text.strip():
        print("PDF içinden metin okunamadı.")
        return

    print("\nPDF başarıyla okundu!")
    print("Karakter sayısı:", len(document_text))

    while True:

        question = input("\nBelge hakkında sorun (exit = çıkış): ")

        if question.lower() == "exit":
            print("PDF Analyzer kapatılıyor.")
            break

        answer = analyze_document(document_text, question)

        print("\nBARIS AI:", answer)


if __name__ == "__main__":
    main()
