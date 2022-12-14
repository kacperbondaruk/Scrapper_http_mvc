from datetime import date
import re
from modelfile import ProgramContainer
from view import View

class Menu() :
    """NAME
        Menu

        DESCRIPTION
            User Interface Control modelFile and view

        FUNCTIONS
            ask_for_requests_amount(self)
                Ask user how many sites he wants to scan

            channel_question(self, exception (dict))
                Ask user which user he would like to check

            date_question (self, regex (string, optional))
                Ask user which day he would like to choose

            interface(self)
                Main user interface
        
        DATA DESCRIPTORS
            __init__
                self.today - holds date selected by user

                self.channelName - hold channel selected by user
                

    """

    def __init__(self) -> None:
         self.today = date.today()
         self.channelName = 0 

    def ask_for_requests_amount (self) -> int :
        """Ask user how many site he want to scan

        Args:
            Self

        Returns:
            int : Returns user input
        """
        userEntryInput = input("""Witaj za chwile program rozpocznie pobierać listę kanałów.\n
Domyślna lista łączy wynosi 20 i potrwa do 5 sekund czy podnieść / zmniejszyć tą liczbę?
1 - Tak 
2 - Nie\n""")
        if userEntryInput == "1" or userEntryInput.lower() == "tak":
            try:
                userRequestInput = int(input("Podaj liczbę łączy: \n"))
                print("Rozpoczynam Skanowanie... \n")
                return userRequestInput
            except ValueError:
                print("To nie jest liczba! Restartuje program... \n")
                return self.ask_for_requests_amount()

            
        elif userEntryInput == "2" or userEntryInput.lower() == "nie":
            print("Rozpoczynam Skanowanie...")
            print("\n")
            return 20
        else:
            print("Nie ma takiego wyboru. Wybierz numer lub odpowiedź. \n")
            return self.ask_for_requests_amount()
    
    def channel_question(self, exception) -> str:
        """Ask user which channel he would like to check

        Args:
            Self

            exception: Dictionary with scanned channels

        Returns:
            int : Returns user input
        """
        self.channelName = input("Podaj nazwe programu: \n")
        if self.channelName not in exception :
            print("Nie ma takiego kanału! \n")
            return self.channel_question(exception)
        else:
            return self.channelName

    def date_question(self, regex = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$") -> object :
        """Ask user which date he would like to select

        Args:
            Self

            regex: formula for corret input RRRR-MM-DD

        Returns:
            object : Returns user input
        """
        userInputDate = input("""Chcesz wybrać datę inną od teraźniejszej?
        1 - Tak
        2 - Nie \n""")
        if userInputDate == "1" or userInputDate.lower() == "tak":
            self.today = input("Podaj date w formacie RRRR-MM-DD z myślnikami \n")
            if not re.match(regex, self.today) :
                print("Podałeś niepoprawny format \n")
                self.date_question()
            else:
                return self.today
        elif userInputDate == "2" or userInputDate.lower() == "nie":
            self.today = date.today()
        else:
            print("Nie ma takiego wyboru \n")
            self.date_question()

    def interface (self) -> object:
        """User Interface

        Args:
            Self

        Returns:
            object : Returns user input
        """
        while True:
            try:
                MenuInput = int(input("""Witaj w Menu!
                    1 - Sprawdź kanał
                    2 - Wyświetl listę kanałów
                    3 - Zapisz wybraną historie kanału
                    4 - Zamknij Program \n"""))
                if MenuInput > 4 or MenuInput < 1 :
                    print("Nie ma takiego wyboru \n")
                    return self.interface()
                elif MenuInput == 1:
                        self.date_question()
                        self.channel_question(programModel.channelHolder)
                        view.channel_view(programModel.channel_info(self.channelName, self.today))
                elif MenuInput == 2:
                    view.channel_list(programModel.channelHolder)
                elif MenuInput == 3:
                    self.date_question()
                    self.channel_question(programModel.channelHolder)
                    view.channel_json(programModel.channel_info(self.channelName, self.today), self.today)
                elif MenuInput == 4:
                    print("Miłego Oglądania!")
                    break
            except ValueError:
                print("To nie jest liczba! \n")
                return self.interface()

#----------------------------------------CONTROLLER---------------------------------------------------------------------------------

menu = Menu()
view = View()
programModel = ProgramContainer()


requestsAmount = menu.ask_for_requests_amount()     # Pytanie o liczbę skanów
programModel.save_html_programs(requestsAmount)     # Zapisywanie kanałów do słownika
menu.interface()                                    # Interface


