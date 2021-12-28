import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI


def reqContent():
    url = "https://www.ndtv.com/business/cryptocurrency/crypto-coins";
    cont = requests.get(url);
    soup = BeautifulSoup(cont.text, 'lxml');
    tbody = soup.find('tbody');
    trs = tbody.find_all('tr');
    toRtn = {"items" : []};
    for tr in trs:
        toAdd = {};
        tds = tr.find_all('td');
        imageTag = tds[0].img;
        imageLink = imageTag['src'];
        nameTag = tds[0].find(class_="_flx crynm");
        bracketIndex = nameTag.text.find('(');
        fullName = nameTag.text[0:bracketIndex];
        shortName = nameTag.text[bracketIndex+1:-1];
        cryptoPrice = tds[1].text[2:];
        DayChange = tds[2].text;
        DayChangeArrowTag = tds[2].span;
        DayChangeArrowDirection = DayChangeArrowTag['class'][1];
        DayChangePercent = tds[3].text;
        if(DayChangeArrowDirection=='up'):
            DayChange = '+'+DayChange;
            DayChangePercent='+'+DayChangePercent;
        else:
            DayChange = '-'+DayChange;
            DayChangePercent='-'+DayChangePercent;
        toAdd['cryptoName'] = fullName;
        toAdd['shortName']=shortName;
        toAdd['currentPrice']=cryptoPrice.strip()[2:];
        toAdd['DayChange']=DayChange; 
        toAdd['DayChangePercent']=DayChangePercent;
        toAdd["imageLink"] = imageLink;      
        toRtn['items'].append(toAdd);
    return toRtn;
app = FastAPI()
@app.get('/')
def index():
    return reqContent();
