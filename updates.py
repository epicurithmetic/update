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
y = "-"                     # This could be decorated more with some simple
                            # cellular automata. Using a RNG we could provide
                            # a new graphic with each update.
print(x + y*169 + x)        # Take from a list of "interesting rules" a random
print(x + y*169 + x)        # rule to make things different each time. 

# Print the time
print("Date: " + local_time)
print(" ")

# Reminders
print(" "*55 + x + y*50 + x)
print("\n" +  " "*60 + "Reminders: \n")

print(" "*70 + "1. Neck and back stretches")
print(" "*70 + "2. Meditation with Sam Harris")
print(" "*70 + "3. Two hours of coding")

print("\n")
print(" "*55 + x + y*50 + x)
print("\n")
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

#print("\n")
# Weather forecast

print("\n")
# Music updates bandcamp pages
print(" "*5 + "Latest releases from your favourite record labels and artists: \n")

arist_list = ["Ultimae",
              "Synphaera",
              "Exosphere",
              "White Label Records",
              "Carbon Based Lifeforms",
              "Hydrangea",
              "Abul Mogard",
              "Faint",
              "Solar Fields",
              "Trentemoller",
              "Alfa Mist"]

# Read in the data from the last time we checked.
N = len(arist_list)
bandcamp_old_release_data = []
bandcamp_database = open("bandcamp_database.txt","r")

for i in range(0,N):
    data = bandcamp_database.readline()
    data_list = data.split(":& ")
    release_name = data_list[1].replace("\n","")    # Cleans the EOL command.
    bandcamp_old_release_data.append(release_name)

# Close the file.
bandcamp_database.close()

def bandcamp_latest_release(url):

    url_artist_discog = url
    response_artist_discog = requests.get(url_artist_discog)
    soup_artist_discog = BeautifulSoup(response_artist_discog.text, "html.parser")

    data_artist_discog = soup_artist_discog.find("p", class_="title")
    newest_artist_discog = data_artist_discog.text

    return newest_artist_discog

# Create a list of URL to loop-through:
bandcamp_list = ["https://ultimae.bandcamp.com/",
                 "https://synphaera.bandcamp.com/",
                 "https://exospheremusic.bandcamp.com/",
                 "https://whitelabrecs.bandcamp.com/music",
                 "https://carbonbasedlifeforms.bandcamp.com/music",
                 "https://hydrangea.bandcamp.com/",
                 "https://abulmogard.bandcamp.com/",
                 "https://faintmusic.bandcamp.com/",
                 "https://solarfields.bandcamp.com/",
                 "https://trentemoller.bandcamp.com/",
                 "https://alfamist.bandcamp.com/music"]

# This function cleans the format of the scraped release_title.
def release_name_clean(raw_release_name):

    """
        This function cleans the release name.

        When I scrape the release name, there is often a lot of
        extra text in the string. For example, the artist name
        and a lot of spaces and new line commands.

    """

    # First remove any newline commands.
    raw_release_name = raw_release_name.replace("\n","")

    # Get rid of the arist name by splitting by a fixed number of spaces.
    split_release_name = raw_release_name.split("              ",1)

    # Get rid of the spaces at the beginning of the release name.
    release_name_string = split_release_name[0]
    release_name_list = list(release_name_string)
    while release_name_list[0] == " ":
        del release_name_list[0]
    # Remove spaces from the start of the release name.

    clean_release_name = ""
    for a in release_name_list:
        clean_release_name += a

    return clean_release_name

# Store all the titles in a list.
newest_releases = []
for url in bandcamp_list:
    raw_release_title = bandcamp_latest_release(url)
    clean_release_title = release_name_clean(raw_release_title)
    newest_releases.append(clean_release_title)

# Print the most recent release titles. If a title has changed since the last
# update, then indicate this with a [New!] printed next to the title.
for i in range(0,N):

    if newest_releases[i] == bandcamp_old_release_data[i]:
        print(" "*10 + arist_list[i] +": " + newest_releases[i])
    else:
        print(" "*10 + arist_list[i] +": " + newest_releases[i] + " [New!]")
        print(newest_releases[i])
        print(bandcamp_old_release_data[i])

# Now we can update the database with the new release information.
file = open("bandcamp_database.txt","w")
for i in range(0,N):
    if i == 0:
        new_data = arist_list[i] + ":& " + newest_releases[i]
        file.write(new_data)
    else:
        new_data = "\n" + arist_list[i] + ":& " + newest_releases[i]
        file.write(new_data)

file.close()

print("\n")
# Merriam-Webster word of the day

#print("\n")
# Friends ArXiv updates. Jim, Simon, Ryan, Andrew, James Bonifacio. Semirings.

#print("\n")
# Dinner idea: recent PuL recipe.

# Cryptocurrency prices
# print(" "*5 + "Cryptocurrency summary: \n")
#
# def BitCoin_price():
#
#     # We will obtain the price from the following website.
#     url_bitcoin = "https://coinmarketcap.com/currencies/bitcoin/markets/"
#
#     # First for BitCoin.
#     response_bitcoin = requests.get(url_bitcoin)
#     soup_bitcoin = BeautifulSoup(response_bitcoin.text, "html.parser")
#
#     # For BitCoin.
#     data_bitcoin = soup_bitcoin.find("span", class_="cmc-details-panel-price__price")
#     price_bitcoin = data_bitcoin.text
#
#     return price_bitcoin
# def Ethereum_price():
#
#     # We will obtain the price from the following website.
#     url_ethereum = "https://coinmarketcap.com/currencies/ethereum/"
#
#     # HTML for Ethereum.
#     response_ethereum = requests.get(url_ethereum)
#     soup_ethereum = BeautifulSoup(response_ethereum.text, "html.parser")
#
#     # For Ethereum.
#     data_ethereum = soup_ethereum.find("span", class_="cmc-details-panel-price__price")
#     price_ethereum = data_ethereum.text
#
#     return price_ethereum
#
# print(" "*10 + "BitCoin  is currently worth " + BitCoin_price() + " (USD)")
# print(" "*10 + "Ethereum is currently worth " + Ethereum_price() + " (USD)")
#
# print("\n")
# # NZX prices
# print(" "*5 + "New Zealand Stock-Exchange summary: \n")
#
# print(" ")
print(x + y*169 + x)
print(x + y*169 + x)

# Now there should be a series of commands which allow the user to open
# any of the stories they would like to read. Furthermore, a full list of
# RNZ stories could be provided: perhaps particular sections could be
# asked for i.e. just the In Depth section.

# Open all RNZ stories the user wants to read.
rnz_reading = True
while rnz_reading == True:

    print("Would you like to read any of the RNZ stories? [Y/n]")
    user_rnzreading = input("")
    if user_rnzreading == "Y":
        print("Which story would you like to read? [1-10]")
        user_rnzstory = input("")
        user_rnzstory = int(user_rnzstory)
        story_url_read = rnz_stories[user_rnzstory - 1][1]
        webbrowser.open(story_url_read)
    else:
        rnz_reading = False

# Open all Quanta stories the user wants to read.
quanta_reading = True
while quanta_reading == True:

    print("Would you like to read any of the stories from Quanta Magazine? [Y/n]")
    user_quantareading = input("")
    if user_quantareading == "Y":
        print("Which story would you like to read? [1-10]")
        user_quantastory = input("")
        user_quantastory = int(user_quantastory)
        story_url_read = quanta_stories[user_quantastory - 1][1]
        webbrowser.open(story_url_read)
    else:
        quanta_reading = False



# Close.
print("\n" + " "*10 + "Now you are all up to date. Enjoy your day." + "\n\n")
