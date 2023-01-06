import requests
import json

URL_PREFIX = 'https://store.epicgames.com/en-US/p/'

def isFree(promoDict):
    return not (promoDict in [None, [], {}] or promoDict['promotionalOffers'] in [None, [], {}])

def parseGame(gameJson):
    result = {}
    result['title'] = gameJson['title']
    result['image'] = gameJson['keyImages'][0]['url']
    result['endDate'] = gameJson['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
    result['url'] = URL_PREFIX + gameJson['catalogNs']['mappings'][0]['pageSlug']
    result['desc'] = gameJson['description']

    return result

def getFreeGames():
    result = requests.get(url='https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US')

    if (result.status_code == 200):
        scrape = json.loads(result.text)
        elements = scrape['data']['Catalog']['searchStore']['elements']

        freeGames = [g for g in elements if isFree(g['promotions'])]
        return freeGames

def scrape():
    thisWeek = getFreeGames()
    gameDict = [parseGame(g) for g in thisWeek]

    return gameDict