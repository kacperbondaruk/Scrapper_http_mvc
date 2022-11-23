import requests
from bs4 import BeautifulSoup
from datetime import date
import json


class ChannelScanner() :
    """NAME
            ChannelScanner

        DESCRIPTION
            Finds URL, Scan HTML, Keep Date, Save HTML to JSON,
            Prints information to user

        FUNCTIONS
            scan(self, amount (int, optional))
                Scan URL to check if the HTML contains channel information
            
            scanned(self)
                Print HTML from scanned channels that were stored in channelHolder

            date_question(self)
                Ask user if he would like to change date of selected channel in menu

            check_channel(self)
                Ask user for the channelName and prints out HTML code

            save_json(self)
                Save selected channel in JSON Format


        DATA DESCRIPTORS
            __init__
                channelId - holds id(string) that let program connect to the indicated channel

                today - holds today date in RRRR-MM-DD value

                channelHolder - save scanned channels from request in dictionary (channelName : channelId)

                programList - hold selected HTML data(string) in list for JSON format

    """
    def __init__(self) -> None:
        self.channelId = "1"
        self.today = date.today()
        self.channelHolder = {}
        self.programList = []

    def scan(self, amount = 100) -> dict:
        """Sends amount(Requests) to check if HTML contain program information

        Args:
            amount (int, optional): Takes Amount of Requests. Defaults to 100.

        Returns:
            dict: Returns dictionary of scanned channels
        """
        print(f"Rozpoczynam skanowanie {amount} łączy:")
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
        
    def scanned (self) -> None:
        """Prints scanned channels to user

        Args:
            Self

        Returns:
            None
        """
        print("Oto lista dostępnych kanałów: \n")
        for key in self.channelHolder.keys():
            print(key)
        print("\n")

    def date_question(self) -> None:
        """Ask user if he would like to change date of channel history
        
        Args:
            Self
        
        Returns:
            None"""
        self.userInputDate = input("""Chcesz wybrać datę inną od teraźniejszej?
        1 - Tak
        2 - Nie \n""")
        if self.userInputDate == "1" or self.userInputDate.lower().capitalize() == "Tak":
            self.today = str(input("Podaj date w formacie RRRR-MM-DD z myślnikami \n"))
            if len(self.today) != 10:
                print("Podałeś niepoprawny format \n")
                self.date_question()
        elif self.userInputDate == "2" or self.userInputDate.lower().capitalize() == "Nie":
            self.today = date.today()


    def check_channel(self) -> None:
        """Prints whole HTML channel history converted to string for particular day

        Args:
            Self

        Returns:
            None"""
        self.userInputChannel = input("Podaj program, który Cię interesuje: ")
        self.selectedProgram = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{self.today},3,{self.channelHolder.get(self.userInputChannel)},0.html").text
        self.soup2 = BeautifulSoup(self.selectedProgram, "lxml")
        self.programHistory = self.soup2.find_all("li", {"class" : ['even', 'odd']})
        print(f"Oto Aktualne dane na dzień {self.today}")
        
        for data in self.programHistory:
            self.programHeader = data.find("a").text
            self.programType = data.find("p").text
            self.programTime = data.find("div", class_ = 'time').text
            self.programDescription = data.find_all("p")[1].text.replace("\n", "").strip()
            self.programLink = "https://tv.gazeta.pl/"+ data.a["href"].replace("\n", "")
            
            print(self.programHeader)
            print(self.programType)
            print(self.programTime)
            print(self.programDescription)
            print(self.programLink + "\n")

    def save_json (self) -> None:
        """Create new file with selected channel history in JSON format

        Functions:
            date_question()

        Args:
            Self

        Returns:
            None
        """
        self.date_question()
        self.userInputChannel = input("Podaj program, który Cię interesuje: ")
        self.selectedProgram = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{self.today},3,{self.channelHolder.get(self.userInputChannel)},0.html").text
        self.soup2 = BeautifulSoup(self.selectedProgram, "lxml")
        self.programHistory = self.soup2.find_all("li", {"class" : ['even', 'odd']})
        print(f"Zapisuje {self.userInputChannel} z dnia {self.today}")
        for data in self.programHistory:
            self.programHeader = {"tytuł" : data.find("a").text}
            self.programType = {"typ" : data.find("p").text}
            self.programTime = {"czas" : data.find("div", class_ = 'time').text + f" [{self.today}]"}
            self.programDescription = {"opis" : data.find_all("p")[1].text.replace("\n", "").strip()}
            self.programLink = {"link" : "https://tv.gazeta.pl/"+ data.a["href"].replace("\n", "")}
            
            self.programList.append([self.programHeader, self.programType, self.programTime, self.programDescription, self.programLink])
            with open(f"program_data.json", "w+") as f:
                json.dump(self.programList, f, indent = 1)
