import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re 
RESULT_PATH = 'C:/Users/김석진/'
now = datetime.now() #파일이름 현 시간으로 저장하기
driver=webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

def get_youtube(n_url):
    
    youtube_detail = []
    driver.get(n_url)
    time.sleep(4)
    breq=driver.page_source
    bsoup=BeautifulSoup(breq,'lxml')
#영상제목[0]
    title =bsoup.select('#container > h1 > yt-formatted-string')[0].text  #대괄호는  h3#articleTitle 인 것중 첫번째 그룹만 가져오겠다.
    youtube_detail.append(title)
#조회수[1]
    view =bsoup.find('span','view-count style-scope yt-view-count-renderer').string
    youtube_detail.append(view)
#좋아요[2]고쳐야함
    like=bsoup.find_all('yt-formatted-string',{'class':'style-scope ytd-toggle-button-renderer style-text'})[0]
    youtube_detail.append(like.text)
#싫어요[3]고쳐야함
    bad=bsoup.find_all('yt-formatted-string',{'class':'style-scope ytd-toggle-button-renderer style-text'})[1]
    youtube_detail.append(bad.text)
#게시날짜[4]
    date=bsoup.select("#date > yt-formatted-string")[0].string
    youtube_detail.append(date)
#게시자[5]
    youtuber=bsoup.select("#text > a")[0].string   
    youtube_detail.append(youtuber)
#게임이름
    game=bsoup.select('#title')[1].string
    youtube_detail.append(game)
#댓글 크롤링
    time.sleep(4)
    SCROLL_PAUSE_TIME = 10.0
    body = driver.find_element_by_tag_name('body')
    k = 0
    while True:
        time.sleep(4)
        last_height = driver.execute_script('return document.documentElement.scrollHeight')
        if k==1:
            break
        for i in range(10):
            body.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            break;
        k = k+1

    youtube_comments = bsoup.find_all('ytd-expander',{'class':'style-scope ytd-comment-renderer'})
    
    for i in range(len(youtube_comments)):
        str_tmp = str(youtube_comments[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        str_tmp = str_tmp.replace(' ','')
        str_tmp = str_tmp.replace('간략히','')
        str_tmp = str_tmp.replace('자세히보기','')
        youtube_detail.append(str_tmp)
        
   
    return youtube_detail


def crawler(query):
    
     f = open("C:/Users/김석진/youtube_text.txt", 'w', encoding='utf-8')
     url ="https://www.youtube.com/" + query + "/trending"
     driver.get(url)
     time.sleep(4)
     req=driver.page_source
     soup=BeautifulSoup(req,'lxml')
     href = soup.find_all('a',{'class':"yt-simple-endpoint style-scope ytd-grid-video-renderer"})
     youtube_coments.pd
     for hrefs in href:
         n_url="https://www.youtube.com"+hrefs["href"]
         youtube_detail=get_youtube(n_url)
         f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(youtube_detail[0], youtube_detail[5], youtube_detail[4], youtube_detail[1], youtube_detail[2],youtube_detail[3],youtube_detail[6]))
     f.close()
     driver.close()
def excel_make():
    data = pd.read_csv(RESULT_PATH+'youtube_text.txt', sep='\t',header=None, error_bad_lines=False)
    data.columns = ['제목','유튜버','게시날짜','조회수','좋아요','싫어요','게임종류','댓글']
    print(data)
    
    xlsx_outputFileName = '%s-%s-%s  %s시 %s분 %s초 유튜브 인기검색 데이터.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    #xlsx_name = 'result' + '.xlsx'
    data.to_excel(RESULT_PATH+xlsx_outputFileName, encoding='utf-8')

     
def main(): 

    query = input("인기검색어 입력: ")
    crawler(query)
    excel_make()
    #분류 하는거
    #db저장 
    
main()
