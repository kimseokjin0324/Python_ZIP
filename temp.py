import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import openpyxl
from konlpy.tag import Okt
from collections import Counter
import os
from openpyxl import load_workbook
okt=Okt()
RESULT_PATH = 'C:/Users/김석진/.spyder-py3/' #저장되는 공간설정(변수)
driver=webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

def get_youtube(n_url):
    
    youtube_detail = []
    driver.get(n_url)
    time.sleep(4)#유튜브창 로딩을 위한 시간지연
    SCROLL_PAUSE_TIME = 10.0
    body = driver.find_element_by_tag_name('body')
    #댓글 크롤링을 위한 스크롤 
    k = 0
    while True:
        time.sleep(4)
        last_height = driver.execute_script('return document.documentElement.scrollHeight')
        if k==1:
            break
        for i in range(5):
            body.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            break;
        k = k+1
    breq=driver.page_source
    bsoup=BeautifulSoup(breq,'lxml')
#댓글 크롤링
    youtube_comments = []
    youtube_comment = bsoup.select("yt-formatted-stringcontent-text")
    for i in range(len(youtube_comment)):
        str_tmp = str(youtube_comment[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        str_tmp = str_tmp.replace('   ','')
        youtube_comments.append(str_tmp)
#영상제목[0]
    title =bsoup.select('#container > h1 > yt-formatted-string')[0].text  #대괄호는  h3#articleTitle 인 것중 첫번째 그룹만 가져오겠다.
    youtube_detail.append(title)
#조회수[1]
    view =bsoup.find('span','view-count style-scope yt-view-count-renderer').string
    youtube_detail.append(view)
#좋아요[2]
    like=bsoup.find_all('yt-formatted-string',{'class':'style-scope ytd-toggle-button-renderer style-text'})[0]
    youtube_detail.append(like.text)
#싫어요[3]
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

    
     
    return youtube_detail,youtube_comments

def crawler(query):
     # 맨처음 크롤링한 데이터를 메모장에 저장
     f = open("C:/Users/김석진/.spyder-py3/1.txt", 'w', encoding='utf-8')
     url ="https://www.youtube.com/" + query + "/trending"
     driver.get(url)
     time.sleep(4)
     req=driver.page_source
     soup=BeautifulSoup(req,'lxml')
     href = soup.find_all('a',{'class':"yt-simple-endpoint style-scope ytd-grid-video-renderer"})
     youtube=[]
     for hrefs in href:
             n_url="https://www.youtube.com"+hrefs["href"]
             youtube=get_youtube(n_url)
  #-------------------------------------------------글자 제거          
             view = youtube[0][2]
             if '천' in view:
                view = view.replace('천','')
                num = float(view) * 1000
                youtube[0][2] = int(num)
             elif '만'in view:
                view = view.replace('만','')
                num = float(view) * 10000
                youtube[0][2] = int(num)
             
             
                
             view2 = youtube[0][1]
             if '조회수' in view2:
                    view2 = view2.replace('조회수','')
                    view2 = view2.replace('회','')
                    youtube[0][1] = str(view2) 
  #-----------------------------------------------------글자제거          
             f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t".format(youtube[0][0], youtube[0][5], youtube[0][4], youtube[0][1], youtube[0][2],youtube[0][3],youtube[0][6]))
             f.write("{}\t \n".format(youtube[1]))
             
            
     f.close()            
     driver.close()
def excel_make():
    #메모장이 저장된 공간에서 txt를 load해 csv로 변환
    data = pd.read_csv(RESULT_PATH+'1.txt', sep='\t',header=None, error_bad_lines=False)
    data.columns = ['제목','유튜버','게시날짜','조회수','좋아요','싫어요','게임종류','댓글,' , '    ']
    xlsx_outputFileName = '유튜브 인기검색 데이터.xlsx' 
    data.sort_values('좋아요')
    data.to_excel(RESULT_PATH+xlsx_outputFileName, encoding='utf-8')
    
def excel_add():
    #위 함수에서 만든 엑셀파일에 시트를 추가하는 코드 
    data=pd.read_excel(RESULT_PATH+'유튜브 인기검색 데이터.xlsx')
    book=load_workbook('C:/Users/김석진/.spyder-py3/유튜브 인기검색 데이터.xlsx')
    writer=pd.ExcelWriter(RESULT_PATH+'유튜브 인기검색 데이터.xlsx',engine='openpyxl')
    comments=data['댓글,']
    game=data['게임종류']
    game=Counter(game).most_common()
    game=pd.DataFrame(game)
    game.to_excel(RESULT_PATH+'유튜브 인기 게임 순위 빈도수.xlsx', encoding='utf-8')
    writer.book=book
    for i in comments.index:
        nouns=okt.nouns(comments.iloc[i])
        df_comments=pd.DataFrame(nouns)
        df_comments.to_excel(writer,'순위'+str(i+1)+'위')

    writer.save()
    writer.close()


def main(): 

    query = input("인기검색어(query) 입력: ")
    crawler(query)
    excel_make()
    excel_add()
main()