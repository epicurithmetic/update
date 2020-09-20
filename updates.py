# Script to run in the morning to update me on the websites and information
# that interest me.
import os
import time
import sqlite3
import requests
import webbrowser
from bs4 import BeautifulSoup

# This function is used to present a poem from the Poetry Foundation.
from poemday import PrintPoem

# Generate the time in a user friendly format.
seconds = time.time()
local_time = time.ctime(seconds)

# Clear the terminal
# os.system("cls")        # Only works on microsoft machines.
os.system("clear")        # Linux option.

# Some simple graphics to frame the update.
x = "|||"
y = "-"                     # This could be decorated more with some simple
                            # cellular automata. Using a RNG we could provide
                            # a new graphic with each update.
print(x + y*205 + x)        # Take from a list of "interesting rules" a random
print(x + y*205 + x)        # rule to make things different each time.

# Print the time
print("Date: " + local_time)
print(" ")

# Reminders
print(" "*75 + x + y*50 + x)
print("\n" +  " "*80 + "Reminders: \n")

print(" "*90 + "1. Neck and back stretches")
print(" "*90 + "2. Yoga with Adriene")
print(" "*90 + "3. Meditation with Sam Harris")
print(" "*90 + "4. Two hours of computer study")

print("\n")
print(" "*75 + x + y*50 + x)
print("\n")
# Greeting
print(" "*20 + "Greetings Robert. \n")
#print(" "*30 + "Your requested updates are as follows: \n")

# Idea: print a poem of interest or quote to begin the update. Create a library
#       of interesting things to print and pick at random when the script runs.


# -----------------------------------------------------------------------------
# ----------------- Here is the birthday reminder code ------------------------
# -----------------------------------------------------------------------------
# Enter the information from MAP database.
# The next functions will allow us to determine whether today is someones
# birthday, or a birthday will occur in the next week.
def map_birthdays(conn):

    sql_birthday = "SELECT first_name, last_name, dob FROM people;"

    cur = conn.cursor()
    cur.execute(sql_birthday)

    birthdays_raw = cur.fetchall()

    # Reformat the information.
    birthdays = []
    for entry in birthdays_raw:
        # [First+Last,dob] format of information.
        birthdays.append([entry[0]+ " " +entry[1],entry[2]])

    return birthdays

def present_day_month():

    # Get local time.
    seconds = time.time()
    local_time = time.ctime(seconds)

    # Both the current month and current day code could be written in their
    # own functions. Perhaps this is better style?

    # Get the current month:
    month_word = local_time[4:7]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month_number = str(months.index(month_word)+1)
    if len(month_number) == 1:              # This if statement puts the month in
        month_number = "0"+month_number     # the same format as that of the SQLite
    else:                                   # database month data.
        pass

    # Get the current day:
    day_raw = local_time[8:10]
    day = ""
    if day_raw[0] == " ":
        day = "0" + day_raw[1]
    else:
        day = day_raw

    today_date = day + "/" + month_number

    return today_date

def tse_ddmm(time_since_epoch):

    """
        This functions takes as input an int (str of int?) interpreting it
        as time since epoch and outputs the corresponding date in a string
        of the form: dd/mm (type str)

    """

    then_time = time.ctime(time_since_epoch)

    # Get the current month:
    month_word = then_time[4:7]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month_number = str(months.index(month_word)+1)
    if len(month_number) == 1:              # This if statement puts the month in
        month_number = "0"+month_number     # the same format as that of the SQLite
    else:                                   # database month data.
        pass

    # Get the current day:
    day_raw = then_time[8:10]
    day = ""
    if day_raw[0] == " ":
        # Time module documentation says there is a space buffer in the case
        # the date is a single digit day. We change the space to a 0...
        day = "0" + day_raw[1]
    else:
        # ... otherwise we do nothing.
        day = day_raw

    then_date = day + "/" + month_number

    return then_date

def whose_birthday_today(conn):

    map_birthday_list = map_birthdays(conn)
    l = len(map_birthday_list)
    day_month = present_day_month()

    # Aux list to store people whose birthday is today.
    birthday_today = []
    # Check birthdays against the database.
    for i in range(0,l):

        # Do the check person-by-person
        if map_birthday_list[i][1][0:5] == day_month:
            birthday_today.append(map_birthday_list[i][0])
        else:
            pass

    return birthday_today

