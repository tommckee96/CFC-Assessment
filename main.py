import requests
from bs4 import BeautifulSoup
import re
import json

CONST_INDEX_DOMAIN = "cfcunderwriting.com"
CONST_INDEX_URL = "https://www." + CONST_INDEX_DOMAIN


def main():
    index_page = requests.get(CONST_INDEX_URL)
    index_page_soup = BeautifulSoup(index_page.content, "html.parser")

    write_external_resources_to_json_file(index_page_soup)

    privacy_policy_subdirectory = get_privacy_policy_subdirectory(index_page_soup)

    privacy_policy_url = CONST_INDEX_URL + privacy_policy_subdirectory

    privacy_policy_page = requests.get(privacy_policy_url).text
    privacy_policy_page_soup = BeautifulSoup(privacy_policy_page, "html.parser")
    #print(privacy_policy_page_soup.get_text())

    data = privacy_policy_page_soup.findAll(text=True)



def write_external_resources_to_json_file(soup):
    """Function to write list of all external resources on page to JSON file"""

    # Construct list of dicts containing attributes of each element containing a link to an external resource
    ext_res_dict_list = []

    for tag in soup.find_all():
        link = ''
        if 'href' in tag.attrs:
            link = tag['href']
        elif 'src' in tag.attrs:
            link = tag['src']

        if link[:4] == 'http' and re.compile(CONST_INDEX_DOMAIN).search(link) is None:
            ext_res_dict_list.append(tag.attrs)


    # Write dict list to json file
    with open('external_resources.json', 'w', encoding='utf-8') as f:
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
