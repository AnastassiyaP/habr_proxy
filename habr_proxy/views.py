import re

import bs4
import requests

from django.http import HttpResponse
from proxy.views import proxy_view

def habr_proxy(request, path):
    url = ('https://habr.com/' + path)
    response = proxy_view(request, url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    for string in soup.findAll(string=True):
        if (type(string) == bs4.element.NavigableString and
              string.parent.name not in ['script','style']):
            res = re.sub(r'\b(\w{6})\b', r'\1™', string)
            if(string != res):
                string.replaceWith(res)

    for a in soup.find_all('a', href=re.compile('https?://habr\.com')):
        link = re.sub(r'^https?://habr.com', r'http://127.0.0.1:8000', a['href'])
        a['href'] = link
        
    response.content = soup.prettify(formatter=None)
    return response