def whose_birthday_week(conn):

    map_birthday_list = map_birthdays(conn)
    number_of_people = len(map_birthday_list)

    # Get local time.
    seconds_since_epoch = time.time()
    local_time = time.ctime(seconds_since_epoch)
    current_day = local_time[0:3]
    days_of_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    days_since_monday = days_of_week.index(current_day)

    # Seconds Since Epoch on the Monday of the present week.
    monday_time = seconds_since_epoch - days_since_monday*24*60*60

    # Now we want the date dd/mm for each day of the present week.
    dates_for_week = []
    for i in range(0,7):
        dates_for_week.append(tse_ddmm(monday_time + i*24*60*60))

    # Create a list to store the birthday information
    birthday_info = []

    # With the dates in hand, we can now check them against the MAP.db
    for i in range(0,number_of_people):

        # Check each person against each day of the week.
        for j in range(0,7):

            if map_birthday_list[i][1][0:5] == dates_for_week[j]:
                # Append birthday person's name and the days since Monday
                # i.e. the local variable j, on which the birthday falls.
                birthday_info.append([map_birthday_list[i][0],j])
            else:
                pass


    return birthday_info

# Obtain the birthday information from the database.
map_conn = sqlite3.connect("map.db")
birth_day = whose_birthday_today(map_conn)
l_day = len(birth_day)
#print(l_day)
birth_week = whose_birthday_week(map_conn)
l_week = len(birth_week)
#print(l_week)
days_of_week_full = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# Print the birthday information.
print("\n\n")
print(" "*3 + y*20 + " Birthday " + y*20)
print(" "*3 + y*20 + " Reminder " + y*20)
print("\n")

if (l_day == 0) and (l_week == 0):
    print(" "*5 + "Your friends and family do not have any\n" + " "*7 + "birthdays this week.")

elif (l_day == 0) and (not(l_week == 0)):
    print(" "*5 + "None of your friends or family have their" + "\n" + " "*7 + "birthday today.\n")
    print(" "*5 + "However the following birthdays fall this week:\n")
    for j in range(0,l_week):
        print(" "*10 + "%s (%s)" % (birth_week[j][0],days_of_week_full[birth_week[j][1]]))

elif (l_day == 1) and (l_week == 1):
    print(" "*5 + ("Today is %s's birthday."% birth_day[0]) + "\n\n" + " "*5 + "This is the only birthday this week." )

elif (l_day == 1) and (l_week >= 1):
    print(" "*5 + ("Today is %s's birthday. \n" % birth_day[0]))
    print(" "*5 + "The following birthdays fall during the week:\n")
    for k in range(0,l_week):
        print(" "*10 + "%s (%s)" % (birth_week[k][0],days_of_week_full[birth_week[k][1]]))

elif (l_day == l_week):
    print(" "*5 + "The following people have their birthday today:")
    for i in range(0,l_day):
        print(" "*10 + birth_day[j])
    print(" "*5 + "These are the only birthdays that fall this week.")

else:
    # The remaining cases (today > 1 and week > 1 and today =/= week) can
    # be handled in the final else statement.
    print(" "*5 + "The following people have their birthday today:" + "\n")
    for i in range(0,l_day):
        print(" "*10 + birth_day[i])
    print("\n" + " "*5 + "The following birthdays fall during the week:\n")
    for k in range(0,l_week):
        print(" "*10 + "%s (%s)" % (birth_week[k][0],days_of_week_full[birth_week[k][1]]))

print("\n\n")
print(" "*3 + y*50)
print(" "*3 + y*50)
print("\n")
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# This small part of the script presents the Poem of the Day from the Poetry Foundation.
print("\n\n")
print(" "*60 + x + y*85 + x)
print(" "*60 + x + y*85 + x)
print("\n")
print(" "*88 +"Poetry Foundation: Poem of the Day")
print("\n")
PrintPoem()


print(" "*5 + "Inner cosmos blogs: \n")

def HHtDL():

    url_HHtDL = "https://www.dalailama.com/news"
    response_HHtDL = requests.get(url_HHtDL)
    soup_HHtDL = BeautifulSoup(response_HHtDL.text, "html.parser")

    latest_entry_section = soup_HHtDL.find("div", class_="card")
    latest_entry_subsection = latest_entry_section.find("h3")

    latest_entry_url_section = latest_entry_subsection.find("a")
    latest_entry_url = latest_entry_url_section['href']
    latest_entry_title = latest_entry_subsection.text


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

