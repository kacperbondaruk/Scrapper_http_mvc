from scan  import Channel_Scanner
import time
import requests
import json
from bs4 import BeautifulSoup

class Program(Channel_Scanner):
    def __init__(self) -> None:
        self.programList = []
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


