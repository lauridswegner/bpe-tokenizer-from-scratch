# script to scrape the rots script and
# cleaning the data, parsing it into a txt
#
# NOTE
# This script will become obsolete, once the website's structure changes
#
import requests
from bs4 import BeautifulSoup

# url to desired movie script
url = "https://imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html"

# fetch the html content
response = requests.get(url)
webpage_content = response.text

# parse the html content
soup = BeautifulSoup(webpage_content, 'html.parser')

script_text = soup.find(class_='scrtext').text.split("\n")

# exlude empty elements and remove "\r" within iterated element
filtered_list = [element.rstrip("\r") for element in script_text if element.strip()]

# removing the footer
spliced_list = filtered_list[:-5]

# write into txt-file
with open("rots.txt", "w") as file:
    for line in spliced_list:
        file.write("%s\n" % line)
    print("The force will be with you, always.")
