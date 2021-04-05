from wcag_zoo.validators.anteater import Anteater
from wcag_zoo.validators.molerat import Molerat
import json
import requests
import os
from bs4 import BeautifulSoup
from wcag_zoo.validators.tarsier import Tarsier

URL = "http://127.0.0.1:8080/login.php"
URL_index = "http://127.0.0.1:8080/index.php"

proxies = {"http": "http://127.0.0.1:8081", "https": "http://127.0.0.1:8081"}

my_data = {'username': 'admin', 'password': 'password', "Login": "Login"}


def check_header(html):
    instance = Tarsier()
    results = instance.validate_document(html.encode("utf-8"))
    #print("Header validation")
    #print(results)
    print("\n")


def check_Anteater(html):
    instance = Anteater()
    results = instance.validate_document(html.encode("utf-8"))
    f = open("C:\\programming\\results.txt", "w+")
    f.write(json.dumps(results, indent=4))
    print("HTML image tags")
    print(results)
    print("\n")


def get_parse(url, post_data=None, dvwa=False):
    results = list()
    with requests.Session() as s:
        page = s.get(url, proxies=proxies, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        get_css(soup, url)
        if dvwa:
            user_token = soup.find_all(attrs={"name": "user_token"})
            # get user token sent from client side
            my_data["user_token"] = user_token[0].get("value")

        check_header(page.text)
        check_Anteater(page.text)

        if post_data is not None:
            send = s.post(URL, data=my_data, proxies=proxies, verify=False)


def get_absolute_css_url(url, css_path):
    url = url.split("/")
    css_path = css_path.split("/")
    # remove last element
    url = url[:-1]
    for items in css_path:
        if items == "..":
            url = url[:-1]
        else:
            url.append(items)
    url = "/".join(url)
    return url


def get_css(soup, url):
    css_tags = soup.findAll("link", href=True)
    print("HERE")
    for css_tag in css_tags:
        css_path = css_tag.get("href")
        if ".css" in css_path:
            css_url = get_absolute_css_url(url, css_path)
            css_content = requests.get(css_url).text

            dir_name = os.getcwd()
            abs_filepath = os.path.join(dir_name, css_path)

            if not os.path.exists(os.path.dirname(abs_filepath)):
                os.makedirs(os.path.dirname(abs_filepath))

            f = open(abs_filepath, "w+")
            f.write(str(css_content))

    # for css_tag in css_tags:

    pass


def clear_up():
    pass


def get_js(html):
    pass


get_parse("https://www.w3.org/WAI/demos/bad/before/home.html")
