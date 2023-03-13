import csv
from datetime import datetime

# Pizza sınıfı tanımlama
class Pizza:
    def __init__(self, description, cost):
        self.description = description
        self.cost = cost

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

# Alt sınıflar oluşturma
class Klasik(Pizza):
    def __init__(self):
        super().__init__("Klasik Pizza", 25.0)

class Margherita(Pizza):
    def __init__(self):
        super().__init__("Margherita Pizza", 30.0)

class TurkPizzasi(Pizza):
    def __init__(self):
        super().__init__("Türk Pizzası", 35.0)

class DominosPizza(Pizza):
    def __init__(self):
        super().__init__("Dominos Pizza", 40.0)

# Decorator sınıfı tanımlama
class Decorator(Pizza):
    def __init__(self, component):
        self.component = component

    def get_description(self):
        return self.component.get_description() + ", " + Pizza.get_description(self)

    def get_cost(self):
        return self.component.get_cost() + Pizza.get_cost(self)

# Sos sınıflarını tanımlama
class Zeytin(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Zeytin"
        self.cost = 5.0

class Mantar(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Mantar"
        self.cost = 7.0

class KeciPeyniri(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Keçi Peyniri"
        self.cost = 10.0

class Et(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Et"
        self.cost = 12.0

class Sogan(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Soğan"
        self.cost = 5.0

class Misir(Decorator):
    def __init__(self, pizza):
        super().__init__(pizza)
        self.description = "Mısır"
        self.cost = 6.0


def tc_kimlik_no_dogrula(tc_kimlik_no):
    # Hatalı girdi kontrolü
    if not tc_kimlik_no.isdigit() or len(tc_kimlik_no) != 11 or tc_kimlik_no[0] == '0':
        return False

    # 1. 3. 5. 7. ve 9. hanelerin toplamının 7 katı
    tekler_toplami = sum(int(tc_kimlik_no[i]) for i in range(0, 9, 2))
    tekler_katlami = tekler_toplami * 7

    # 2. 4. 6. ve 8. hanelerin toplamı
    ciftler_toplami = sum(int(tc_kimlik_no[i]) for i in range(1, 9, 2))

    # 10. hanenin kontrolü
    kontrol1 = (tekler_katlami - ciftler_toplami) % 10
    if int(tc_kimlik_no[9]) != kontrol1:
        return False

    # 1-10. hanelerin toplamının 10'a bölümünden kalanın 11. haneyi vermesi gerekiyor
    toplam = sum(int(tc_kimlik_no[i]) for i in range(10))
    kontrol2 = toplam % 10
    if int(tc_kimlik_no[10]) != kontrol2:
        return False

    return True
def luhn_algorithm(kart_numarasi):
    # Kart numarası bir string olmalı
    # Kart numarasını ters çevir
    kart_numarasi = kart_numarasi[::-1]
    
    # Değişkenleri başlat
    toplam = 0
    ikinci_digit = False
    
    # Kart numarasındaki her rakam için döngü oluştur
    for rakam in kart_numarasi:
        # Eğer ikinci rakamsa, iki katına çıkar
        if ikinci_digit:
            iki_kati = int(rakam) * 2
            # Sonuç iki haneli ise, rakamları topla
            if iki_kati > 9:
                iki_kati = int(str(iki_kati)[0]) + int(str(iki_kati)[1])
            toplam += iki_kati
        else:
            toplam += int(rakam)
        # Bir sonraki iterasyon için ikinci_digit bayrağını çevir
        ikinci_digit = not ikinci_digit
    
    # Toplamın 10'a bölümünden kalan 0 ise True, aksi takdirde False döndür
    return toplam % 10 == 0
def main():
    # Menüyü yazdır
    with open("Menu.txt","r", encoding="utf-8") as fl:
        print(fl.read())

    pizza = None
    while True:
        # Kullanıcının seçimini al
        choice = int(input("Lütfen bir pizza seçin (1-5): "))

        if choice == 1:
            pizza = Klasik()
        elif choice == 2:
            pizza = Margherita()
        elif choice == 3:
            pizza = TurkPizza()
        elif choice == 4:
            pizza = DominosPizza()
        elif choice == 5:
            print("Çıkış yapılıyor...")
            return
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")
            continue

        choice = int(input("Lütfen bir Sos seçin (6-11): "))

        if choice == 6:
            pizza = Zeytin(pizza)
        elif choice == 7:
            pizza = Mantar(pizza)
        elif choice == 8:
            pizza = KeciPeyniri(pizza)
        elif choice == 9:
            pizza = Et(pizza)
        elif choice == 10:
            pizza = Sogan(pizza)
        elif choice == 11:
            pizza = Misir(pizza)
        elif choice == 12:
            pass
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")
            continue

        # Sipariş özeti
        print("Sipariş özeti:")
        print("Pizza: {}".format(pizza.get_description()))
        print("Toplam fiyat: {} TL".format(pizza.get_cost()))

        # Kullanıcının bilgilerini al
        isim = input("İsim: ")
        kimlik = input("TC Kimlik Numarası: ")
        while not tc_kimlik_no_dogrula(kimlik):
            kimlik = input("Geçersiz TC Kimlik Numarası, lütfen doğru girin: ")
        kart_num = input("Kredi Kartı Numarası: ")
        while not luhn_algorithm(kart_num):
            kart_num = input("Geçersiz Kredi Kartı Numarası, lütfen doğru girin: ")
        kart_sifre = input("Kredi Kartı Şifresi: ")

        # Siparişi veritabanına kaydet
        database = "Orders_Database.csv"
        with open(database, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "ID", "Credit Card Number", "Pizza Description", "Order Time", "Credit Card Password"])
            writer.writerow([isim, kimlik, kart_num, pizza.get_description(),
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kart_sifre])

        print("Sipariş alındı! Teşekkür ederiz.")

if __name__ == "__main__":
    main()


