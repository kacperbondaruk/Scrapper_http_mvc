from scan import Channel_Scanner
from json_save import Program

        
class Menu(Channel_Scanner):
    def __init__(self) -> None:
        self.scanArray = Channel_Scanner()
        super().__init__()
        self.userEntryInput = input("""Witaj za chwile program rozpocznie pobierać listę kanałów.\n
Domyślna lista łączy wynosi 100 i potrwa do 15 sekund czy podnieść / zmniejszyć tą liczbę?
1 - Tak 
2 - Nie\n""")

        if self.userEntryInput == "1" or self.userEntryInput.lower().capitalize() == "Tak":
            self.userScanInput = int(input("Podaj liczbę łączy: \n"))
            self.scanArray.scan(self.userScanInput)
            print("\n")
        else:
            self.scanArray.scan()
            print("\n")

        while True:
            self.MenuInput = input("""Witaj w Menu!
            1 - Sprawdź kanał
            2 - Wyświetl listę kanałów
            3 - Aktualizuj liste kanałów
            4 - Zapisz wybraną historie kanału
            5 - Zamknij Program \n""")
            if self.MenuInput == "1":
                self.scanArray.date_question()
            elif self.MenuInput == "2":
                self.scanArray.scanned()
            elif self.MenuInput == "3":
                Menu()
                break
            elif self.MenuInput == "4":
                self.scanArray.save_json()
            elif self.MenuInput == "5":
                print("Miłego Oglądania!")
                break



