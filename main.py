import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def check_link(href):
    if href.startswith("http://www.techiedelight.com/"):
        return True
    return False


def construct_links():
    page = requests.get(
        "https://www.quora.com/q/techiedelight/500-Data-Structures-and-Algorithms-interview-questions-and-their-solutions"
    )

    soup = BeautifulSoup(page.content, "html.parser")
    links = []

    for link in soup.find_all("a", href=check_link):
        link_href = link["href"]
        question_name_raw = link_href.split("/")[-2].split("-")
        question_name = " ".join(question_name_raw)
        if question_name.startswith("www"):
            continue
        links.append((question_name, link_href))

    return links


config = {
  #config here
}
cred = credentials.ApplicationDefault()
app = firebase_admin.initialize_app(cred, config)
db = firestore.client()


def push_to_db():
    links = construct_links()
    for link in links:
        doc_ref = db.collection(u"questions").document(link[0])
        question = {u"name": link[0], u"url": link[1]}
        print("pushing " + link[0])
        doc_ref.set(question)


push_to_db()

# links = construct_links()
# print(len(links))
