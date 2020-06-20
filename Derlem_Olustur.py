import pandas as pd
import nltk

data = pd.read_csv('bigdata.csv')
data.head()

def preprocess(ReviewText):
    #Verinin okunması için temizlik yapıldı.
    ReviewText = ReviewText.str.replace("(<br/>)", "")
    ReviewText = ReviewText.str.replace('(<a).*(>).*(</a>)', '')
    ReviewText = ReviewText.str.replace('(&amp)', '')
    ReviewText = ReviewText.str.replace('(&gt)', '')
    ReviewText = ReviewText.str.replace('(&lt)', '')
    ReviewText = ReviewText.str.replace("(\')", "")
    ReviewText = ReviewText.str.replace(".", ". ")
    ReviewText = ReviewText.str.replace("(  )", ' ')
    ReviewText = ReviewText.str.replace('(\xa0)', ' ')
    #Verideki Linkleri Kaldır.
    ReviewText = ReviewText.str.replace(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', ' ')

    return ReviewText

data['Body_text'] = preprocess(data['Body_text'])

text = []
for i in range(len(data)):
    text.append(data.iloc[i, 2])
print(text)

corpus = []
for i in range(len(text)):
    corpus.append(nltk.sent_tokenize(text[i]))

Derlem = []
for i in range(len(corpus)):
    for k in range(len(corpus[i])):
        # print("url :"+ data.iloc[i,1])
        # print("segment no :"+ str(k))
        # print("cumle icerigi :" +str(corpus[i][k]))
        words = corpus[i][k].split(' ')
        sozcuk_sayisi = len(words)
        # print("sozcuk sayisi :" + str(sozcuk_sayisi)+"\n")
        Derlem.append((data.iloc[i,1],k,corpus[i][k],sozcuk_sayisi))

Derlem2 = pd.DataFrame(Derlem)
Derlem2.columns = ["url","segment_no","cumle_icerigi","sözcük_sayisi"]
Derlem2.index = range(0,len(Derlem2))
Derlem2.head()

Derlem2.to_csv("Derlem.csv")
# test için xlsx dosyası oluşturuldu.
Derlem2.to_excel("Derlem.xlsx", sheet_name="Data")