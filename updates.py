# Script to run in the morning to update me on the websites and information
# that interest me.
import os
import time
import requests
from bs4 import BeautifulSoup


# Generate the time in a user friendly format.
seconds = time.time()
local_time = time.ctime(seconds)

# Clear the terminal
os.system("cls")

# Some simple graphics to frame the update.
x = "|||"
y = "-"

print(x + y*169 + x)
print(x + y*169 + x)

# Print the time
print("Date: " + local_time)
print(" ")

# Greeting
print("Greetings Robert. \n")
print("Your requested updates are as follows: \n")


# RNZ headlines
#print("Today's Radio New Zealand headlines: ")

# Quanta stories
print(" "*5 + "Today's Quanta Magazine headlines: \n  ")
def QuantaHeadlines():

    url_quanta = "https://www.quantamagazine.org/"
    response_quanta = requests.get(url_quanta)
    soup_quanta = BeautifulSoup(response_quanta.text, "html.parser")

    headlines = []

    # This gets the primary headline on the homepage.
    main = soup_quanta.find("h1", class_="noe mv0 h0 color-transition hover--orange")
    headlines.append(main.text)

    # This gets the rest of the stories on the homepage.
    sub_headlines = soup_quanta.find_all("h2", class_="card__title noe mv0 theme__accent-hover transition--color")
    for x in sub_headlines:
        headlines.append(x.text)

    return headlines

quanta_stories = QuantaHeadlines()
i = 1
for story in quanta_stories:
    print(" "*10 + str(i) + ". " + story)
    i += 1

print("\n")
# Cryptocurrency prices
print(" "*5 + "Here is the summary of the cryptocurriencies you're interested in: \n")

def BitCoin_price():

    # We will obtain the price from the following website.
    url_bitcoin = "https://coinmarketcap.com/currencies/bitcoin/markets/"

    # First for BitCoin.
    response_bitcoin = requests.get(url_bitcoin)
    soup_bitcoin = BeautifulSoup(response_bitcoin.text, "html.parser")

    # For BitCoin.
    data_bitcoin = soup_bitcoin.find("span", class_="cmc-details-panel-price__price")
    price_bitcoin = data_bitcoin.text

    return price_bitcoin
def Ethereum_price():

    # We will obtain the price from the following website.
    url_ethereum = "https://coinmarketcap.com/currencies/ethereum/"

    # HTML for Ethereum.
    response_ethereum = requests.get(url_ethereum)
    soup_ethereum = BeautifulSoup(response_ethereum.text, "html.parser")

    # For Ethereum.
    data_ethereum = soup_ethereum.find("span", class_="cmc-details-panel-price__price")
    price_ethereum = data_ethereum.text

    return price_ethereum

print(" "*10 + "BitCoin  is currently worth " + BitCoin_price() + " (USD)")
print(" "*10 + "Ethereum is currently worth " + Ethereum_price() + " (USD)")

print("\n")
# NZX prices
print(" "*5 + "These are the prices of the NZX stocks that you want to keep an eye on: \n")

print("\n")
# Weather forecast

print("\n")
# Music updates bandcamp pages
# Ultimae, Synphaera, Carbon Based Lifeforms, White Label Records, 1631 Recordings

print("\n")
# Merriam-Webster word of the day
#print("Today's word of the day is: " + MW_WotD)

print("\n")
# Dinner idea: recent PuL recipe.


print(" ")
print(x + y*169 + x)
print(x + y*169 + x)
