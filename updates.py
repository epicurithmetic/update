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


print(" "*5 + "His Holiness, Jung, and Mythology: \n")

def HHtDL():

    url_HHtDL = "https://www.dalailama.com/"
    response_HHtDL = requests.get(url_HHtDL)
    soup_HHtDL = BeautifulSoup(response_HHtDL.text, "html.parser")

    latest_entry_title = soup_HHtDL.find("h2").text
    latest_entry_url = url_HHtDL[:-1] + soup_HHtDL.find("a",class_="button gold")["href"]

    return [latest_entry_title,latest_entry_url]

def jungianthology():

    url_jung = "https://jungchicago.org/blog/category/blog-posts/"
    response_jung = requests.get(url_jung)
    soup_jung = BeautifulSoup(response_jung.text, "html.parser")

    data_jung = soup_jung.find("h2",class_="excerpt-title")
    data_jung_finer = data_jung.find("a")

    title_blog = data_jung_finer.text
    url_blog = data_jung_finer["href"]

    return [title_blog, url_blog]

def myth_matters():

    url_mm = "https://mythologymatters.wordpress.com/"
    response_mm = requests.get(url_mm)
    soup_mm = BeautifulSoup(response_mm.text,"html.parser")

    data_mm = soup_mm.find("h2",class_="entry-title")
    data_mm_finer = data_mm.find("a")

    title_blog = data_mm_finer.text
    url_blog = data_mm_finer["href"]

    return [title_blog, url_blog]



print("\n")
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

#print("\n")
# Merriam-Webster word of the day.


print("\n")
# Blog updates.

blogs = ["Joel David Hampkins", "Matt Baker", "Godel's Lost Letter", "Annoying Precision", "Full Stack Python"]

number_of_blogs = len(blogs)
# First we write some function to grab the latest post each of the blogs.

# Joel David Hampkins: Mathematics and Philosophy of the infinite.
def jdh_headline():

    url_jdh = "http://jdh.hamkins.org/"
    response_jdh = requests.get(url_jdh)
    soup_jdh = BeautifulSoup(response_jdh.text, "html.parser")

    main_jdh = soup_jdh.find("h1", class_="entry-title")
    title_jdh = main_jdh.text

    return title_jdh

# Matt Baker's blog.
def baker_headline():

    url_baker = "https://mattbaker.blog/"
    response_baker = requests.get(url_baker)
    soup_baker = BeautifulSoup(response_baker.text, "html.parser")

    main_baker = soup_baker.find("h1", class_="entry-title")
    title_baker = main_baker.text

    return title_baker

# # Logic Matters
# def logic_matters():
#
#     url_logic = "https://www.logicmatters.net/blogfront/"
#     response_logic = requests.get(url_logic)
#     soup_logic = BeautifulSoup(response_logic.text, "html.parser")
#
#     main_logic = soup_logic.find("h1", class_="entry-title")
#     title_logic = main_logic.text
#
#     return title_logic

# Godels lost letter
def godel_letter():

    url_godel = "https://rjlipton.wordpress.com/"
    response_godel = requests.get(url_godel)
    soup_godel = BeautifulSoup(response_godel.text, "html.parser")

    # First pick out the section containing recent post.
    section_godel = soup_godel.find("div", id = "content", class_="pad")

    # Now pick out the title part of the HTML.
    main_godel = section_godel.find("h2")
    title_godel = main_godel.text

    return title_godel

# Annoying Precision
def annoying_precision():

    url_annoying_precision = "https://qchu.wordpress.com/"
    response_annoying_precision = requests.get(url_annoying_precision)
    soup_annoying_precision = BeautifulSoup(response_annoying_precision.text, "html.parser")

    # First pick out the section containing recent post.
    section_annoying_precision = soup_annoying_precision.find("div", class_="posttitle")

    # Now pick out the title part of the HTML.
    main_annoying_precision = section_annoying_precision.find("h2")
    title_annoying_precision = main_annoying_precision.text

    return title_annoying_precision

# Full stack python (blog)
def fullstack_python():

    url_python = "https://www.fullstackpython.com/blog.html"
    response_python = requests.get(url_python)
    soup_python = BeautifulSoup(response_python.text, "html.parser")

    # Zero in on the information.
    section_python = soup_python.find("div", class_="c9")

    blog_link = url_python + section_python.find("a")["href"]
    blog_title = section_python.find("a").text

    return blog_title

# These functions get the most recent blog titles.
blogs_functions = [jdh_headline(), baker_headline(),godel_letter(),annoying_precision(),fullstack_python()]

# Get the latest blog titles.
new_blogs = []
for blog in blogs_functions:
    new_blogs.append(blog)

# Read in the data from the last time we checked the blog.
blogs_in_database = []
blog_database = open("blog_database.txt","r")
for i in range(0,number_of_blogs):
    data = blog_database.readline()
    data_list = data.split(":& ")
    blog_title = data_list[1].replace("\n","")  # Clean EOL command.
    blogs_in_database.append(blog_title)

# Close the file.
blog_database.close()

# Print the latest blog titles. If they are different from the last check, then
# print a [New!] with the title name.
print(" "*5 + "Latest entries of your favourite blogs: \n")
for i in range(0,number_of_blogs):

    if new_blogs[i] == blogs_in_database[i]:
        print(" "*10 + blogs[i] + ": " + new_blogs[i])
    else:
        print(" "*10 + blogs[i] + ": " + new_blogs[i] + " [New!]")

# Now we can update the database with the new release information.
file = open("blog_database.txt","w")
for i in range(0,number_of_blogs):
    if i == 0:
        new_data = blogs[i] + ":& " + new_blogs[i]
        file.write(new_data)
    else:
        new_data = "\n" + blogs[i] + ":& " + new_blogs[i]
        file.write(new_data)

file.close()






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
print("\n")
print(x + y*169 + x)
print(x + y*169 + x)

# Now there should be a series of commands which allow the user to open
# any of the stories they would like to read. Furthermore, a full list of
# RNZ stories could be provided: perhaps particular sections could be
# asked for i.e. just the In Depth section.

# In order to be 100% advertisement free, I should print the body of the stories
# in the terminal, rather than jumping to the webpage.

"\n"
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
