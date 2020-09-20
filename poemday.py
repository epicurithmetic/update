#     Task:
#
#       Scrape poem of the day from Poetry Foundation.
#       Display the poem in the updates.py terminal application.
#       Ask the user whether or not they wish to store this poem as a favourite.

# Task 1: Scrape the poem.
import requests
from bs4 import BeautifulSoup

def PotDAuthor():

    url_PotDAuthor = "https://www.poetryfoundation.org/poems/poem-of-the-day"
    response_PotDAuthor = requests.get(url_PotDAuthor)
    soup_PotDAuthor = BeautifulSoup(response_PotDAuthor.text, "html.parser")

    author_section = soup_PotDAuthor.find("span", class_="c-txt c-txt_attribution")
    author = author_section.text
    author_formatted = author.split("By ")[1][:-1] # Remove formatting and newline.
    return author_formatted

def PotDURL():

    url_PotDURL = "https://www.poetryfoundation.org/poems/poem-of-the-day"
    response_PotDURL = requests.get(url_PotDURL)
    soup_PotDURL = BeautifulSoup(response_PotDURL.text, "html.parser")

    PotDURL = soup_PotDURL.find("a", href="https://www.poetryfoundation.org/poems/49459/incantation")['href']
    return PotDURL

def PotDTitle():

    url_poem = PotDURL()
    response_title = requests.get(url_poem)
    soup_PotDURL = BeautifulSoup(response_title.text, "html.parser")

    title_messy = soup_PotDURL.find("h1", class_="c-hdgSans c-hdgSans_2 c-mix-hdgSans_inline").text
    title = title_messy.split(" "*20)[1] # HACK! May cause problems.
    title = title.split("\n")[0] # HACK! May cause problems.

    return title

def PotDPoem():

    url_poem = PotDURL()
    response_poem = requests.get(url_poem)
    soup_PotDURL = BeautifulSoup(response_poem.text, "html.parser")

    poem_section = soup_PotDURL.find("div", class_="c-feature-bd")
    poem = poem_section.findAll("div", style="text-indent: -1em; padding-left: 1em;")
    poem_full = ""
    for line in poem:
        poem_full += line.text +" \n"


    return poem_full[:-1]

# Task 2: Display the poem.
def PrintPoem():

    poem_author = PotDAuthor()
    poem_title = PotDTitle()
    poem_string = PotDPoem()
    poem_lines = poem_string.split("\n\r")
    spacing = 65

    print("\n" + " "*(spacing) + poem_title + "\n")
    for line in poem_lines[:-1]:
        print(" "*spacing + line)
    print("\n"+ " "*(spacing + 60) + "- " + poem_author)

# Task 3: Determine whether or not to add the poem to the database of favourites.
