import requests
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver


# def collectTimes(hall):

def timeConverter(websiteTime):
    splitTime = websiteTime.split()
    firstTime = splitTime[0] + splitTime[1]
    secondTime = splitTime[3] + splitTime[4]

    print(firstTime)
    print(secondTime)

    today = datetime.today()
    print(today)
    print(today.day)

    openTime = datetime.strptime(firstTime, '%I:%M%p')
    openTime = openTime.replace(day=today.day, year=today.year, month = today.month)
    print(openTime.date())
    closeTime = datetime.strptime(secondTime, '%I:%M%p')
    closeTime = closeTime.replace(day=today.day, year=today.year, month = today.month)
    print(openTime)
    print(closeTime)
    return [openTime, closeTime]

driver = webdriver.Firefox()


driver.get('https://food.oregonstate.edu/')

html = driver.page_source

driver.quit()


soup = BeautifulSoup(html, "html.parser")

# allHalls = soup.find(id = "hours").findAll('a')

open = False

# Get all unsorted lists under hours
# check if query matches the text of the first element in each ul (which is an a tag)
#   if so, print out all of the remaining children of that specific tag
while True:
    canFind = False
    diningHall = input("Enter a dining hall: ")
    allHalls = soup.find(id = "hours").findAll('li')
    for hall in allHalls:
        hallName = hall.find('a')
        if hallName != None:
            if diningHall == hallName.get_text():
                canFind = True
                timeSlots = hall.findAll('li')
                arrTimes = []
                # Adds each time to array
                for availableTime in timeSlots:
                    if availableTime.get_text() == 'Closed':
                        print(diningHall + " is currently closed")
                        break
                    arrTimes.append((availableTime.get_text()))
                print(arrTimes)
                now = datetime.now()
                converedArrTimes = []
                for ele in arrTimes:
                    converedArrTimes.append(timeConverter(ele))
                    print(ele)
                print(converedArrTimes)
                inTime = False

                for ele in converedArrTimes:
                    if ele[0] < now and ele[1] > now:
                        inTime = True

                if inTime:
                    print(diningHall + " is open!")
                else:
                    print(diningHall + " is closed")



                break
    if canFind != True:
        print("Please Try Again")
