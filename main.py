from wcag_zoo.validators.anteater import Anteater
from wcag_zoo.validators.molerat import Molerat
import requests
import pprint
from bs4 import BeautifulSoup
from wcag_zoo.validators.tarsier import Tarsier

URL = "http://127.0.0.1:8080/login.php"
URL_index = "http://127.0.0.1:8080/index.php"

proxies = {"http": "http://127.0.0.1:8081", "https": "http://127.0.0.1:8081"}

my_data = {'username': 'admin', 'password': 'password', "Login": "Login"}


def check_header(html):
    instance = Tarsier()
    results = instance.validate_document(html.encode("utf-8"))
    print("Header validation")
    print(results)
    print("\n")


def check_Anteater(html):
    instance = Anteater()
    results = instance.validate_document(html.encode("utf-8"))
    print("HTML image tags")
    print(results)
    print("\n")



def get_parse(url, post_data=None, dvwa=False):
    results = list()
    with requests.Session() as s:
        page = s.get(url, proxies=proxies, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")

        if dvwa:
            user_token = soup.find_all(attrs={"name": "user_token"})
            # get user token sent from client side
            my_data["user_token"] = user_token[0].get("value")

        check_header(page.text)
        check_Anteater(page.text)

        if post_data is not None:
            send = s.post(URL, data=my_data, proxies=proxies, verify=False)


get_parse("https://www.w3.org/WAI/demos/bad/before/home.html")
