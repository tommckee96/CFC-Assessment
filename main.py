import requests
from bs4 import BeautifulSoup
import re
import json


def main():
    index_url = "https://www.cfcunderwriting.com"
    index_page = requests.get(index_url)

    soup = BeautifulSoup(index_page.content, "html.parser")

    # Construct list of dicts containing attributes of each element containing a link to an external resource
    ext_res_dict_list = []
    for tag in soup.find_all(src=re.compile('^http')):
        ext_res_dict_list.append(tag.attrs)
    for tag in soup.find_all(href=re.compile('^http')):
        ext_res_dict_list.append(tag.attrs)

    # Write dict list to json file
    with open('resources.json', 'w', encoding='utf-8') as f:
        json.dump(ext_res_dict_list, f, ensure_ascii=False, indent=4)

    # hyperlinks = soup.findAll('a')

    # print(hyperlinks)

    # privacy_policy_html_elem = soup.find("a", string="Privacy policy")
    # privacy_policy_url = index_url + privacy_policy_html_elem['href']
    # print(privacy_policy_url)


main()
