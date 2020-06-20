"""
@outhor Erdem Şahin

"""

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from IPython.display import clear_output



#Kategoriler
# Linkler çok fazla veri çıkardığından kapatıldı. 
# Linkleri açarak veriyi arttırabilirsiniz.
sections = [#"https://www.sondakika.com/spor/",
            "https://www.sondakika.com/dunya/"
            #"https://www.sondakika.com/koronavirus/",
            #"https://www.sondakika.com/teknoloji/"
]

urls = []
# Öncelikle bir Kategori seçiyoruz.
for section in sections:
    # Kategorinin içerisinde sırayla gezicek veri fazla çıktığından 2 yapıldı sadece 1 defa dolaşıyor. 
    # Daha fazla sayfa kontrolü için yükseltiniz
    for i in range(1, 2):
        try:
            # URL'imizi oluşturuyoruz. Örneğin;
            # https://www.sondakika.com/spor/1
            newurl = section + str(i)
            print(newurl)

            # Url'nin içerisindeki bütün html dosyasını indiriyoruz.
            html = requests.get(newurl).text
            soup = bs(html, "lxml")

            # makaleleri buradan tags adında bir değişkene topluyor.
            tags = soup.findAll("ul", class_="news-list")[0]

            print(tags)

            # Sırayla bütün makalelere girip, href'in içerisindeki linki urls adlı listemize append ediyor.
            for a in tags.find_all('a', href=True):
                urls.append((section.split("/")[4], a['href']))
        except IndexError:
            break

urldata = pd.DataFrame(urls)
urldata.columns = ["Kategori","Link"]
urldata.head()
#Bazı linkler çoklamışlar, onlardan kurtulmak için drop_duplicates() kullanıldı.
urldata = urldata.drop_duplicates()
urldata.to_csv('urldata.csv')

sondakika = "https://www.sondakika.com"
def GetData(url):
    try:
        url = sondakika + str(url)
        # Url içerisindeki html'i indiriyor.
        html = requests.get(url).text
        soup = bs(html, "lxml")

        # Belirlediğimiz element'in altındaki bütün p'leri seçiyoruz.
        body_text = soup.findAll("div", class_="wrapper detay-v3_3 haber_metni")[0].findAll('p')

        # Body_text adındaki metni tek bir string üzerinde topluyor.
        body_text_big = ""
        for i in body_text:
            body_text_big = body_text_big + i.text

        return ((url, body_text_big))

    # Link boş ise verilen hata üzerine Boş Data mesajını döndürüyor.
    except IndexError:
        return ("Boş Data")


#Veri kazıma, Urldatasındaki linkleri tek tek fonksiyon ile çalıştırıp, sonuçları bigdata listesine kaydediyor.
bigdata = []
k = 0
for i in urldata.Link:
    clear_output(wait=True)
    print(k)
    print(i)
    bigdata.append(GetData(i))
    k = k + 1

#Verileri DataFrame olarak kaydetme
bigdatax = pd.DataFrame(bigdata)
bigdatax.columns = ["Link","Body_text"]
bigdatax = bigdatax.loc[bigdatax.Link.drop_duplicates().index]
bigdatax.index = range(0,len(bigdatax))
bigdatax.head()
bigdatax.to_csv("bigdata.csv")
