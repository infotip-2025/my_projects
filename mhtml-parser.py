# Import our libraries
from bs4 import BeautifulSoup  ## the BeautifulSoup library for scraping from the bs4 package
import requests ## Establish website connection using the requests library

soup = BeautifulSoup(txt, 'html.parser')

# locate <script> with XML data
script = soup.select_one('script#myXML')

# parse the XML data
xml_soup = BeautifulSoup(script.contents[0], 'html.parser')

# get data
all_data = []
for each_eaction in xml_soup.select('EachAction'):
    all_data.append({'ActionNumber': each_eaction['actionnumber'],
                     'Time':each_eaction['time'],
                     'FileDescription':each_eaction['filedescription'],
                     'Action':each_eaction.find('action').get_text(strip=True)})

# print data:
for line in all_data:
    print('{:<30}{:<30}{:<30}{:<30}'.format(*line.values()))
    