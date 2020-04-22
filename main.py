import psycopg2
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://postgrespro.ru"
PAGES = ["/docs/postgrespro/11/preface", "/docs/postgrespro/11/intro-whatis", "/docs/postgrespro/11/intro-pgpro-vs-pg"]

conn = psycopg2.connect("dbname='#' user='#' host='#' password='#'")
cur = conn.cursor()


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


for p in PAGES:
    res = requests.get(BASE_URL + '/' + p, verify=False)
    bs = BeautifulSoup(res.text, "html.parser")
    data = bs.findAll(text=True)
    result = '\n'.join(filter(visible, data))
    cur.execute("""insert into public.fts_example(file_name,file_content) values(%s,%s)""", (p, result))
    conn.commit()
