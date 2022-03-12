from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import re


# Class for structuring data


class House:
    def __init__(self):
        self.city = None
        self.plotsize = None
        self.location = None
        self.rooms = None
        self.seller = None
        self.price = None
        self.name = None
        self.squaremeters = None

    def init(self, name="", price=0, squaremeters=0, seller="", rooms=0, location=0.0, plotsize=0, city=""):
        self.squaremeters = squaremeters
        self.name = name
        self.price = price
        self.seller = seller
        self.rooms = rooms
        self.location = location
        self.plotsize = plotsize
        self.city = city

    def str(self):
        return self.name


# function for converting a string into int
def getint(string):
    final = ''
    # remove decimal delimiter to get clean value
    string = string.replace(".", "")
    for z in string:
        try:
            final += str(int(z))
        except ValueError:
            return int(final)


# selenium config
DRIVER_PATH = "C:\\ChromeWebdriver\\chromedriver.exe"
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# main url with querystring for the search result
url = "https://www.immowelt.de/liste/41069/haeuser/kaufen?d=true&r=50&sd=DESC" \
      "&sf=RELEVANCE&sp=@PAGENUMBER@"

# initialize variables
# Collection for the houses
HouseCollection = []
# lastHouselist to stop the loop
lastHouselist = ""
# fallback value to stop the loop after defined turns
maxPages = 100

# loop for each page till limit or no new houses found
for i in range(1, maxPages):
    # Set Pagenumber
    curURL = url.replace("@PAGENUMBER@", str(i))
    print("Current URL")
    print(curURL)

    # open url
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(curURL)
    # Wait for content being loaded
    driver.implicitly_wait(2)

    try:
        # get the houselist via class-name
        # the structure has been analyzed before, the search results have defined a classname für each house
        # the house-element has always the same structure and can be split by newline
        HouseList = driver.find_elements(By.CLASS_NAME, "EstateItem-1c115")

        if lastHouselist == HouseList:
            # Houseliste is the same with the previous, so it's the end of the List
            break

        # Save content of the last Result, so compare it for the break of the loop
        lastHouselist = HouseList

        # Loop through the Houselist
        for e in HouseList:
            # Extract the text
            rowItems = e.text.splitlines()
            # initialize the Class House as new instance
            currentHouse = House()

            # Key-Attributes that need to be identified correctly
            hasName = 0
            hasPrice = 0
            hasRooms = 0
            hasSQ = 0
            hasLocation = 0
            hasCity = 0
            hasPlotsize = 0
            hasSeller = 0

            if len(rowItems) >= 6:
                if rowItems[0].find("m²") == -1 and rowItems[0].find("€") == -1 and rowItems[0].find("Zi.") == -1:
                    # Identify seller by Itemposition
                    currentHouse.seller = rowItems[0]
                    hasSeller = 1
                if rowItems[1].find("€") > -1:
                    # Identify price by Itemposition
                    try:
                        houseprice = getint(rowItems[1])
                        currentHouse.price = houseprice
                        hasPrice = 1
                    # broad except to catch any possible error and skip the house
                    except:
                        hasPrice = 0

                if rowItems[2].find("m²") > -1:
                    # Identify squaremeters by Itemposition
                    currentHouse.squaremeters = getint(rowItems[2])
                    hasSQ = 1
                if rowItems[3].find("Zi.") > -1:
                    #  Identify rooms by Itemposition
                    currentHouse.rooms = getint(rowItems[3])
                    hasRooms = 1
                if rowItems[4] not in "m²" and rowItems[4] not in "€" and rowItems[4] not in "Zi.":
                    #  Identify housename by Itemposition
                    currentHouse.name = rowItems[4]
                    hasName = 1
                if len(rowItems) >= 7 and rowItems[6].find("m²") == -1 and rowItems[6].find("€") == -1 and \
                        rowItems[6].find("Zi.") == -1:
                    #  Identify location by Itemposition

                    if len(rowItems[6].split("|")) > 1:
                        # get distance from string
                        currentHouse.location = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", rowItems[6].split("|")[0])[0]
                        # get cityname
                        currentHouse.city = rowItems[6].split("|")[1]
                        hasLocation = 1
                        hasCity = 1
                if len(rowItems) >= 9 and rowItems[8].find("m²") > -1:
                    #  Identify plotsize by Itemposition
                    currentHouse.plotsize = getint(rowItems[8])
                    hasPlotsize = 1

            # check if attributes are included
            if hasName == 1 & hasSeller == 1 & hasPrice == 1 & hasSQ == 1 & \
                    hasRooms == 1 & hasLocation == 1 & hasCity == 1 & \
                    hasPlotsize == 1:
                # Add House to collection
                HouseCollection.append(currentHouse)

    finally:
        #  increase pagenumber for next turn
        i = +1
        # close browser
        driver.quit()

# convert Collection of Class to final Collection
# there was no stable way to write the collection of class to a file, tried it with pickle, but it had issues with codec

# Workaround: Convert the collection of class in a "normal" collection
x = 1
hname = ""
hprice = ""
hsquaremeters = ""
hrooms = ""
hlocation = ""
hplotsize = ""
hseller = ""
hcity = ""

finalCollection = []
finalCollectionDataframe = []

for h in HouseCollection:
    print("House name:")
    print(h.name)
    hname = h.name
    print("House price:")
    print(h.price)
    hprice = h.price
    print("House squaremeters:")
    print(h.squaremeters)
    hsquaremeters = h.squaremeters
    print("House rooms:")
    print(h.rooms)
    hrooms = h.rooms
    print("House location:")
    print(h.location)
    hlocation = h.location
    print("House city:")
    print(h.city)
    hcity = h.city
    print("House plotsize:")
    print(h.plotsize)
    hplotsize = h.plotsize
    print("House seller:")
    print(h.seller)
    hseller = h.seller
    tmpHouse = [hname, hprice, hsquaremeters, hrooms, hlocation, hplotsize,
                hseller, hcity]

    finalCollection.append(tmpHouse)
    tmpHouse = [hprice, hsquaremeters, hrooms, hlocation, hplotsize]
    finalCollectionDataframe.append(tmpHouse)
    x += 1

# write new collection to csv-file
with open("c:\\temp\\houselist.csv", "w", newline='', encoding="utf-8") as \
        csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    writer.writerow(["Name", "Price", "Livingspace", "Rooms", "Distance", "Plotsize", "Seller", "City"])
    writer.writerows(finalCollection)
# write new collection with numeric columns only to csv-file
with open("c:\\temp\\houselist_df.csv", "w", newline='', encoding="utf-8") as \
        csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    writer.writerow(["Price", "Livingspace", "Room", "Distance", "Plotsize"])
    writer.writerows(finalCollectionDataframe)