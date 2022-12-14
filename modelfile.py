from bs4 import BeautifulSoup
from datetime import date
import requests

class RequestHttp():
    """NAME
        RequestHTTP

        DESCRIPTION
            Sends requests to program site

        FUNCTIONS
            request(self, channelId (int, optional), day (RRRR-MM-DD, optional))
                Send one request to site.
                Checks site status_code
                return http.text for specific day.


        DATA DESCRIPTORS
            __init__
                pass

    """ 


    def __init__(self):
        pass

    def request (self, channelId = 0, day = date.today()) -> object :
        """Send one request to site. Checks site status_code

        Args:
            channelId (int, optional): Request Id. Defaults to 0.
            day (RRRR-MM-DD, optional): Sets date for function. Defaults to date.today().

        Returns:
            object: Returns html.text for selected url
            string: If site doesn't work (status_code 404)
        """
        http = requests.get(f"https://tv.gazeta.pl/program_tv/0,110298,8700474,,,{day},3,{channelId},0.html")
        if http.status_code == 200:
            return http.text
        elif http.status_code == 404:
            print("Website Error or check URL in Function")

class ProgramContainer(RequestHttp) :
    """NAME
        ProgramContainer

        DESCRIPTION
            Modify data from RequestHttp class

        FUNCTIONS
            find_html_programId(self, http)
                Search for Program Name and ID in html data

            save_html_programs(self, amount (int, optional))
                Saves Programs from requests in dictionary

            channel_info(self, channelName, time (optional, RRRR-MM-DD))
                Search for Program History returns w HTML

    Args:
        RequestHttp (class): Sends requests to program site

        DATA DESCRIPTORS
            __init__
                self.channelHolder - hold dictionary of scanned programs
    """

    def __init__(self):
        self.channelHolder = {}

    def find_html_programId (self, http) -> object :
        """Search for Program Name and ID in html data

        Args:
            http (object): HTTP data for scan
            
        Errors:
            AttributeError (pass) if http doesn't have program

        Returns:
            object: Returns Program Name and Program ID
        """
        try:
            programName = (http).span.text
            programId = str((http).a['href'].split("3,")[-1]).split(",")[0]
            return programName, programId
        except AttributeError:
            pass
            
    
    def save_html_programs (self, amount = 1) -> dict:
        """Saves Programs from requests to dictionary

        Args:
            amount (int, optional): Amount of channels to save. Defaults to 1
            
        Errors:
            TypeError (pass) if http doesn't have program

        Returns:
            dict: Returns Program Dictionary
        """
        loop = 0
        while loop != amount :
            loop += 1
            data = self.request(loop)
            soup = BeautifulSoup(data, "lxml")
            soupdata = soup.find("div", class_ = f"station station[{loop}]")
            scannedSoup = self.find_html_programId(soupdata)
            try:
                self.channelHolder[scannedSoup[0]] = scannedSoup[1]
            except TypeError:
                pass
                
        return self.channelHolder


    def channel_info (self, channelName, time = date.today()) -> list:
        """Search for Program History returns raw HTML

        Args:
            channelName (string): Program Name that user want to check
            time (RRRR-MM-DD, optional): Sets date for function. Defaults to date.today().

        Returns:
            list: Returns Program History in HTML list
        """
        if channelName in self.channelHolder :
            channelHttpId = self.channelHolder.get(channelName)
            data = self.request(channelId = channelHttpId, day = time)
            soup = BeautifulSoup(data, "lxml")
            soupdata = soup.find_all("li", {"class" : ['even', 'odd']})
            return soupdata
        else:
            return "Channel wasn't Scanned"


