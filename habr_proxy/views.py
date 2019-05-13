import re

import bs4
from proxy.views import proxy_view


def habr_proxy(request, path):
    url = ('https://habr.com/' + path)
    response = proxy_view(request, url)
    if not re.match('text/html', response['Content-Type']):
        return response

    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    habr_link = re.compile('https?://habr\.com')
    local_link = r'http://127.0.0.1:8000'
    for string in soup.findAll(string=True):
        if (type(string) == bs4.element.NavigableString and
                string.parent.name not in ['script', 'style']):
            res = re.sub(r'\b(\w{6})\b', r'\1™', string)
            if(string != res):
                string.replaceWith(res)

    for attr_name in ('xlink:href', 'href'):
        for tag in soup.find_all(attrs={attr_name: habr_link}):
            link = re.sub(habr_link, local_link, tag[attr_name])
            tag[attr_name] = link

    response.content = soup.prettify(formatter=_formatter)
    return response

def _formatter(str):
    if (type(str) == bs4.element.NavigableString and
            str.parent.name not in ['script', 'style']):
        return str.replace('>', '&gt;').replace('<', '&lt;')
    return str
