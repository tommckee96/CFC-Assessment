import requests
from bs4 import BeautifulSoup
import re
import json

CONST_INDEX_DOMAIN = "cfcunderwriting.com"
CONST_INDEX_URL = "https://www." + CONST_INDEX_DOMAIN
CONST_EXTERNAL_RESOURCES_LIST_FILENAME = 'external_resources.json'
CONST_WORD_FREQUENCY_COUNT_FILENAME = 'word_frequency_count.json'


def main():
    # Scrape index webpage and parse to BeautifulSoup object
    index_page = requests.get(CONST_INDEX_URL)
    index_page_soup = BeautifulSoup(index_page.content, "html.parser")

    # Write list of all external resources to JSON output file
    write_external_resources_to_json_file(index_page_soup, CONST_EXTERNAL_RESOURCES_LIST_FILENAME)

    # Enumerate page's hyperlinks and retrieve the URL of the privacy policy page
    privacy_policy_subdirectory = get_privacy_policy_subdirectory(index_page_soup)
    privacy_policy_url = CONST_INDEX_URL + privacy_policy_subdirectory
    
    # Scrape privacy policy page and parse to BeautifulSoup object
    privacy_policy_page = requests.get(privacy_policy_url)
    privacy_policy_page_soup = BeautifulSoup(privacy_policy_page.content, "html.parser")

    # Retrieve all static text on the page (newsletter section excluded)
    privacy_policy_content = privacy_policy_page_soup.find(id='main')
    sitemap = privacy_policy_page_soup.find(class_='sitemap')
    header = privacy_policy_page_soup.find(id='header')
    text = privacy_policy_content.text + ' ' + sitemap.text + ' ' + header.text

    # Write case-insensitive frequency count to JSON file
    generate_frequency_count(text, CONST_WORD_FREQUENCY_COUNT_FILENAME)


def generate_frequency_count(text, json_filename):
    """Writes a word frequency count to a JSON file

    Parameters:
        :text - string that the word frequency count will be generated from
        :json_filename - string with name of JSON file that frequency count will be written to
    """

    # Remove all words containing a number or @ symbol such as postcodes and email addresses
    text = ' '.join(s for s in text.split() if not any(c.isdigit() or c == '@' for c in s))

    # Replace all non-alphabetic characters with a space
    text = re.sub('[^a-zA-Z]+', ' ', text.lower())

    word_list = text.split()

    # Generate word and frequency pair dictionary
    freq_count = {}
    for word in word_list:
        if word in freq_count:
            freq_count[word] = freq_count[word] + 1
        else:
            freq_count[word] = 1

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(freq_count, f, indent=4)


def write_external_resources_to_json_file(soup, json_filename):
    """Function to write list of all external resources on page to JSON file

    Parameters:
    :soup - BeautifulSoup4 object representation of HTML page
    :json_filename - string containing name of JSON file that will be written to
    """

    # Construct list of dicts containing attributes of each element containing a link to an external resource
    ext_res_dict_list = []

    for tag in soup.find_all():
        link = ''
        if 'href' in tag.attrs:
            link = tag['href']
        elif 'src' in tag.attrs:
            link = tag['src']

        resource_is_external = re.compile(CONST_INDEX_DOMAIN).search(link) is None
        if link[:4] == 'http' and resource_is_external:
            ext_res_dict_list.append(tag.attrs)

    # Write dict list to json file (list of json)
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(ext_res_dict_list, f, ensure_ascii=False, indent=4)


def get_privacy_policy_subdirectory(soup):
    """Returns the subdirectory of the privacy policy

    Parameters:
        :bs4.BeautifulSoup - soup object representation of the whole page

    Returns:
        :string - the href of the privacy policy
    """

    # Enumerate the hyperlink tags
    hyperlinks = soup.find_all('a')

    # Iterate over hyperlinks until tag containing string 'privacy policy' is found
    for i in range(len(hyperlinks)):
        if hyperlinks[i].text.lower() == 'privacy policy':
            return hyperlinks[i]['href']


main()
