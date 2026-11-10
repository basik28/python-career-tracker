
def hesap_makinesi():

    print("=== BARIS AI HESAP MAKİNESİ ===")

    while True:

        print("\n1 - Toplama")
        print("2 - Çıkarma")
        print("3 - Çarpma")
        print("4 - Bölme")
        print("0 - Çıkış")

        try:
            operation = int(input("İşlem seçin: "))

            if operation == 0:
                print("Program kapatılıyor.")
                break

            if operation not in (1, 2, 3, 4):
                print("Geçersiz işlem!")
                continue

            num1 = float(input("İlk sayı: "))
            num2 = float(input("İkinci sayı: "))

            if operation == 1:
                result = num1 + num2

            elif operation == 2:
                result = num1 - num2

            elif operation == 3:
                result = num1 * num2

            elif operation == 4:
                if num2 == 0:
                    print("Hata: Sıfıra bölünemez!")
                    continue

                result = num1 / num2

            print(f"Sonuç: {result}")

        except ValueError:
            print("Hata: Lütfen geçerli bir sayı girin.")


if __name__ == "__main__":
    hesap_makinesi()
