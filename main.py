
import codecs
import requests
from bs4 import BeautifulSoup
import re

LoginURL=r"https://www.royalroad.com/account/login?returnurl=%2Fhome"
FollowsURL=r"https://www.royalroad.com/my/follows"
# Fill in your details here to be posted to the login form.
payload = {
    'email': '@.com',
    'password': 'password'
}
LinkClass="btn-primary"
def SearchForLinks(FollowsURL,LinkClass):
    r = requests.get(FollowsURL)
    soup = BeautifulSoup(r.content, "html.parser")
    for link in soup.find_all('a'):
        print(link.get('href'))
    return soup.find_all('a')
def ChapterLinks(href):
    return href and re.compile(r"chapter/next/[0-9]+").search(href)
def GetNextChapter():
    r = requests.get(FollowsURL)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup.find_all('a')

def FindLongestText(soup):
    LastString=""
    for string in soup.strings:
        if(len(string.string)>len(LastString)):
            LastString=string.string
    return LastString




# opens a sessions with login and password
with requests.Session() as s:
    p = s.post(LoginURL, data=payload)
    r = s.get(FollowsURL)    
    LinksSite=BeautifulSoup(r.content,'html.parser')
    # gets into links inside follows
    if LinksSite is not None:
        print('Login...')
       # with codecs.open('page','a',"utf-8") as book:
            #book.writelines(LinksSite.prettify())
    for link in LinksSite.find_all('li',r'list-item'):
        if link.contents[0].get_text("|", strip=True) != 'Last Read Chapter:':
            continue
        print('acquiring links...')
        #for con in link.contents:
            #print(con)
        #clicks a link
        chapter=s.get("https://www.royalroad.com"+link.contents[1].get('href'))
        chapter=BeautifulSoup(chapter.content, "html.parser")
        rawtitle=chapter.h2.get_text(strip=True)
        #Forbiddenslist=['*','.','"','/','\\',':',';',r'|',',',"'",'<','>',']','[']
        translation_table = dict.fromkeys(map(ord, '*."/\\:;|,\'><]['), None)
        title=rawtitle.translate(translation_table)
        title=title.split()
        FinalTitle=''
        for word in title:
            FinalTitle=FinalTitle+word.capitalize()
        content='Start'
        #content=chapter.find('div','chapter-inner chapter-content').get_text()
        print(FinalTitle)
        with codecs.open(r"C:\Users\Woda\Desktop\RoyalRoadBooks"+"\\"+FinalTitle+".txt",'a',encoding="utf-8") as book:
            book.writelines(content)        
        while True:
            try:
                NextChapter = chapter.find('link',rel='next').get("href")
                chapter=s.get("https://www.royalroad.com"+NextChapter)
                chapter=BeautifulSoup(chapter.content, "html.parser")
                content=chapter.find('div','chapter-inner chapter-content').get_text()
                content=content.replace('.','. ')
                content=content.replace('.  ','. ') 
                with codecs.open(r"C:\Users\Woda\Desktop\RoyalRoadBooks"+"\\"+FinalTitle+".txt",'a',encoding="utf-8") as book:
                    book.writelines(content) 
            except:
                print(FinalTitle+" finished...")
                break
       


