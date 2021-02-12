# Hunter Graves
# 30/1/2021
# epicPrint.py

# Discord rewrite (discord.py) bot extension that scrapes Epic's website for weekly free games.
# Will retrieve only on Thursdays, at 11a (minutes not considered)
# Will retrieve all games available until the next 'epic day' (Thursday, 11a)

# call epicPrint.scrape() to get information

# Returns information in the form as follows:
# [ (image URL, game title, link to store page, offer window) ]

# Example:
# [https://cdn1.epicgames.com/73b62f4875a248d8acc95966ce94c80f/offer/EGS_DandaraTrialsofFearEdition_LongHatHouse_S1-2560x1440-d20ffd22ba6944939635a2af807d3610.jpg?h=480&resize=1&w=854,
#       Dandara: Trials of Fear Edition, https://www.epicgames.com/store/en-US/product/dandara, Free Now - Feb 04 at 11:00 AM) ,
#   (https://cdn1.epicgames.com/epic/offer/Diesel_productv2_for-the-king_EGS_IronOakGames_ForTheKing_G1C_00-1920x1080-fe6c412cac9a22dd1a9df2eeab05d0a3cd34761b-1920x1080-60e45fce935660131ba319296fe00037.jpg?h=480&resize=1&w=854,
#       For The King, https://www.epicgames.com/store/en-US/product/for-the-king/home, Free Feb 04 - Feb 11)]

import datetime
import selenium
from selenium import webdriver

# parseData(elem) returns a 5-tuple containing normalized information retrieves from children
# of elem.
def parseData(elem):
    # start by getting the image
    imageElem = elem.find_element_by_xpath('.//img')
    imageLink = imageElem.get_attribute('src')

    # get the flavor text
    textElem = elem.find_element_by_xpath('.//span[@data-testid="offer-title-info-title"]').text
    linkElem = elem.find_element_by_xpath('.//a[@aria-label]').get_attribute('href')
    timeElem = elem.find_element_by_xpath('.//span[@data-testid="offer-title-info-subtitle"]').text
    
    if 'Free Now' not in timeElem:
        return []
    
    return (imageLink,textElem,linkElem,timeElem)

# getWeeklyGames() launches the chrome driver and retrives the information from epicgames.com
# Also removes games from the results if the offer doesn't begin this Epic Day.
# Returns a list of 4-tuple containing element information.
def getWeeklyGames():
    # set the browser options to headless to get rid of the dumb chrome window
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')

    # start the driver up and got to EPIC
    driver = webdriver.Chrome('chromedriver')#, options=chrome_options)
    driver.get('https://www.epicgames.com/store/en-US/free-games')
    
    # go ahead and grab elements and then parse through
    elemList = driver.find_elements_by_xpath("//div[@data-component='WithClickTrackingComponent']")
    gamesList = [parseData(e) for e in elemList]
    
    finalList = [g for g in gamesList if g]
    
    driver.close()
    return finalList
    
# master function.
# Returns a list of 4-tuple scraped from epicgames.com
def scrape():
    return getWeeklyGames()