def jbp_blog():

    url_jbp = "https://www.jordanbpeterson.com/"
    response_jbp = requests.get(url_jbp)
    soup_jbp = BeautifulSoup(response_jbp.text, "html.parser")

    # Zero-in on the relevant information.
    first_jbp = soup_jbp.find("h4")

    title_jbp = first_jbp.find("a").text
    blog_url_jbp = first_jbp.find("a")['href']

    return [title_jbp, blog_url_jbp]


def healing_psyche():

    url_healing = "https://www.thehealingpsyche.org/blog"
    response_healing = requests.get(url_healing)
    soup_healing = BeautifulSoup(response_healing.text, "html.parser")

    # Zero in on the relevant information.
    blog_title_healing = soup_healing.find("h2").text
    blog_title_healing = blog_title_healing[0] + blog_title_healing[1:].lower()   # This blog uses all CAPS, so this line cleans that up.
    blog_url_healing_first = soup_healing.find("div", id="comp-j6k92uwy_MediaLeftPage_PhotoPost__0_0_0_0_def_7")
    blog_url_healing = blog_url_healing_first.find("a")['href']

    return [blog_title_healing,blog_url_healing]

newest_blogs = [["Jordan B. Peterson", jbp_blog()],
                ["His Holiness the Dalai Lama", HHtDL()],
                ["Jungianthology", jungianthology()],
                ["Myth Matters", myth_matters()],
                ["Healing Pysche",healing_psyche()]]

blog_count = 1
for blog in newest_blogs:
    print(" "*10 + str(blog_count) + ". " + blog[0] + ": " + blog[1][0])
    blog_count += 1

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

        if not(link_data == None):
            link = url_rnz[:-1] + link_data['href']
            headlines.append([headline,link])
        else:
            pass

        #headlines.append([headline,link])


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
# Music updates bandcamp pages
bandcamp_intro = "Latest releases from your favourite record labels and artists:"
orbmag_intro = "Latest podcast and articles on Orbmag:"
print(" "*5 + bandcamp_intro + "\n")

artist_list = ["Ultimae",
              "Synphaera",
              "Exosphere",
              "White Label Records",
              "Carbon Based Lifeforms",
              "Hydrangea",
              "Grand River",
              "Abul Mogard",
              "Faint",
              "Solar Fields",
              "Trentemoller",
              "Alfa Mist",
              "Oddisee",
              "Bruno Sanfilippo",
              "1631 Recordings"]

# Read in the data from the last time we checked.
N = len(artist_list)
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
                 "https://grandrivermusic.bandcamp.com/",
                 "https://abulmogard.bandcamp.com/",
                 "https://faintmusic.bandcamp.com/",
                 "https://solarfields.bandcamp.com/",
                 "https://trentemoller.bandcamp.com/",
                 "https://alfamist.bandcamp.com/music",
                 "https://oddiseemmg.bandcamp.com/",
                 "https://brunosanfilippo.bandcamp.com/",
                 "https://1631recordings.bandcamp.com/"]

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

    # Get rid of the artist name by splitting by a fixed number of spaces.
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
    time.sleep(1)

