from channelscanner import ChannelScanner

        
class Menu(ChannelScanner):
    """NAME
            Menu
    
       DESCRIPTION 
            User Interface


        DATA DESCRIPTORS
            scanArray - Holds ChannelScanner() methods and data

            userEntryInput - Ask user if he want to scan more than 100 requests

            userScanInput - Ask how many requests user want to scan

            menuInput - Ask user about Scanning / Saving / Updating / Printing HTML program data

            channelId - holds id(string) that let program connect to the indicated channel

            today - holds today date in RRRR-MM-DD value

            channelHolder - save scanned channels from request in dictionary (channelName : channelId)

            programList - hold selected HTML data(string) in list for JSON format



    ARGS:
        ChannelScanner (Main Class): Finds URL, Scan HTML, Keep Date, Save HTML to JSON,
            Prints information to user
    """
    def __init__(self) -> None:
        self.scanArray = ChannelScanner()
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
                self.scanArray.check_channel()
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



