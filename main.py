import requests
from bs4 import BeautifulSoup
import re
import json

CONST_INDEX_URL = "https://www.cfcunderwriting.com"


def main():
    index_page = requests.get(CONST_INDEX_URL)

    soup = BeautifulSoup(index_page.content, "html.parser")

    write_external_resources_to_json_file(soup)

    # Enumerate the hyperlinks
    privacy_policy = get_privacy_policy_url(soup)

    print(privacy_policy)


def write_external_resources_to_json_file(soup):
    """Function to write list all external resources on page to JSON file"""

    # Construct list of dicts containing attributes of each element containing a link to an external resource
    ext_res_dict_list = []
    for tag in soup.find_all(src=re.compile('^http')):
        ext_res_dict_list.append(tag.attrs)
    for tag in soup.find_all(href=re.compile('^http')):
        ext_res_dict_list.append(tag.attrs)

    # Write dict list to json file
    with open('external_resources.json', 'w', encoding='utf-8') as f:
        json.dump(ext_res_dict_list, f, ensure_ascii=False, indent=4)


def get_privacy_policy_url(soup):
    """Returns the href of the privacy policy

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