# I want to print the ambient blog and orbmag beside bandcamp list.
# def ambient_blog():
#
#     url_ambient = "https://www.ambientblog.net/blog/"
#     response_ambient = requests.get(url_ambient)
#     soup_ambient = BeautifulSoup(response_ambient.text, "html.parser")
#
#     title_section = soup_ambient.find_all("h2", class_="entry-title", itemprop = "headline")
#
#     blog_entry_data = []
#
#     for entry in title_section:
#         entry_info = entry.find("a")
#         entry_title = entry_info.text
#         entry_url = entry_info["href"]
#
#         blog_entry = [entry_title,entry_url]
#         blog_entry_data.append(blog_entry)
#
#     return blog_entry_data
#
# def orbmag_podcast():
#
#     url_orbcast = "https://www.orbmag.com/music/"
#     response_orbcast = requests.get(url_orbcast)
#     soup_orbcast = BeautifulSoup(response_orbcast.text, "html.parser")
#
#     title_section = soup_orbcast.find("h3")
#     orbcast_title = title_section.find("a").text
#     orbcast_url = title_section.find("a")["href"]
#
#     return [orbcast_title,orbcast_url]
#
# def orbmag_news():
#
#     url_orbnews = "https://www.orbmag.com/news/"
#     response_orbnews = requests.get(url_orbnews)
#     soup_orbnews = BeautifulSoup(response_orbnews.text, "html.parser")
#
#     # Single out all of the new stories on the (first) news page.
#     articles_orbnews = soup_orbnews.find_all("article")
#
#     # I don't want updates about "EVENTS". I only want "NEWS" articles.
#     articles_just_orbnews = []
#     for story in articles_orbnews:
#         story_type = story.find("a").text
#         if story_type ==  "News":
#             articles_just_orbnews.append(story)
#         else:
#             pass
#
#     # Store the articles I am interested in here.
#     article_data = []
#
#     # For each "NEWS" story I need to go ahead and get the title and URL.
#     for story in articles_just_orbnews:
#         story_data = story.find("h3").find("a")
#         # Grab the relevant data.
#         story_url = story_data["href"]
#         story_title = story_data.text
#         # Append the data to the list.
#         article_data.append([story_title,story_url])
#
#     return article_data

# Print the most recent release titles. If a title has changed since the last
# update, then indicate this with a [New!] printed next to the title.
for i in range(0,N):

    if newest_releases[i] == bandcamp_old_release_data[i]:
        print(" "*10 + artist_list[i] +": " + newest_releases[i])
    else:
        print(" "*10 + artist_list[i] +": " + newest_releases[i] + " [New!]")

# Now we can update the database with the new release information.
file = open("bandcamp_database.txt","w")
for i in range(0,N):
    if i == 0:
        new_data = artist_list[i] + ":& " + newest_releases[i]
        file.write(new_data)
    else:
        new_data = "\n" + artist_list[i] + ":& " + newest_releases[i]
        file.write(new_data)

file.close()

#print("\n")
# Merriam-Webster word of the day.


print("\n")
# Blog updates.

blogs = ["Stephen Wolfram", "Joel David Hampkins", "Matt Baker",
        "Godel's Lost Letter", "Annoying Precision", "Full Stack Python",
        "The n-Category Cafe", "The Overflow", "Light Blue Touchpaper"]

number_of_blogs = len(blogs)
# First we write some function to grab the latest post each of the blogs.

# Stephen Wolfram's *writings* blog.
def wolfram_writings():

    url_wolf = "https://writings.stephenwolfram.com/"
    response_wolf = requests.get(url_wolf)
    soup_wolf = BeautifulSoup(response_wolf.text, "html.parser")

    latest_article_data = soup_wolf.find("article").find("a")

    article_title = latest_article_data.text
    article_url = latest_article_data["href"]

    return [article_title,article_url]

# Joel David Hampkins: Mathematics and Philosophy of the infinite.
def jdh_headline():

    url_jdh = "http://jdh.hamkins.org/"
    response_jdh = requests.get(url_jdh)
    soup_jdh = BeautifulSoup(response_jdh.text, "html.parser")

    main_jdh = soup_jdh.find("h1", class_="entry-title")
    title_jdh = main_jdh.text
    url_blog = main_jdh.find("a")["href"]

    return [title_jdh, url_blog]

# Matt Baker's blog.
def baker_headline():

    url_baker = "https://mattbaker.blog/"
    response_baker = requests.get(url_baker)
    soup_baker = BeautifulSoup(response_baker.text, "html.parser")

    main_baker = soup_baker.find("h1", class_="entry-title")
    title_baker = main_baker.a.text
    article_url = main_baker.a["href"]

    return [title_baker, article_url]

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
    article_url = main_godel.find("a")["href"]

    return [title_godel,article_url]

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
    article_url = main_annoying_precision.find("a")["href"]

    return [title_annoying_precision,article_url]

# Full stack python (blog)
def fullstack_python():

    url_python = "https://www.fullstackpython.com/blog.html"
    response_python = requests.get(url_python)
    soup_python = BeautifulSoup(response_python.text, "html.parser")

    # Zero in on the information.
    section_python = soup_python.find("div", class_="c9")

    blog_link = url_python + section_python.find("a")["href"]
    blog_title = section_python.find("a").text

    return [blog_title, blog_link]

