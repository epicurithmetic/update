# Script to run in the morning to update me on the websites and information
# that interest me.
import os
import time
import webbrowser
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
print(" "*5 + "Radio New Zealand headlines: \n  ")
def RNZHeadlines():

    """
        This function retrieves all headlines (and the urls of the stories)
        from the homepage of the Radio New Zealand website.

        This function returns a list, the elements of which are lists of the
        form: [headline,url]

    """

    url_rnz = "https://www.rnz.co.nz/"
    response_rnz = requests.get(url_rnz)
    soup_rnz = BeautifulSoup(response_rnz.text, "html.parser")

    headlines = []

    # Grab the headlines.
    main = soup_rnz.find_all("h3", class_="o-digest__headline")

    for story in main:
        headline = story.text
        link_data = story.find("a", class_="faux-link")
        link = url_rnz[:-1] + link_data['href']

        headlines.append([headline,link])


    return headlines

rnz_stories = RNZHeadlines()
count_rnz = 0
while count_rnz < 10:
    print(" "*10 + str(count_rnz + 1) + ". " + rnz_stories[count_rnz][0])
    count_rnz += 1


print("\n")
# Quanta stories
print(" "*5 + "Quanta Magazine headlines: \n  ")
def QuantaHeadlines():

    """
        This function gets headlines and the links for the stories
        from the homepage of the Quanta Magazine webpage.

        This function returns a list whose entries are themselves lists
        of the form: [headline, story_url]

    """

    url_quanta = "https://www.quantamagazine.org/"
    response_quanta = requests.get(url_quanta)
    soup_quanta = BeautifulSoup(response_quanta.text, "html.parser")

    headlines = []

                        # Main headline
    # This zeroes in on the HTML for the main headline.
    main_data = soup_quanta.find("div", class_="hero-title pb2")

    # First we can get the headline.
    headline_data = main_data.find("h1", class_="noe mv0 h0 color-transition hover--orange")
    headline_text = headline_data.text

    # Next we can get the link for this story.
    link_data = main_data.find_all("a")                            # Note: We have to do some hack here to get the link
    link_data_relevant = link_data[1]                              #       to the story and not to the "tag" under which
    headline_link = url_quanta[:-1] + link_data_relevant['href']   #       the story is classified e.g. Abstractions blog.
                                                                   #       So I assumed the link for the story will be the
    # Add this to the list of headlines.                           #       second link collected. This may cause trouble!
    headlines.append([headline_text, headline_link])

                    # Next block of stories
    more_data = soup_quanta.find_all("div", class_="card__content")

    for story in more_data:

        # Get the headline.
        more_headline_data = story.find("h2", class_="card__title noe mv0 theme__accent-hover transition--color")
        more_headline = more_headline_data.text

        # Get the URL.
        more_link_data_list = story.find_all("a")
        more_link_data_relevant = more_link_data_list[1]
        more_headline_link = url_quanta[:-1] + more_link_data_relevant["href"]

        # Add this data to the list.
        headlines.append([more_headline, more_headline_link])

    return headlines


quanta_stories = QuantaHeadlines()
i = 1
for story in quanta_stories:
    print(" "*10 + str(i) + ". " + story[0])
    i += 1

print("\n")
# Cryptocurrency prices
print(" "*5 + "Cryptocurrency summary: \n")

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
print(" "*5 + "New Zealand Stock-Exchange summary: \n")

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

# Now there should be a series of commands which allow the user to open
# any of the stories they would like to read. Furthermore, a full list of
# RNZ stories could be provided: perhaps particular sections could be
# asked for i.e. just the In Depth section.


#webbrowser.open(quanta_stories[0][1]) - This works, after uninstalling Internet Explorer.
