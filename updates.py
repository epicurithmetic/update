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
print("Your updates are as follows: \n")


# RNZ headlines
print("Radio New Zealand Headlines: ")

# Quanta stories

# Cryptocurrency prices
print("Cryptocurrency summary: \n ")

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


# NZX prices

# Weather forecast

# Dinner idea: recent PuL recipe. 


print(" ")
print(x + y*169 + x)
print(x + y*169 + x)
