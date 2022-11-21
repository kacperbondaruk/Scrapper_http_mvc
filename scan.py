import requests
from bs4 import BeautifulSoup
from datetime import date
import pprint
import time
import json


class Channel_Scanner() :
    """Ta klasa odpowiada za skanowanie kanałów. Wysyła ona n requestów 
    w celu sprawdzenia kodu html i przypisaniu nazwy kanału do numeru ID
     w słowniku jeśli dany link URL posiada historie programu. 
     Następnie uzytkownik wpisując nazwe kanału odwołuje się do przypisanego numeru ID
     dzięki czemu program wie, którą strone ma otworzyć a następnie zeskanować.
    """
    def __init__(self) -> None:
        self.channelId = "1"
        self.today = date.today()
        self.channelHolder = {}
        self.channelProgram = []
        self.programList = []

    def scan(self, amount = 100) -> dict:
        """
        Ta metoda zbiera dane na temat dostępnych kanałów
        - Argumenty:
            amount (int, opcjonalnie): Domyślnie skanuje 100 kanałów (15 sekund średnio na 100 skanów).

        - Zwraca:
            dict: Aktualizuje zmienną self.channelHolder
        """
        print(f"Rozpoczynam skanowanie {amount} łączy")
        while self.channelId != (amount) :
            http = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{self.today},3,{self.channelId},0.html").text
            soup = BeautifulSoup(http, "lxml")
            httpData = soup.find("div", class_ = f"station station[{self.channelId}]")
            try:        
                programName = httpData.span.text
                programId = str(httpData.a['href'].split("3,")[-1]).split(",")[0]
                self.channelHolder.update({programName : programId})
            except AttributeError:
                print(f"Łącze {self.channelId} nie posiada kanału pod tym adresem")
            finally:
                self.channelId = int(self.channelId)
                self.channelId = self.channelId + 1
        return self.channelHolder
        
    def scanned (self):
        """Printuje zeskanowane wcześniej kanały, aby ułatwić wybór uzytkownikowi"""
        print("Oto lista dostępnych kanałów: \n")
        for key in self.channelHolder.keys():
            print(key)

    def date_question(self):
        self.userInputDate = input("""Chcesz wybrać datę inną od teraźniejszej?
        1 - Tak
        2 - Nie \n""")
        if self.userInputDate == "1" or self.userInputDate.lower().capitalize() == "Tak":
            self.today = str(input("Podaj date w formacie RRRR-MM-DD z myślnikami \n"))
            self.check_channel()
        else:
            self.check_channel()

    def check_channel(self):
        self.userInputChannel = input("Podaj program, który Cię interesuje: ")
        self.selectedProgram = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{self.today},3,{self.channelHolder.get(self.userInputChannel)},0.html").text
        self.soup2 = BeautifulSoup(self.selectedProgram, "lxml")
        self.programHistory = self.soup2.find_all("li", {"class" : ['even', 'odd']})
        print(f"Oto Aktualne dane na dzień {self.today}")
        time.sleep(1)
        for data in self.programHistory:
            self.programHeader = data.find("a").text
            self.programType = data.find("p").text
            self.programTime = data.find("div", class_ = 'time').text
            self.programDescription = data.find_all("p")[1].text.replace("\n", "").rstrip().lstrip()
            self.programLink = "https://tv.gazeta.pl/"+ data.a["href"].replace("\n", "")
            
            print(self.programHeader)
            print(self.programType)
            print(self.programTime)
            print(self.programDescription)
            print(self.programLink + "\n")

    def save_json (self):
        self.userInputChannel = input("Podaj program, który Cię interesuje: ")
        self.selectedProgram = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{self.today},3,{self.channelHolder.get(self.userInputChannel)},0.html").text
        self.soup2 = BeautifulSoup(self.selectedProgram, "lxml")
        self.programHistory = self.soup2.find_all("li", {"class" : ['even', 'odd']})
        print(f"Zapisuje {self.userInputChannel} z dnia {self.today}")
        time.sleep(1)
        for data in self.programHistory:
            self.title = data.find("a").text
            self.programType = data.find("p").text
            self.programTime = data.find("div", class_ = 'time').text
            self.programDescription = data.find_all("p")[1].text.replace("\n", "").rstrip().lstrip()
            self.programLink = "https://tv.gazeta.pl/"+ data.a["href"].replace("\n", "")
            a = {"tytuł" : self.title}
            b = {"godzina" : self.programTime}
            c = {"opis" : self.programDescription}
            d = {"typ" : self.programType}
            e = {"link" : self.programLink}
            self.programList.append(a.copy())
            self.programList.append(b.copy())
            self.programList.append(c.copy())
            self.programList.append(d.copy())
            self.programList.append(e.copy())
            with open(f"Dane_programu.json", "a+") as f:
                json.dump(self.programList, f)
                f.write("\n")


#Bugi: Niektóre kanały mimo zgodności kodu do odbieranego html nie zwracają prawidłowej wartości jest to mniej niz 5 % zwracanych danych