# N-Cat lab.
def ncat_blog():

    url_ncat = "https://golem.ph.utexas.edu/category/"
    partial_url_ncat = "https://golem.ph.utexas.edu"
    response_ncat = requests.get(url_ncat)
    soup_ncat = BeautifulSoup(response_ncat.text, "html.parser")

    # Zero-in on the required information.
    main_ncat = soup_ncat.find("div", class_="extended")

    title_ncat = main_ncat.find("a").text
    url_blog_ncat = partial_url_ncat + main_ncat.find("a")['href']

    return [title_ncat, url_blog_ncat]

# Stack exchange blog
def stackoverflow_blog():

    url_overflow = "https://stackoverflow.blog/newsletter/"
    response_overflow = requests.get(url_overflow)
    soup_overflow = BeautifulSoup(response_overflow.text, "html.parser")

    # Zero-in on the required information.
    main_overflow = soup_overflow.find("h2")

    title_overflow = main_overflow.find("a")['title']
    url_blog_overflow = main_overflow.find("a")['href']


    return [title_overflow, url_blog_overflow]

# CyberSec blog.
def lbtouch():

    url_lbt = "https://www.lightbluetouchpaper.org"
    response_lbt = requests.get(url_lbt)
    soup_lbt = BeautifulSoup(response_lbt.text, "html.parser")

    main_lbt = soup_lbt.find("h1", class_="entry-title")
    blog_title_lbt = main_lbt.find("a").text
    blog_url_lbt = main_lbt.find("a")['href']

    return [blog_title_lbt,blog_url_lbt]

# These functions get the most recent blog titles.
blogs_functions = [wolfram_writings(), jdh_headline(), baker_headline(),
                    godel_letter(),annoying_precision(),fullstack_python(),
                    ncat_blog(),stackoverflow_blog(), lbtouch()]

# Get the latest blog titles.
new_blogs = []
for blog in blogs_functions:
    new_blogs.append(blog)
    time.sleep(1)

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
print(" "*5 + "Latest entries from your favourite mathematics and science blogs: \n")
for i in range(0,number_of_blogs):
    if new_blogs[i][0] == blogs_in_database[i]:
        print(" "*10 + str(i+1) + ". " + blogs[i] + ": " + new_blogs[i][0])
    else:
        print(" "*10 + str(i+1) + ". " + blogs[i] + ": " + new_blogs[i][0] + " [New!]")

# Now we can update the database with the new release information.
file = open("blog_database.txt","w")
for i in range(0,number_of_blogs):
    if i == 0:
        new_data = blogs[i] + ":& " + new_blogs[i][0]
        file.write(new_data)
    else:
        new_data = "\n" + blogs[i] + ":& " + new_blogs[i][0]
        file.write(new_data)

file.close()

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
# Store blog commands in a list
reading_commands = ["Would you like to read any of the spiritual blogs? [Y/n]",
                    "Would you like to read any of the RNZ stories? [Y/n]",
                    "Would you like to read any of the stories from Quanta Magazine? [Y/n]",
                    "Would you like to read any of the blog entries? [Y/n]"]

article_numbers = ["[1-4]","[1-10]","[1-10]",("[1-%d]" % number_of_blogs)]

blog_url_lists = [newest_blogs,rnz_stories,quanta_stories,new_blogs]
length_blog_list = len(blog_url_lists)

section_counter = 0
while section_counter < length_blog_list:

    # Ask the user if they would like to read any of the articles.
    print(reading_commands[section_counter])

    # Receive the user input.
    reading_yn = input("")

    # Act accordingly
    if reading_yn == "Y":

        # Ask which stories the user wants to read.
        stories = input("Enter the numbers corresponding to the stories you want to read seperated by commas: ")
        stories = stories.split(",")

        # Get all url for the current section.
        current_section_urls = []

        # Obtain the list of urls for the user.
        if section_counter == 0:
            # In this case we are getting the spiritual blogs.
            for blog in newest_blogs:
                current_section_urls.append(blog[1][1])
        else:
            # This case covers the format of the information obtained from
            # the remaining websites.
            for blog in blog_url_lists[section_counter]:
                current_section_urls.append(blog[1])

        # Open the stories in a browser.
        for x in stories:
            webbrowser.open(current_section_urls[int(x)-1])
    else:
        pass
    # Move onto the next blog.
    section_counter += 1

# Close.
print("\n" + " "*10 + "Now you are all up to date." + "\n\n")
