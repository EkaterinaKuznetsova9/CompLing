from lxml import html
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
import re

kolNextList=1
# as *10
lemmatizedTexts=[]
lemmJoinTexts=[]
allTexts=[]
fwd = open('Texts.txt', 'w')

topics={"style"}
for iTopic in range(len(topics)):
    nameCategory = topics.pop()
    print(nameCategory)
    nameLink="http://www.ng.ru/" + nameCategory + "/"
    htmlLink = urllib.request.urlopen(nameLink)
    soup = BeautifulSoup(htmlLink, 'html.parser', parse_only=SoupStrainer('a'))
    sameLink = 0
    links=[]

    nextLinkElement=0
    for idStr in range(kolNextList):
        if idStr>0:
            nextLink=nextLinkElement['href']
            htmlLink = urllib.request.urlopen("http://www.ng.ru" + nextLink)
            soup = BeautifulSoup(htmlLink, 'html.parser', parse_only=SoupStrainer('a'))
        for i in soup.find_all('a', href=True):
            if '.html' in i['href'] and i['href'].startswith('http') and 'www.ng' in i['href'] and nameCategory in i['href']:
                link=i['href']
                ind1=link.find('www.ng')
                ind2=link.find('.html')
                link=link[ind1:ind2+5]
                if sameLink==0:
                    link1=link
                    sameLink=1
                    links.append(link)
                else:
                    if not link==link1:
                        link1=link
                        links.append(link)
            if 'PAGEN_' in i['href']:
                nextLinkElement=i

    for item in links:
        # print(item)
        URL = "http://"+item
        page = html.parse(URL)
        title = page.getroot().find_class('htitle')[0].text
        # print(title)
        full_text = page.getroot().find_class('typical')[0]
        text = ""
        for el in full_text[1:]:
            if el.tag in ['p']:
                if not el.text==None:
                    text += el.text
                    for subel in el:
                        if subel.tag == 'a':
                            if not subel.text==None:
                                text += subel.text
                    text += '\n'

        text=re.sub(r'[\n\r\t]',' ', text)
        text = title + "\n" + text
        # print(text)
        fwd.write(text + "\n\n")