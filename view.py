import json

class View ():
    """NAME
            View

        DESCRIPTION
            Converts data into print presentation for user

        FUNCTIONS

            channel_view(self, data)
                Print program history from HTML
            
            channel_list(self, data)
                Print scanned programs to user

            channel_json(self, data, time)
                Modify raw HTML and save it into json file

        DATA DESCRIPTORS

            __init__
                pass
    """
    def __init__(self) -> None:
        pass

    def channel_view (self, data) -> None:
        """Print program history from HTML

        Args:
            data (object): Takes raw HTML from model
        """
        for element in data :
            print(element.find("a").text)
            print(element.find("p").text)
            print(element.find("div", class_ = 'time').text)
            print(element.find_all("p")[1].text.replace("\n", "").strip())
            print("https://tv.gazeta.pl/"+ element.a["href"].replace("\n", ""))

    def channel_list (self, data) -> None:
        """Print scanned programs to user

        Args:
            data (object): Takes model program dictionary
        """
        print("\n Oto lista twoich kanałów! \n")
        for program in data.keys():
            print(program)
        print("\n")

    def channel_json (self, data, time) -> None :
        """Modify raw HTML and save it into json file

        Args:
            data (object): Takes raw HTML list from model
            time (RRRR-MM-DD): Set date in function
        """
        program = []
        jsonData = data
        for element in jsonData :
            jsonData = {"tytuł" : element.find("a").text, 
            "typ" : element.find("p").text, 
            "czas" : element.find("div", class_ = 'time').text + f" [{time}]", 
            "opis" : element.find_all("p")[1].text.replace("\n", "").strip(), 
            "link" : "https://tv.gazeta.pl/"+ element.a["href"].replace("\n", "")}
                
            program.append(jsonData)
    
        with open(f"program_data.json", "w+") as f:
            json.dump(program, f, indent = 1)